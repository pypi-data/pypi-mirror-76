#!/usr/bin/env python
#
# Copyright (C) 2020 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import logging
import math
import os
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import UnidentifiedImageError
from majormode.perseus.model.enum import Enum
from majormode.perseus.utils import cast
import exifread
import face_recognition
import numpy


# Default color for area outside the rotated image.
DEFAULT_FILL_COLOR = (255, 255, 255)

# Default space in pixels to add on the left and the right, respectively
# on the top and bottom, of the detected face.
DEFAULT_VERTICAL_PADDING = 0.25
DEFAULT_HORIZONTAL_PADDING = 0.25

# Exif tag which value corresponds to the orientation, which indicates
# the orientation of the camera relative to the captured scene.
EXIF_TAG_ORIENTATION = 'Image Orientation'

EXIF_TAG_ORIENTATION_ROTATION_0 = 1
EXIF_TAG_ORIENTATION_ROTATION_90 = 8
EXIF_TAG_ORIENTATION_ROTATION_180 = 3
EXIF_TAG_ORIENTATION_ROTATION_270 = 6
EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_0 = 2
EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_90 = 7
EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_180 = 4
EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_270 = 5

EXIF_PIL_TRANSPOSITIONS = {
    EXIF_TAG_ORIENTATION_ROTATION_0: [],
    EXIF_TAG_ORIENTATION_ROTATION_90: [Image.ROTATE_90],
    EXIF_TAG_ORIENTATION_ROTATION_180: [Image.ROTATE_180],
    EXIF_TAG_ORIENTATION_ROTATION_270: [Image.ROTATE_270],
    EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_0: [Image.FLIP_LEFT_RIGHT],
    EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_90: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],
    EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_180: [Image.FLIP_TOP_BOTTOM],
    EXIF_TAG_ORIENTATION_FLIP_LEFT_RIGHT_ROTATION_270: [Image.FLIP_LEFT_RIGHT, Image.ROTATE_270],
}

LOGGING_FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

FaceFeature = Enum(
    'chin',
    'left_eyebrow',
    'right_eyebrow',
    'nose_bridge',
    'nose_tip',
    'left_eye',
    'right_eye',
    'top_lip',
    'bottom_lip',
)

EyelidOpeningState = Enum(
    'narrowed_or_closed',
    'normally_open',
    'widely_open'
)


DEFAULT_FACE_FEATURE_COLORS = {
    FaceFeature.chin: (255, 0, 0),
    FaceFeature.left_eyebrow: (255, 0, 0),
    FaceFeature.right_eyebrow: (255, 0, 0),
    FaceFeature.nose_bridge: (255, 0, 0),
    FaceFeature.nose_tip: (255, 0, 0),
    FaceFeature.left_eye: (255, 0, 0),
    FaceFeature.right_eye: (255, 0, 0),
    FaceFeature.top_lip: (255, 0, 0),
    FaceFeature.bottom_lip: (255, 0, 0),
}


class BiometricPassportPhotoException(Exception):
    """
    Base class of biometric passport photo exceptions.
    """
    def __init__(self, message, payload=None):
        super().__init__(message)
        self.payload = payload


class NoFaceDetectedException(BiometricPassportPhotoException):
    """
    Raise when no face has been detected in a photo
    """


class MultipleFacesDetectedException(BiometricPassportPhotoException):
    """
    Raised when multiple faces have been detected in a photo.
    """


class MissingFaceFeaturesException(BiometricPassportPhotoException):
    """
    Raised when some features are missing from the detected face.
    """


class ObliqueFacePoseException(BiometricPassportPhotoException):
    """
    Raised when the head doesn't face the camera straight on.
    """


class OpenedMouthOrSmileException(BiometricPassportPhotoException):
    """
    Raised when the mouth is not closed or with a smile.
    """


class AbnormalEyelidOpeningStateException(BiometricPassportPhotoException):
    """
    Raised when an eyelid is widely opened, narrowed or closed.
    """
    def __init__(self, message, eyelid_opening_state):
        super().__init__(message)
        self.eyelid_opening_state = eyelid_opening_state


class UnevenlyOpenEyelidException(BiometricPassportPhotoException):
    """
    Raised when a eye is more opened/closed than the other.
    """


class TransformedPoint2D:
    """
    Represent a 2D point that has been rotated.
    """
    def __init__(self,x, y, angle=0.0, origin=(0, 0)):
        """

        :param x: Abscissa of the point on the x-axis.

        :param y: Ordinate of the point on the y-axis.

        :param angle: Angle in degrees counter clockwise of the rotation of
            the point.

        :param origin: A tuple `(x0, y0)` representing the center of the
            rotation.
        """
        self.__x = x
        self.__y = y
        self.__set_angle(angle, origin)

    def __set_angle(self, angle, origin):
        self.__angle = angle
        if angle == 0:
            self.__transformed_x = self.__x
            self.__transformed_y = self.__y
        else:
            origin_x, origin_y = origin

            self.__transformed_x = round(
                (self.__x - origin_x) * math.cos(angle)
                - (self.__y - origin_y) * math.sin(angle)) \
                + origin_x

            self.__transformed_y = round(
                (self.__x - origin_x) * math.sin(angle)
                + (self.__y - origin_y) * math.cos(angle)) \
                + origin_y

    @property
    def angle(self):
        return self.__angle

    @property
    def x(self):
        return self.__transformed_x

    @property
    def y(self):
        return self.__transformed_y


class BiometricPassportPhoto:
    @staticmethod
    def __assert_all_face_features(face_features):
        """
        Assert that all the features of a face have been detected.


        :param face_features: A dictionary of found face feature locations
            where the key corresponds to an item of the enumeration
            `FaceFeature`, and the value corresponds to a list of tuple
            `(x, y)` representing a point of the face feature.


        :raise MissingFaceFeaturesException: If one or more face features are
            missing.
        """
        if not isinstance(face_features, dict):
            raise ValueError("wrong argument 'face_features'")

        if any([face_feature not in FaceFeature for face_feature in face_features]):
            raise ValueError("the list of face features must contain items of the enumeration 'FaceFeature' only")

        missing_face_features = [
            face_feature
            for face_feature in FaceFeature
            if face_feature not in face_features
        ]

        if len(missing_face_features):
            raise MissingFaceFeaturesException(
                "missing features in the detected face",
                payload={'face_features': missing_face_features})

    @classmethod
    def __assert_front_full_face(
            cls,
            face_features,
            forbid_oblique_face=True,
            perpendicularity_threshold=0.1,
            middle_threshold=0.14):
        """
        Indicate whether the pose directly faces the camera with full face in
        view.


        :param face_features: A dictionary of found face feature locations
            where the key corresponds to an item of the enumeration
            `FaceFeature`, and the value corresponds to a list of tuple
            `(x, y)` representing a point of the face feature.

        :param forbid_oblique_face: Indicate whether the check if the face is
            oblique.

        :param perpendicularity_threshold: A floating number between `0.0` and
            `1.0` representing the maximum acceptable perpendicularity between
            the midsagittal facial and the midhorizontal iris lines.

        :param middle_threshold: A floating number between `0.0` and `1.0`
            representing the maximum acceptable threshold that the midsagittal
            facial line interesects the midhorizontal iris line in the middle.


        :return: `True` if the photo represents a photo portrait of a person
            who faces directly the camera with full face in view; `False`
            otherwise.


        :raise ObliqueFacePoseException: If the face is not directly facing the
            camera.
        """
        cls.__assert_all_face_features(face_features)

        # Check that the midsagittal facial line (line passing through points 27
        # and 30) is perpendicular to the midhorizontal iris line (line passing
        # through points 0 and 17).
        #
        # For a definition of each point index, see:
        #
        #     https://cdn-images-1.medium.com/max/1600/1*AbEg31EgkbXSQehuNJBlWg.png
        chin = face_features[FaceFeature.chin]
        left_ear_top_x, left_ear_top_y = chin[0]
        right_ear_top_x, right_ear_top_y = chin[-1]
        left_right_ear_top_vector = (
            right_ear_top_x - left_ear_top_x,
            right_ear_top_y - left_ear_top_y)

        nose_bridge = face_features[FaceFeature.nose_bridge]
        nose_bridge_top_x, nose_bridge_top_y = nose_bridge[0]
        nose_bridge_bottom_x, nose_bridge_bottom_y = nose_bridge[-1]
        nose_bridge_vector = (
            nose_bridge_bottom_x - nose_bridge_top_x,
            nose_bridge_bottom_y - nose_bridge_top_y)

        angle = cls.__calculate_vectors_angle(left_right_ear_top_vector, nose_bridge_vector)
        perpendicularity = cls.__calculate_relative_difference(angle, 90)
        if perpendicularity > perpendicularity_threshold:
            raise ObliqueFacePoseException("the midsagittal facial and the midhorizontal iris lines are not perpendicular to each other")

        # Check that the midsagittal facial line (line passing through points 27
        # and 30) intersects the midhorizontal iris line (line passing through
        # points 0 and 17) in almost the middle.
        #
        # @note: We don't try to calculate the slope and the y-intersect of the
        #     midsagittal facial line and the midhorizontal iris line as
        #     midsagittal facial line may be vertical (no y-intersect):
        #
        #       m1, b1 = cls.__calculate_line_equation(
        #           (left_ear_top_x, left_ear_top_y),
        #           (right_ear_top_x, right_ear_top_y))
        #       m2, b2 = cls.__calculate_line_equation(
        #           (nose_bridge_top_x, nose_bridge_top_y),
        #           (nose_bridge_bottom_x, nose_bridge_bottom_y))
        #       x, y = cls.__calculate_line_intersection((m1, b1), (m2, b2))
        if forbid_oblique_face:
            x, y = cls.__calculate_4point_line_intersection(
                (left_ear_top_x, left_ear_top_y),
                (right_ear_top_x, right_ear_top_y),
                (nose_bridge_top_x, nose_bridge_top_y),
                (nose_bridge_bottom_x, nose_bridge_bottom_y))

            middle = cls.__calculate_relative_difference(abs(left_ear_top_x - x), abs(right_ear_top_x - x))
            if middle > middle_threshold:
                raise ObliqueFacePoseException("the midsagittal facial line doesn't intersect the midhorizontal iris line in the middle")

    @classmethod
    def __assert_mouth_closed_with_no_smile(cls, face_features, rima_oris_lips_areas_threshold=0.05):
        """
        Assert that the mouth is closed with no smile.


        :param face_features: A dictionary of found face feature locations
            where the key corresponds to an item of the enumeration
            `FaceFeature`, and the value corresponds to a list of tuple
            `(x, y)` representing a point of the face feature.

        :param rima_oris_lips_areas_threshold: The maximum relative difference
            between the area of the orifice of the mouth (rima oris) with the
            areas of the upper and lower lips.


        :raise OpenedMouseOrSmileException: If the mouth is not closed or with
            a smile.
        """
        upper_lip = face_features[FaceFeature.top_lip]
        lower_lip = face_features[FaceFeature.bottom_lip]

        # Build the polygon corresponding to the orifice of the mouth (rima
        # oris) with the bottom line of the upper lip and the top line of the
        # lower lip.
        lines = cls.__split_line_by_angle(upper_lip, 90)
        if len(lines) != 2:
            raise ValueError('undetected top lip curve')
        upper_lip_bottom_line = lines[1]

        lines = cls.__split_line_by_angle(lower_lip, 90)
        if len(lines) != 2:
            raise ValueError('undetected bottom lip curve')
        lower_lip_top_line = lines[1]

        # The points composing the bottom line of the upper lip are listed from
        # right to left, while those composing the top line of the lower lip are
        # listed from left to right. Reverse these positions to build the
        # polygon corresponding to the mouth's orifice.
        mouth_orifice = list(reversed(upper_lip_bottom_line)) + list(reversed(lower_lip_top_line))

        # Check the relative difference of the mouth orifice's area with those
        # of the upper and lower lips.
        mouth_orifice_area = cls.__calculate_polygon_area(mouth_orifice)
        lips_area = cls.__calculate_polygon_area(upper_lip) + cls.__calculate_polygon_area(lower_lip)

        # Check that the mouth orifice area is not larger than the lips area,
        # and that the relative difference between these 2 areas is below the
        # specified threshold.
        if mouth_orifice_area > lips_area:
            raise OpenedMouthOrSmileException('the mouth must not be largely opened')

        lips_rima_oris_areas_relative_difference = cls.__calculate_relative_difference(lips_area, mouth_orifice_area)
        if lips_rima_oris_areas_relative_difference < 1 - rima_oris_lips_areas_threshold:
            raise OpenedMouthOrSmileException('the mouth must not be opened or with a smile')

    @classmethod
    def __assert_opened_eyes(
            cls,
            face_features,
            eyelid_too_closed_threshold=0.16,
            eyelid_too_open_threshold=0.55,
            eye_area_similarity_threshold=0.08,
            forbid_unevenly_open_eye=True):
        """
        Assert that both eyes are normally opened.


        :param face_features: A dictionary of found face feature locations
            where the key corresponds to an item of the enumeration
            `FaceFeature`, and the value corresponds to a list of tuple
            `(x, y)` representing a point of the face feature.

        :param eyelid_too_closed_threshold: A float value used to detect
            whether the eyelids of an eye is narrowed or closed (cf.
            @{link __detect_eyelid_opening_state}).

        :param eyelid_too_open_threshold: A float value used to detect whether
            the eyelids of an eye are widely open (cf.
            @{link __detect_eyelid_opening_state}).

        :param eye_area_similarity_threshold: A float value representing the
            maximum relative difference between the visible areas of the two
            eyes.

        :param forbid_unevenly_open_eye: Indicate whether to check if the 2
            eyelids are evenly open (same area of the visible part of the eyes).


        :raise AbnormalEyelidOpeningStateException: If an eye is considered
            widely open, narrowed, or closed.

        :raise UnevenlyOpenEyelidException: if an eye is more open than the
            other.
        """
        # Check whether the 2 eyelids are normally open.
        left_eye = face_features[FaceFeature.left_eye]
        left_eyebrow = face_features[FaceFeature.left_eyebrow]

        left_eyelid_opening_state = cls.__detect_eyelid_opening_state(
            left_eye, left_eyebrow,
            eyelid_too_closed_threshold=eyelid_too_closed_threshold,
            eyelid_too_open_threshold=eyelid_too_open_threshold)
        if left_eyelid_opening_state != EyelidOpeningState.normally_open:
            raise AbnormalEyelidOpeningStateException("the left eyelid is not normally open", left_eyelid_opening_state)

        right_eye = face_features[FaceFeature.right_eye]
        right_eyebrow = face_features[FaceFeature.right_eyebrow]

        right_eyelid_opening_state = cls.__detect_eyelid_opening_state(
            right_eye, right_eyebrow,
            eyelid_too_closed_threshold=eyelid_too_closed_threshold,
            eyelid_too_open_threshold=eyelid_too_open_threshold)
        if right_eyelid_opening_state != EyelidOpeningState.normally_open:
            raise AbnormalEyelidOpeningStateException(
                "the right eyelid is not normally open", right_eyelid_opening_state)

        # Check whether the 2 eyelids are evenly open (same area of the
        # visible part of the eyes).
        if forbid_unevenly_open_eye:
            left_eye_area = cls.__calculate_polygon_area(left_eye)
            right_eye_area = cls.__calculate_polygon_area(right_eye)
            eye_areas_relative_difference = cls.__calculate_relative_difference(left_eye_area, right_eye_area)
            if eye_areas_relative_difference > eye_area_similarity_threshold:
                less_opened_eye, more_opened_eye = ('right', 'left') if left_eye_area > right_eye_area \
                    else ('left', 'right')
                raise UnevenlyOpenEyelidException(
                    f"the {more_opened_eye} eye is more opened than the {less_opened_eye} eye")

    @staticmethod
    def __build_vectors(points):
        """
        Return the list of vectors corresponding to a list of points forming a
        line.


        :param points: A list of 2D points `(x, y)`.


        :return: A list of 2D vectors `(x, y)` between each 2D points.
        """
        vectors = [
            (points[i + 1][0] - points[i][0],
             points[i + 1][1] - points[i][1])
            for i in range(len(points) - 1)
        ]

        vectors1 = []
        x1, y1 = points[0]
        for x2, y2 in points[1:]:
            vectors1.append((x2 - x1, y2 - y1))
            x1, y1 = x2, y2

        return vectors

    @staticmethod
    def __calculate_4point_line_intersection(point1, point2, point3, point4):
        """
        Calculate the coordinates of the point at the intersection of 2 lines
        L1 and L2 defined respectively by 2 distinct points.


        :param point1: A point `(x1, y1)` on the line L1.

        :param point2: A point `(x2, y2)` on the line L1.

        :param point3: A point `(x3, y4)` on the line L2.

        :param point4: A point `(x4, y4)` on the line L2.


        :return: A tuple `(x, y)` of the point at the intersection between the
            lines L1 and L2.


        :raise ValueError: If the two lines are parallel.
        """
        x1, y1 = point1
        x2, y2 = point2
        x3, y3 = point3
        x4, y4 = point4

        # Calculate the determinant (https://en.wikipedia.org/wiki/Line–line_intersection).
        denominator = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        if denominator == 0:
            raise ValueError("the two lines are parallel")

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator

        # Calculate the coordinates of the points at the intersection bwtween
        # the 2 lines.
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)

        return x, y

    @staticmethod
    def __calculate_face_angle(face_features):
        """
        Return the horizontal angle of the face.


        :param face_features: A dictionary of found face feature locations
            where the key corresponds to an item of the enumeration
            `FaceFeature`, and the value corresponds to a list of tuple
            `(x, y)` representing a point of the face feature.
        .

        :return: The horizontal angle in degrees of the face.
        """
        # Determine the vector that represents the midhorizontal iris line.
        chin = face_features[FaceFeature.chin]
        left_ear_top_x, left_ear_top_y = chin[0]
        right_ear_top_x, right_ear_top_y = chin[-1]

        vector_x = right_ear_top_x - left_ear_top_x
        vector_y = right_ear_top_y - left_ear_top_y

        # Determine the angle of the midhorizontal iris line with the the
        # x-axis.
        angle = math.atan(vector_y / vector_x)

        return angle

    @staticmethod
    def __calculate_line_equation(point1, point2):
        """
        Return the slope and the y-intercept of a line passing through two
        points.


        :param point1: A tuple `(x1, y1)` of a point on the line.

        :param point2: A tuple `(x2, y2)` of another point of the line.


        :return: A tuple `(m, b)` of the equation `y = m.x + b` where:

            * `m`: the slope that describes both the direction and the steepness
              of the line.

            * `b`: the y-intercept of the line, that is, the y-coordinate where the
              line intersects the y-axis.

            Or an integer representing the x-intercept if the line is vertical.
        """
        x1, y1 = point1
        x2, y2 = point2

        vertical_change = y2 - y1  # rise
        horizontal_change = x2 - x1  # run

        if horizontal_change == 0:
            return x1

        m = vertical_change / horizontal_change  # slope
        b = y1 - m * x1  # y-intercept

        return m, b

    @staticmethod
    def __calculate_line_intersection(line1, line2):
        """
        Calculate the coordinates of the point at the intersection between two
        lines.

        :param line1: A tuple `(m1, b1)` of the equation `y = m1.x + b1` of
            the first line, where:

            * `m1`: the slope that describes both the direction and the steepness
              of the line.

            * `b1`: the y-intercept of the line, that is, the y-coordinate where the
              line intersects the y-axis.


        :param line2: A tuple `(m2, b2)` of the second line.


        :return: A tuple `(x, y)` of the point at the intersection between the
            lines L1 and L2.


        :raise ValueError: If the two lines are parallel.
        """
        m1, b1 = line1
        m2, b2 = line2

        slope_difference = m1 - m2
        y_intercept_difference = b2 - b1

        if slope_difference == 0:
            raise ValueError("the two lines are parallel")

        x = y_intercept_difference / slope_difference
        y = m1 * y_intercept_difference / slope_difference + b1

        return x, y

    @staticmethod
    def __calculate_polygon_area(points):
        """
        Return the area of a polygon.


        :param points: A list of tuples `(x, y)` corresponding to the 2D
            points that compose a polygon.


        :return: The area of the polygon.


        :raise ValueError: If the list `points` has less than 3 items.
        """
        if len(points) < 3:
            raise ValueError("a polygon must be composed of 3 or more points")

        # The shoelace algorithm is a mathematical algorithm to determine the
        # area of a simple polygon whose vertices are described by their
        # Cartesian coordinates in the plane.
        #
        #     area = 0
        #     n = len(points)
        #     j = n - 1
        #     for i in range(n):
        #         area += (points[j][0] + points[i][0]) * (points[j][1] - points[i][1])
        #         j = i
        #
        #     area = abs(area) / 2
        #
        # However the Python implementation of this algorithm is ±45% slower
        # than the Pythonic implementation below, because accessing the elements
        # of an array with their indices is as efficient in Python (compared to
        # C/C++) as using an iterator.
        area = 0
        x0, y0 = x1, y1 = points[0]

        for x2, y2 in points[1:]:
            area += (x1 + x2) * (y1 - y2)  # Faster than `x1 * y2 - y1 * x2` (2 multiplications)
            x1, y1 = x2, y2

        area += (x2 + x0) * (y2 - y0)

        return abs(area) / 2

    @staticmethod
    def __calculate_relative_difference(i, j):
        """
        Calculate the relative difference between two numbers.

        The function takes the absolute difference divided by the absolute
        value of their arithmetic mean.


        :param i: A number.

        :param j: Another number.


        :return: A float representing the relative difference (a ratio) between
            the two numbers passed to this function.
        """
        return 0 if i + j == 0 else abs(i - j) / abs(i + j) * 2

    @staticmethod
    def __calculate_vectors_angle(vector1, vector2):
        """
        Calculate the angle between two vectors.


        :param vector1: A `Sprite` object.

        :param vector2: Another `Sprite` object.


        :return: The angle in degrees counter clockwise o between the two vectors.


        :raise ValueError: If the two vectors are parallel.
        """
        x1, y1 = vector1
        x2, y2 = vector2

        vector_dot_product = float(x1 * x2 + y1 * y2)

        vector1_magnitude = math.sqrt(x1 ** 2 + y1 ** 2)
        vector2_magnitude = math.sqrt(x2 ** 2 + y2 ** 2)

        denominator = vector1_magnitude * vector2_magnitude
        if denominator == 0:
            raise ValueError("the two vectors are parallel")

        cosinus_angle = vector_dot_product / denominator

        # @patch: Python floating point imprecision, e.g., -1.0000000000000002
        angle = math.acos(max(min(1.0, cosinus_angle), -1.0))

        # Determine the sign of the angle between the two vectors using the
        # z-component of the cross-product of the two vectors.
        vector_cross_product_z_component = x1 * y2 - y1 * x2
        if vector_cross_product_z_component < 0:
            angle = -angle

        return math.degrees(angle)

    @classmethod
    def __calculate_vectors_angles(cls, vectors):
        """
        Calculate the angle of consecutive vectors.

        :param vectors: A list of vectors defined by their respective
            coordinates `(x, y)`.


        :return: A list of angles in degrees counter clockwise between each 2
            consecutive vectors pair.
        """
        return [
            cls.__calculate_vectors_angle(vectors[i], vectors[i + 1])
            for i in range(len(vectors) - 1)
        ]

    @classmethod
    def __detect_eyelid_opening_state(
            cls,
            eye,
            eyebrow,
            eyelid_too_closed_threshold=0.16,
            eyelid_too_open_threshold=0.55):
        """
        Detect the eyelid opening state of an eye.


        The function uses a heuristic for detecting if eyelids are widely open,
        normally open, narrowed, or closed, based on the following features of
        the face:

        - the topmost position of the eyebrow (EB)
        - the topmost position of the upper eyelid (UEL)
        - the bottommost position of the lower eyelid (LEL)

        The function calculates the distance D1 between EB and UEL, and the
        distance D2 between EB and LEL.

        The function calculates the relative difference R between the distances
        D1 and D2.

        - If the relative difference R is low, it means that the upper eyelid
          is far from the eyebrow and close to the lower eyelid: the eyelids
          are probably narrowed or closed;

        - If the relative difference R is high, it means that the upper eyelid
          is close from the eyebrow and far to the lower eyelid: the eyelids
          are probably widely open;

        - If the relative difference R is medium, it means that the upper
          eyelid is almost midway between the eyebrow and the lower eyelid: the
          eyelids are probably normally open;


        :param eye: A list of 2D points composing the upper and lower eyelids.

        :param eyebrow: A list of 2D points composing the eyebrow above the
            eyelids.

        :param eyelid_too_closed_threshold: The minimum relative difference R.

        :param eyelid_too_open_threshold: The maximum relative difference R.


        :return: An item of the enumeration `EyelidOpeningState`.
        """
        # Determine the 2D points representing:
        # - the topmost position of the eyebrow (EB)
        # - the topmost position of the upper eyelid (UEL)
        # - the bottommost position of the lower eyelid (LEL)
        eyebrow_topmost_position = min([y for x, y in eyebrow])
        upper_eyelid_topmost_position = min([y for x, y in eye])
        lower_eyelid_bottommost_position = max([y for x, y in eye])

        # Calculate the distance D1 between EB and UEL, and the distance D2
        # between EB and LEL.
        upper_eyelid_eyebrow_distance = upper_eyelid_topmost_position - eyebrow_topmost_position
        lower_eyelid_eyebrow_distance = lower_eyelid_bottommost_position - eyebrow_topmost_position

        # Calculate the relative difference between these distances D1 and D2.
        eye_eyebrow_relative_distance = cls.__calculate_relative_difference(
            upper_eyelid_eyebrow_distance,
            lower_eyelid_eyebrow_distance)

        if eye_eyebrow_relative_distance < eyelid_too_closed_threshold:
            return EyelidOpeningState.narrowed_or_closed
        elif eye_eyebrow_relative_distance > eyelid_too_open_threshold:
            return EyelidOpeningState.widely_open
        else:
            return EyelidOpeningState.normally_open

    @staticmethod
    def __detect_face_features(image):
        """
        Detect the feature of a face


        :param image: A `numpy` array representing the image to detect face
            features.


        :return: A dictionary of found face feature locations where the key
            corresponds to an item of the enumeration `FaceFeature`, and the
            value corresponds to a list of tuple `(x, y)` representing a point
            of the face feature.


        :raise MultipleFacesDetectedException: If more than one face have been
            detected.
        """
        # Get a dictionary of face features, such as eyes, nose, etc., for each
        # face in the image.
        faces_features = face_recognition.face_landmarks(image)

        if len(faces_features) == 0:
            raise NoFaceDetectedException("no face has been detected in the photo")
        elif len(faces_features) > 1:
            raise MultipleFacesDetectedException(
                "a biometric photo passport MUST only have one face",
                payload={'face_count', len(faces_features)})

        return {
            cast.string_to_enum(key, FaceFeature): value
            for key, value in faces_features[0].items()
        }

    def __init__(
            self,
            image,
            forbid_oblique_face=True,
            forbid_open_mouth=True,
            forbid_closed_eye=True,
            forbid_unevenly_open_eye=True):
        """
        Build an object `BiometricPassportPhoto` from an image.


        :param image: An object `PIL.Image`.

        :param forbid_oblique_face: Indicate whehter to check if the face is
            oblique.

        :param forbid_open_mouth: Indicate whether to check if the mouth is
            closed with no smile.

        :param forbid_closed_eye: Indicate whether to check if one or two eyes
            are closed.

        :param forbid_unevenly_open_eye: Indicate whether to check if the 2
            eyelids are evenly open (same area of the visible part of the eyes).


        :raise BiometricPassportPhotoException: if the photo doesn't comply
            with the requirements for a biometric passport photo.

        :raise ValueError: If the argument `image` is not an object `PIL.Image`.
        """
        if not isinstance(image, Image.Image):
            raise ValueError("invalid argument 'image'")

        image_array = numpy.array(image)
        face_features = self.__detect_face_features(image_array)

        self.__assert_front_full_face(face_features, forbid_oblique_face=forbid_oblique_face)

        if forbid_open_mouth:
            self.__assert_mouth_closed_with_no_smile(face_features)

        if forbid_closed_eye:
            self.__assert_opened_eyes(face_features, forbid_unevenly_open_eye=forbid_unevenly_open_eye)

        self.__image = image
        self.__face_features = face_features
        self.__face_angle = self.__calculate_face_angle(face_features)
        self.__face_center = self.__get_face_center(face_features)

    @staticmethod
    def __get_face_center(face_features):
        """
        Determine the center of a face.


        :param face_features: A dictionary of found face feature locations
            where the key corresponds to an item of the enumeration
            `FaceFeature`, and the value corresponds to a list of tuple
            `(x, y)` representing a point of the face feature.


        :return: A tuple `(x, y)` corresponding the coordinates of the point
            at the center of the face.
        """
        chin = face_features[FaceFeature.chin]
        left_ear_top_x, left_ear_top_y = chin[0]
        right_ear_top_x, right_ear_top_y = chin[-1]

        face_center_x = round((left_ear_top_x + right_ear_top_x) / 2)
        face_center_y = round((left_ear_top_y + right_ear_top_y) / 2)
        return face_center_x, face_center_y

    @classmethod
    def __split_line_by_angle(cls, points, maximum_angle):
        """
        Split a line in sub-lines depending when the angle between two
        consecutive segments of this line is over the specified angle.

        For example, given a line composed of points [P0, P1, P2, P3]

            P0
            o           o P3
             \          |
              \         |
               \ 135°   | 90°
             P1 o-------o P2

        Provided an angle `100` degrees, the function splits the line in 2
        sub-lines: [P0, P1], [P1, P2, P3].


        :param points: A list of 2D points `(x, y)` forming a closed line
            segment.

        :param maximum_angle: A positive decimal value representing the angle
            between two consecutive vectors
            of the close line segment to split these 2 vectors in 2 sets.


        :return: a list of lines, each line corresponding to a list of 2D
            points.


        :raise ValueError: If the given list has less than 3 points.
        """
        if len(points) < 3:
            raise ValueError('the list must contain 3 or more points')

        vectors = cls.__build_vectors(points)
        vectors_angles = cls.__calculate_vectors_angles(vectors)

        l = []
        i = 0
        for j, angle in enumerate(vectors_angles, start=1):
            if abs(angle) >= maximum_angle:
                l.append(points[i:j + 1])
                i = j + 1

        l.append(points[i:len(points)])
        return l

    def build_image(
            self,
            size,
            horizontal_padding=DEFAULT_HORIZONTAL_PADDING,
            vertical_padding=DEFAULT_VERTICAL_PADDING):
        """
        Build a new image containing the face that has been detected.


        :param size: The requested size in pixels, as a 2-tuple `(width, height)`.

        :param horizontal_padding: Space in pixels to add on the left and the
            right of the detected face.

        :param vertical_padding: Space in pixels to add on the top and the
            bottom of the detected face.


        :return: An object `PIL.Image`.
        """
        image_width, image_height = size
        image_aspect_ratio = image_width / image_height

        chin = self.__face_features[FaceFeature.chin]
        transformed_chin = [
            TransformedPoint2D(x, y, angle=self.__face_angle, origin=self.__face_center)
            for x, y in chin
        ]

        head_bottom_y = max([point.y for point in transformed_chin])

        left_ear_top = transformed_chin[0]
        right_ear_top = transformed_chin[-1]

        head_center_y = round((left_ear_top.y + right_ear_top.y) / 2)
        head_top_y = head_center_y - (head_bottom_y - head_center_y)

        head_width = right_ear_top.x - left_ear_top.x + 1
        head_height = head_bottom_y - head_top_y + 1

        vertical_padding = round(head_width * vertical_padding)
        horizontal_padding = round(head_height * horizontal_padding)

        frame_left = left_ear_top.x - horizontal_padding
        frame_top = head_top_y - vertical_padding
        frame_right = right_ear_top.x + horizontal_padding
        frame_bottom = head_bottom_y + vertical_padding
        frame_width = frame_right - frame_left + 1
        frame_height = frame_bottom - frame_top + 1

        frame_aspect_ratio = frame_width / frame_height

        if frame_aspect_ratio < image_aspect_ratio:
            frame_extended_width = image_aspect_ratio * frame_height
            frame_left -= round((frame_extended_width - frame_width) / 2)
            frame_right += round((frame_extended_width - frame_width) / 2)  # + 1 if necessary
        else:
            frame_extended_height = frame_width / image_aspect_ratio
            frame_top -= round((frame_extended_height - frame_height) / 2)
            frame_bottom += round((frame_extended_height - frame_height) / 2)  # + 1 if necessary

        _width = frame_right - frame_left + 1
        _height = frame_bottom - frame_top + 1

        transformed_image = self.__image \
            .rotate(
                angle=math.degrees(self.__face_angle),
                center=self.__face_center,
                fillcolor=DEFAULT_FILL_COLOR) \
            .crop((frame_left, frame_top, frame_right, frame_bottom)) \
            .resize(size)

        return transformed_image

    def debug_face_features(self):
        """
        Return an image with the outline of the polygons representing the
        features of the face.


        :return: An image where the face features have been drawn on.
        """
        image = self.__image.copy()
        draw = ImageDraw.Draw(image)

        for face_feature, points in self.__face_features.items():
            color = DEFAULT_FACE_FEATURE_COLORS[face_feature]
            draw.line(points, fill=color, width=2)
            draw.line([points[-1], points[0]], fill=color, width=2)

        return image

    @classmethod
    def from_file(
            cls,
            image_file_path_name,
            forbid_oblique_face=True,
            forbid_open_mouth=True,
            forbid_closed_eye=True,
            forbid_unevenly_open_eye=True):
        """
        Return an object `BiometricPassportPhoto` from the specified image
        file.


        :param image_file_path_name: Absolute path and name of an image file.
             Only 'RGB' (8-bit RGB, 3 channels) and ‘L’ (black and white) are
             currently supported (cf. Python library Face Recognition 1.2.2).

        :param forbid_oblique_face: Indicate whether to check whether the face
            is oblique.

        :param forbid_open_mouth: Indicate whether to check if the mouth is
            closed with no smile.

        :param forbid_closed_eye: Indicate whether to check if one or two eyes
            are closed.

        :param forbid_unevenly_open_eye: Indicate whether to check if the 2
            eyelids are evenly open (same area of the visible part of the eyes).


        :return: An object `BiometricPhotoPassport`.
        """
        image = load_image_and_correct_orientation(image_file_path_name)

        return BiometricPassportPhoto(
            image,
            forbid_oblique_face=forbid_oblique_face,
            forbid_open_mouth=forbid_open_mouth,
            forbid_closed_eye=forbid_closed_eye,
            forbid_unevenly_open_eye=forbid_unevenly_open_eye)


def get_console_handler(logging_formatter=LOGGING_FORMATTER):
    """
    Return a logging handler that sends logging output to the system's
    standard output.


    :param logging_formatter: An object `Formatter` to set for this handler.


    :return: An instance of the `StreamHandler` class.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging_formatter)
    return console_handler


def load_image_and_correct_orientation(file_path_name):
    """
    Load an image generated by a digital device (e.g., camera, smartphone,
    scanner, etc.) and correct its orientation when needed.

    The function reads the Exif tag indicating the orientation of the
    digital device relative to the captured scene, and transpose the image
    accordingly.


    :param file_path_name: The path and name of an image file.


    :return: An object `PIL.Image` of the photo which orientation may have
        been corrected.
    """
    image = Image.open(file_path_name)

    # Process the Exif chunk of the image.
    with open(file_path_name, 'rb') as fd:
        exif_tags = exifread.process_file(fd)

    # Apply the transposition corresponding to the Exif values of the
    # orientation tag of this image.
    exif_tag_orientation = exif_tags.get(EXIF_TAG_ORIENTATION)
    if exif_tag_orientation and exif_tag_orientation.values:
        transpositions = [
            transposition
            for value in exif_tag_orientation.values
            for transposition in EXIF_PIL_TRANSPOSITIONS[value]]

        for transposition in transpositions:
            image = image.transpose(transposition)

    return image


def main():
    arguments = parse_arguments()
    setup_logger()

    image_file_path_name = os.path.abspath(os.path.expanduser(arguments.file_path_name))
    image_size_str = arguments.image_size
    image_width, image_height = image_size_str.split('x')
    image_size = int(image_width), int(image_height)

    biometric_photo_passport = BiometricPassportPhoto.from_file(
        image_file_path_name,
        forbid_oblique_face=not arguments.allow_oblique_face,
        forbid_open_mouth=not arguments.allow_open_mouth,
        forbid_unevenly_open_eye=not arguments.allow_unevenly_open_eye)

    if arguments.debug:
        biometric_photo_passport \
            .debug_face_features() \
            .save(f'{image_file_path_name}.debug.jpg')

    biometric_photo_passport \
        .build_image(image_size)\
        .save(f'{image_file_path_name}.bpp.jpg')


def parse_arguments():
    """
    Convert argument strings to objects and assign them as attributes of
    the namespace.


    @return: an instance `Namespace` corresponding to the populated
        namespace.
    """
    parser = argparse.ArgumentParser(description='Biometric Passport Photo Magick')

    parser.add_argument(
        '-f', '--file',
        dest='file_path_name',
        metavar='FILE',
        required=True,
        help="specify the absolute path and name of the image file to produce a biometric passport photo")

    parser.add_argument(
        '-s', '--size',
        dest='image_size',
        metavar='GEOMETRY',
        required=True,
        help="specify the width and height of the image to build")

    parser.add_argument(
        '--allow-oblique-face',
        dest='allow_oblique_face',
        action='store_true',
        required=False,
        default=False,
        help="indicate whether to check whether the face is oblique")

    parser.add_argument(
        '--allow-open-mouth',
        dest='allow_open_mouth',
        action='store_true',
        required=False,
        default=False,
        help="indicate whether to allow face with open mouth")

    parser.add_argument(
        '--allow-unevenly-open-eye',
        dest='allow_unevenly_open_eye',
        action='store_true',
        required=False,
        default=False,
        help="indicate whether to allow face with the 2 eyelids not evenly open")

    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        required=False,
        default=False,
        help="indicate whether to generate an image with face feature outlines")

    return parser.parse_args()


def setup_logger(
        logging_formatter=LOGGING_FORMATTER,
        logging_level=logging.INFO,
        logger_name=None):
    """
    Setup a logging handler that sends logging output to the system's
    standard output.


    :param logging_formatter: An object `Formatter` to set for this handler.

    :param logger_name: Name of the logger to add the logging handler to.
        If `logger_name` is `None`, the function attaches the logging
        handler to the root logger of the hierarchy.

    :param logging_level: The threshold for the logger to `level`.  Logging
        messages which are less severe than `level` will be ignored;
        logging messages which have severity level or higher will be
        emitted by whichever handler or handlers service this logger,
        unless a handler’s level has been set to a higher severity level
        than `level`.


    :return: An object `Logger`.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    logger.addHandler(get_console_handler(logging_formatter=logging_formatter))
    logger.propagate = False
    return logger


def test():
    setup_logger(logging_level=logging.INFO)

    samples_path = os.path.abspath(
        os.path.join(
            os.path.os.path.dirname(__file__),
            os.pardir,
            'samples'))

    image_file_path_names = [
        os.path.join(samples_path, file_name)
        for file_name in os.listdir(samples_path)
        if os.path.isfile(os.path.join(samples_path, file_name))]

    for image_file_path_name in image_file_path_names:
        try:
            print(image_file_path_name)
            biometric_photo_passport = BiometricPassportPhoto.from_file(
                image_file_path_name,
                forbid_oblique_face=False,
                forbid_open_mouth=False,
                forbid_closed_eye=False,
                forbid_unevenly_open_eye=False)

            biometric_photo_passport.build_image((400, 400)).save(f'{image_file_path_name}_bpp.jpg')
        except BiometricPassportPhotoException as exception:
            logging.warning(f"The processing of the file {image_file_path_name} raised the following exception:")
            logging.warning(f"\t{str(exception)}")
        except (UnidentifiedImageError, FileNotFoundError) as exception:
            pass


if __name__ == '__main__':
    main()
