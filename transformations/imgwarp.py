import math as m
import numpy as np


class imgwarp:

    output = None

    def imgwarpv(self, img, amplitude):
        (row, col) = img.shape
        oimg = np.zeros(img.shape, dtype=img.dtype)
        for i in range(row):
            for j in range(col):
                distox = int(amplitude * m.sin(2 * m.pi * i / 180))
                if j+distox < row:
                    oimg[i, j] = img[i, (j+distox) % col]
                else:
                    oimg[i, j] = 0
        return oimg

    def imgwarph(self, img, amplitude):
        (row, col) = img.shape
        oimg = np.zeros(img.shape, dtype=img.dtype)
        for i in range(row):
            for j in range(col):
                distoy = int(amplitude * m.sin(2 * m.pi * j / 150))

                if i+distoy < row:
                    oimg[i, j] = img[(i+distoy) % row, j]
                else:
                    oimg[i, j] = 0
        return oimg

    def imgwarp(self, img, Xamplitude, Yamplitude):

        oimg = self.imgwarpv(img, Xamplitude)
        oimg = self.imgwarph(oimg, Yamplitude)

        """
        (row, col) = img.shape
        oimg = np.zeros(img.shape, dtype=img.dtype)
        for i in range(row):
            for j in range(col):

                distox = int(amplitude * m.sin(2 * m.pi * i / 150))
                distoy = int(amplitude * m.sin(2 * m.pi * j / 150))

                if i+distoy < row and j+distox < col:
                    oimg[i, j] = img[(i+distoy) % row, (j+distox) % col]
                else:
                    oimg[i, j] = 0
        """
        return oimg
