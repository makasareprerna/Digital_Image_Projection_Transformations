import numpy as np
import math as m


class translation:

    def translateImage(self, img, xOffSet, yOffSet):
        imgRows, imgCols = img.shape
        translatedImg = np.zeros((imgRows, imgCols), np.uint8)
        if xOffSet < imgRows and yOffSet < imgCols:
            for row in range(imgRows):
                for col in range(imgCols):
                    x = row + xOffSet
                    y = col + yOffSet
                    if x < imgRows and y < imgCols:
                        translatedImg[x, y] = img[row, col]
        else:
            print("offsets are out of bounds")

        return translatedImg
