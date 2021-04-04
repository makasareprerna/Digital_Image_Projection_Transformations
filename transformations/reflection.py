import numpy as np


class reflection:

    def reflectX(self, image):
        img = image
        r, c = img.shape
        refimg1 = np.empty((r, c), dtype=np.uint8)
        for a in range(0, r):
            for b in range(0, c):
                refimg1[a, c - b - 1] = img[a, b]  # Right Axis
        return refimg1

    def reflectY(self, image):
        img = image
        r, c = img.shape
        refimg2 = np.empty((r, c), dtype=np.uint8)
        for a in range(0, r):
            for b in range(0, c):
                refimg2[r - a - 1, b] = img[a, b]  # Bottom Axis
        return refimg2
