import numpy as np
import math as m


class scaling:

    def nearestNeighbor(self, image, fx, fy):
        # Processing the size of the original and new image to be formed
        originalImageRows, originalImageColumns = image.shape
        newImageRows = round(originalImageRows*fx)
        newImageColumns = round(originalImageColumns*fy)

        # new Image with just zeros
        newImage = np.zeros((newImageRows, newImageColumns), np.uint8)

        # Scaling the newImage pixel's according to match the oldImage pixel values
        for newImageIndexRow in range(newImageRows):
            for newImageIndexColumn in range(newImageColumns):
                oldX = newImageIndexRow/fx
                oldY = newImageIndexColumn/fy
                oldX = m.floor(oldX)
                oldY = m.floor(oldY)
                newImage[newImageIndexRow, newImageIndexColumn] = image[oldX, oldY]

        return newImage

    def bicubicscaling(self, img, fx, fy):
        A = -0.75
        imgRows, imgCols = img.shape
        paddedImage = self.addBorders(img)
        paddedImgRows, paddedImgCols = paddedImage.shape
        scaledImgRows = round(imgRows*fx)
        scaledImgCols = round(imgCols*fy)

        # new image -- scaled (all black for now)
        scaledImg = np.zeros((scaledImgRows, scaledImgCols), np.uint8)

        for row in range(scaledImgRows):
            for col in range(scaledImgCols):
                oldX = ((row+0.5)*fx - 0.5)
                sx = m.floor(oldX)
                oldX -= sx

                oldY = ((col+0.5)*fy - 0.5)
                sy = m.floor(oldY)
                oldY -= sy
                print(oldX, oldY)
                print(" ")
                # print(oldX, oldY)
                # oldX = m.floor(row/fx)
                # oldY = m.floor(col/fy)
                coeffsAlongX = self.findCoeff(oldX, A)
                # print(coeffsAlongX)
                coeffsAlongY = self.findCoeff(oldY, A)
                interpolatedArray = self.cubic16Neighbors(oldX, oldY, paddedImage, coeffsAlongX)
                # print(interpolatedArray)
                # print(oldX, oldY)
                sum = self.multiply(coeffsAlongY, interpolatedArray)
                scaledImg[row, col] = round(sum)

        return scaledImg

    def multiply(self, coeffsAlongY, interpolatedArray):
        sum = 0
        for i in range(len(coeffsAlongY)):
            # print(interpolatedArray[i], end="*")
            # print(coeffsAlongY[i], end="*")
            # print(interpolatedArray[i], end="    ")
            x = coeffsAlongY[i]*interpolatedArray[i]
            sum = sum + x
        # print(sum)
        # print("\n\n")
        return sum

    def cubic16Neighbors(self, oldX, oldY, paddedImage, coeffs):
        oldX = round(oldX)
        oldY = round(oldY)
        interpolated = 0
        interpolatedArray = []
        for i in range(4):
            interpolated = 0
            for j in range(4):
                interpolated += paddedImage[oldX+i, oldY+j]*coeffs[j]
                # print(interpolated)
                # print(paddedImage[oldX+i, oldY+j], end="*")
                # print(coeffs[j], end=" ")
                # print("")
            interpolatedArray.append(interpolated)
        return interpolatedArray

    def findCoeff(self, oldX, A):
        coeff = []
        coeff.append(((A*(oldX + 1) - 5*A)*(oldX + 1) + 8*A)*(oldX + 1) - 4*A)
        coeff.append(((A + 2)*oldX - (A + 3))*oldX*oldX + 1)
        coeff.append(((A + 2)*(1 - oldX) - (A + 3))*(1 - oldX)*(1 - oldX) + 1)
        coeff.append(1 - coeff[0] - coeff[1] - coeff[2])
        return coeff

    def addBorders(self, img):
        imgRows, imgCols = img.shape
        rowPadding = 4  # because bi-cubic takes 16 neighboring pixels
        colPadding = 4  # because bi-cubic takes 16 neighboring pixels
        paddedImage = np.zeros((imgRows+rowPadding,
                                imgCols+colPadding), np.uint8)
        paddedImage[m.ceil(rowPadding/2): m.ceil((rowPadding/2)+imgRows),
                    m.ceil(colPadding/2): m.ceil((colPadding/2)+imgCols)] = img
        paddedImgRows, paddedImgCols = paddedImage.shape
        # adding border in the x direction (top)
        paddedImage[1:2, :] = paddedImage[2:3, :]
        paddedImage[0:1, :] = paddedImage[2:3, :]

        # adding border in the x direction (bottom)
        paddedImage[paddedImgRows-2: paddedImgRows-1, :] = paddedImage[
            paddedImgRows-3: paddedImgRows-2, :]
        paddedImage[paddedImgRows-1: paddedImgRows, :] = paddedImage[
            paddedImgRows-3: paddedImgRows-2, :]

        # adding borders in the y direction (left)
        paddedImage[:, 1:2] = paddedImage[:, 2:3]
        paddedImage[:, 0:1] = paddedImage[:, 2:3]

        # adding borders in the y direction (right)
        paddedImage[:, paddedImgCols-2:paddedImgCols - 1] = paddedImage[
            :, paddedImgCols-3:paddedImgCols-2]
        paddedImage[:, paddedImgCols-1:paddedImgCols] = paddedImage[
            :, paddedImgCols-3:paddedImgCols-2]

        return paddedImage


# Reference
"""https://theailearner.com/2018/12/29/image-processing-bicubic-interpolation/"""
