import cv2
import numpy as np
import math as m

from transformations import imgshear, imgwarp, interpolation, reflection
from transformations import perspective, resample, rotation, scaling, translation


def main():
    testImageName = "img/Lenna.png"
    testImage = cv2.imread(testImageName, 0)
    displayImage("Lenna", testImage)
    rotateMyImage(testImage)
    translateMyImage(testImage)
    shearMyImage(testImage)
    reflectMyImage(testImage)
    perspectiveFunction(testImage)
    warpMyImage(testImage)
    print("THE END")


def rotateMyImage(testImage):
    print("ROTATION TRANSFORMATION\n")
    rotationObject = rotation.rotation()
    rotatedImage = rotationObject.rotate(testImage, m.pi/6)
    displayImage("rotated image", rotatedImage)


def warpMyImage(testImage):
    print("HORIZONTAL AND VERRTICAL WARPING\n")

    imgWarpObject = imgwarp.imgwarp()
    verticalWrappedImage = imgWarpObject.imgwarpv(testImage, 25)
    displayImage("Vertical warp", verticalWrappedImage)

    horizontalWrappedImage = imgWarpObject.imgwarph(testImage, 25)
    displayImage("horizontal warp", horizontalWrappedImage)


def shearMyImage(testImage):
    print("SHEARING IMAGE\n")
    shearingObject = imgshear.imgshear()
    shearedImageV = shearingObject.verticalShear(testImage, 0.7)
    shearedImageH = shearingObject.horizontalShear(testImage, 1)
    displayImage("Horizontal Shear", shearedImageH)
    displayImage("Vertical Shear", shearedImageV)


def translateMyImage(testImage):
    print("TRANSLATING IMAGE\n")
    translationObject = translation.translation()
    trImage = translationObject.translateImage(testImage, 100, 50)
    displayImage("Translated Image", trImage)


def reflectMyImage(testImage):
    print("REFLECTING IMAGE\n")
    displayImage("original image", testImage)
    reflectionObject = reflection.reflection()
    reflectedRightImage = reflectionObject.reflectX(testImage)
    displayImage("right reflected", reflectedRightImage)
    reflectedBottomImage = reflectionObject.reflectY(testImage)
    displayImage("bottom reflected", reflectedBottomImage)


def perspectiveFunction(testImage):
    print("PERSPECTIVE TRANSFORMATION \n")
    testImageName = "img/hello.png"
    testImage = cv2.imread(testImageName, 0)
    displayImage("Hello World", testImage)
    coords = "[(73, 239), (356, 117), (475, 265), (187, 443)]"
    pts = np.array(eval(coords), dtype="float32")
    perspectiveObj = perspective.perspective()
    transformedImage = perspectiveObj.perspective_transform(testImage, pts)
    displayImage("Perspective Transformation", transformedImage)


def scaleMyImage(testImage):
    print("SCALING IMAGE\n")
    scalingObject = scaling.scaling()
    bicubicScaled = scalingObject.bicubicscaling(testImage, 2, 2)
    print(bicubicScaled)


def displayImage(window_name, image):
    """A function to display image"""
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, image)
    cv2.waitKey(2000)


if __name__ == "__main__":
    main()
