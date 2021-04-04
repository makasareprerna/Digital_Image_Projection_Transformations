import numpy as np
import math as m


class rotation:

    def rotate(self, img, degrees):
        """
        Rotates image with x degrees
        @img: grayscale image to be rotated
        @degrees: angle by which the image needs to be rotated
        @returns: rotated image
        """
        paddedImage = self.padImage(img)
        imgRows, imgColumns = img.shape
        padImgRows, padImgColumns = paddedImage.shape
        originX = m.ceil(padImgRows/2 + 1)
        originY = m.ceil(padImgColumns/2 + 1)
        rotatedImg = np.zeros((padImgRows, padImgColumns), np.uint8)

        for row in range(padImgRows):
            for col in range(padImgColumns):
                x = (row-originX)*m.cos(degrees)+(col-originY)*m.sin(degrees)
                y = -(row-originX)*m.sin(degrees)+(col-originY)*m.cos(degrees)
                x = round(x)+originX
                y = round(y)+originY
                if (x >= 0 and y >= 0 and x < padImgColumns and y < padImgRows):
                    rotatedImg[row, col] = paddedImage[x, y]
        return rotatedImg

    def padImage(self, img):
        """
        Pad the image so that we can see the whole image
        @img: takes one argument, image to be padded
        @returns: padded image with black pixels
        """
        imgRows, imgColumns = img.shape
        diagnol = m.sqrt(imgRows*imgRows + imgColumns*imgColumns)
        rowPadding = m.ceil(diagnol - imgRows) + 2
        columnPadding = m.ceil(diagnol - imgColumns) + 2
        newRowsSize = imgRows + rowPadding
        newColumnSize = imgColumns + columnPadding
        paddedImage = np.zeros((newRowsSize, newColumnSize), np.uint8)
        paddedImage[m.ceil(rowPadding/2): m.ceil((rowPadding/2)+imgRows),
                    m.ceil(columnPadding/2): m.ceil((columnPadding/2) + imgColumns)] = img
        return paddedImage
