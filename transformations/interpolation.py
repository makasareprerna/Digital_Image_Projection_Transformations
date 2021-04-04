import numpy as np


class interpolation:

    def linear_interpolation(self, pt1, pt2, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2
        take as input
        pt1: known point pt1 and f(pt1) or intensity value
        pt2: known point pt2 and f(pt2) or intensity value
        unknown: take and unknown location
        return the f(unknown) or intentity at unknown"""

        x1 = pt1[0]
        y1 = pt1[1]
        i1 = pt1[2]
        y2 = pt2[1]
        i2 = pt2[2]
        y = unknown[1]
        if y2 > y1:
            intensity = int(((float(y2-y) / float(y2-y1)) * i2) +
                            ((float(y-y1) / float(y2-y1)) * i1))
        else:
            intensity = int((float(y2 - y) * i2) + (float(y - y1) * i1))

        return x1, y, intensity

    def linear_interpolation_row(self, pt1, pt2, unknown):
        x1 = pt1[0]
        x2 = pt2[0]
        i1 = pt1[2]
        i2 = pt2[2]
        x = unknown[0]
        if x2 > x1:
            intensity = int(((float(x2 - x) / float(x2 - x1)) * i2) +
                            ((float(x - x1) / float(x2 - x1)) * i1))
        else:
            intensity = int((float(x2 - x) * i2) + (float(x - x1) * i1))

        return intensity

    def bilinear_interpolation(self, pt1, pt2, pt3, pt4, unknown):
        """Computes the linear interpolation for the unknown values using pt1 and pt2
        take as input
        pt1: known point pt1 and f(pt1) or intensity value
        pt2: known point pt2 and f(pt2) or intensity value
        pt1: known point pt3 and f(pt3) or intensity value
        pt2: known point pt4 and f(pt4) or intensity value
        unknown: take and unknown location
        return the f(unknown) or intentity at unknown"""

        p5 = self.linear_interpolation(pt1, pt2, unknown)
        p6 = self.linear_interpolation(pt3, pt4, unknown)
        i = np.abs(self.linear_interpolation_row(p5, p6, unknown))
        return i
