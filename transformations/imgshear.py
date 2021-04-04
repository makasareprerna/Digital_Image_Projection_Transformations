import math as m
import numpy as np


class imgshear:

    # shears the image horizontally
    def horizontalShear(self, img, shearFactor):
        imgRows, imgCols = img.shape
        paddedImage = self.padImageForHorizontal(img, shearFactor)
        padImgRows, padImgCols = paddedImage.shape
        shearedImage = np.zeros((padImgRows, padImgCols), np.uint8)
        for row in range(padImgRows):
            for col in range(padImgCols):
                x = row
                y = col + m.floor(row*shearFactor)
                if (x < padImgRows and y < padImgCols):
                    shearedImage[row, col] = paddedImage[x, y]

        return shearedImage

    # Pads the image with black pixels in the right for horizontal shear
    def padImageForHorizontal(self, img, shearFactor):
        imgRows, imgColumns = img.shape
        rowPadding = 0
        columnPadding = m.ceil(shearFactor*imgColumns)
        newRowsSize = imgRows + rowPadding
        newColumnSize = imgColumns + columnPadding
        paddedImage = np.zeros((newRowsSize, newColumnSize), np.uint8)
        paddedImage[rowPadding:newRowsSize, columnPadding:newColumnSize] = img
        return paddedImage

    # shears the image vertically
    def verticalShear(self, img, shearFactor):
        imgRows, imgCols = img.shape
        paddedImage = self.padImageForVertical(img, shearFactor)
        padImgRows, padImgCols = paddedImage.shape
        shearedImage = np.zeros((padImgRows, padImgCols), np.uint8)
        for row in range(padImgRows):
            for col in range(padImgCols):
                x = row + m.floor(col*shearFactor)
                y = col
                if (x < padImgRows and y < padImgCols):
                    shearedImage[row, col] = paddedImage[x, y]

        return shearedImage

    def padImageForVertical(self, img, shearFactor):
        imgRows, imgColumns = img.shape
        rowPadding = m.ceil(shearFactor*imgRows)
        columnPadding = 0
        newRowsSize = imgRows + rowPadding
        newColumnSize = imgColumns + columnPadding
        paddedImage = np.zeros((newRowsSize, newColumnSize), np.uint8)
        paddedImage[rowPadding:newRowsSize, columnPadding:newColumnSize] = img
        return paddedImage
