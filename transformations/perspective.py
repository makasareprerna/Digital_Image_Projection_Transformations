# --image img/example_01.png --coords "[(73, 239), (356, 117), (475, 265), (187, 443)]"
# --image img/example_02.png --coords "[(101, 185), (393, 151), (479, 323), (187, 441)]"
# --image img/example_03.png --coords "[(63, 242), (291, 110), (361, 252), (78, 386)]"

import numpy as np
import cv2


class perspective:
    def order_points(self, points):
        #points = np.asarray([(3,1),(1,1),(3,5),(1,5)])
        rectangle = np.zeros((4, 2), dtype="float32")

        aggregate = points.sum(axis=1)
        rectangle[0] = points[np.argmin(aggregate)]
        rectangle[2] = points[np.argmax(aggregate)]

        difference = np.diff(points, axis=1)
        rectangle[1] = points[np.argmin(difference)]
        rectangle[3] = points[np.argmax(difference)]
        print(rectangle)
        return rectangle

    def perspective_transform(self, image, points):
        points = np.asarray(points)
        rectangle = self.order_points(points)
        (top_left, top_right, bottom_right, bottom_left) = rectangle

        first_width = np.sqrt(((bottom_right[0] - bottom_left[0]) **2) + 
                              ((bottom_right[1] - bottom_left[1]) ** 2))
        second_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) +
                               ((top_right[1] - top_left[1]) ** 2))
        max_width = max(int(first_width), int(second_width))

        first_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) +
                               ((top_right[1] - bottom_right[1]) ** 2))
        second_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) +
                                ((top_left[1] - bottom_left[1]) ** 2))
        max_height = max(int(first_height), int(second_height))

        destination = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]], dtype="float32")

        matrix = cv2.getPerspectiveTransform(rectangle, destination)
        final_image = cv2.warpPerspective(image, matrix, (max_width, max_height))

        return final_image
