import numpy as np
import math


class resample:
    def resize(self, image, fx=None, fy=None, interpolation=None):
        """calls the appropriate funciton to resample an image based on the interpolation method
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        interpolation: method used for interpolation ('either bilinear or nearest_neighbor)
        returns a resized image based on the interpolation method
        """
        if interpolation == 'bilinear':
            return self.bilinear_interpolation(image, float(fx), float(fy))

        elif interpolation == 'nearest_neighbor':
            return self.nearest_neighbor(image, float(fx), float(fy))

        elif interpolation == 'bicubic':
            return self.bicubic_interpolation(image, float(fx), float(fy))

        elif interpolation == 'lanczos':
            return self.lanczos_interpolation(image, float(fx), float(fy))

    def nearest_neighbor(self, image, fx, fy):
        """resizes an image using nearest neighbor approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the nearest neighbor interpolation method
        """

        x = image.shape[0]
        y = image.shape[1]
        new_x = fx*x
        new_y = fy*y
        r_ratio = new_x/x
        c_ratio = new_y/y
        new_x = int(new_x)
        new_y = int(new_y)
        new_image = np.zeros([new_x, new_y])
        nearest_row = np.array(range(x))
        nearest_col = np.array(range(y))

        nearest_row = nearest_row*r_ratio
        nearest_col = nearest_col*c_ratio

        nearest_row = np.ceil(nearest_row)
        nearest_col = np.ceil(nearest_col)

        for i in range(new_x):
            for j in range(new_y):
                xi = np.abs(nearest_row-i).argmin()
                yi = np.abs(nearest_col-j).argmin()
                new_image[i, j] = image[xi, yi]

        return new_image

    def bilinear_interpolation(self, image, fx, fy):
        """resizes an image using bilinear interpolation approximation for resampling
        image: the image to be resampled
        fx: scale along x direction (eg. 0.5, 1.5, 2.5)
        fx: scale along y direction (eg. 0.5, 1.5, 2.5)
        returns a resized image based on the bilinear interpolation method

        Note: Do not write the code to perfrom interpolation between points in this file.
        There is a file named interpolation.py, and two function definitions are provided
        linear_interpolation: Write your code to perform linear interpolation between two in this function
        bilinear_interpolation: Write your code to perfrom bilinear interpolation using four points in this functions.
                                As bilinear interpolation essentially does linear interpolation three times, you coould simply call the
                                linear_interpolation function three times, with the correct parameters.
        """

        x = image.shape[0]
        y = image.shape[1]
        new_x = fx * x
        new_y = fy * y
        r_ratio = new_x / x
        c_ratio = new_y / y
        new_x = int(new_x)
        new_y = int(new_y)
        new_image = np.zeros([new_x, new_y])
        nearest_row = np.array(range(x))
        nearest_col = np.array(range(y))

        nearest_row = nearest_row * r_ratio
        nearest_col = nearest_col * c_ratio

        nearest_row = np.ceil(nearest_row)
        nearest_col = np.ceil(nearest_col)

        interpolate = interpolation.interpolation()
        for i in range(new_x):
            for j in range(new_y):
                xi = np.abs(nearest_row - i).argmin()
                yi = np.abs(nearest_col - j).argmin()
                p1 = [xi, yi, image[xi, yi]]
                p2 = [xi, yi+1, image[xi, yi]]
                p3 = [xi+1, yi, image[xi, yi]]
                p4 = [xi+1, yi+1, image[xi, yi]]
                unknown = [i, j]
                new_image[i, j] = interpolate.bilinear_interpolation(p1, p2, p3, p4, unknown)

        return new_image

    def bicubic_interpolation(self, image, fx, fy):
        a = -1/2
        x = image.shape[0]
        y = image.shape[1]

        def f(s, a):
            if (abs(s) >= 0) & (abs(s) <= 1):
                return (a + 2) * (abs(s) ** 3) - (a + 3) * (abs(s) ** 2) + 1
            elif (abs(s) > 1) & (abs(s) <= 2):
                return a * (abs(s) ** 3) - (5 * a) * (abs(s) ** 2) + (8 * a) * abs(s) - 4 * a
            return 0
        new_x = fx * x
        new_y = fy * y
        r_ratio = new_x / x
        c_ratio = new_y / y
        new_x = int(new_x)
        new_y = int(new_y)
        new_image = np.zeros([new_x, new_y])
        nearest_row = np.array(range(x))
        nearest_col = np.array(range(y))

        nearest_row = nearest_row * r_ratio
        nearest_col = nearest_col * c_ratio

        nearest_row = np.ceil(nearest_row)
        nearest_col = np.ceil(nearest_col)

        for i in range(new_x):
            for j in range(new_y):
                xi = np.abs(nearest_row - i).argmin()
                yi = np.abs(nearest_col - j).argmin()
                p1 = image[xi, yi]
                if 0 <= yi < y - 1:
                    p2 = image[xi, yi+1]
                else:
                    p2 = 0
                if 0 <= yi < y - 2:
                    p3 = image[xi, yi+2]
                else:
                    p3 = 0
                if 0 <= yi < y - 3:
                    p4 = image[xi, yi+3]
                else:
                    p4 = 0

                if 0 <= yi < y and 0 <= xi < x - 1:
                    p5 = image[xi+1, yi]
                else:
                    p5 = 0
                if 0 <= yi < y - 1 and 0 <= xi < x - 1:
                    p6 = image[xi+1, yi+1]
                else:
                    p6 = 0
                if 0 <= yi < y - 2 and 0 <= xi < x - 1:
                    p7 = image[xi+1, yi+2]
                else:
                    p7 = 0
                if 0 <= yi < y - 3 and 0 <= xi < x - 1:
                    p8 = image[xi+1, yi+3]
                else:
                    p8 = 0

                if 0 <= yi < y and 0 <= xi < x - 2:
                    p9 = image[xi+2, yi]
                else:
                    p9 = 0
                if 0 <= yi < y-1 and 0 <= xi < x - 2:
                    p10 = image[xi+2, yi+1]
                else:
                    p10 = 0
                if 0 <= yi < y-2 and 0 <= xi < x - 2:
                    p11 = image[xi+2, yi+2]
                else:
                    p11 = 0
                if 0 <= yi < y-3 and 0 <= xi < x - 2:
                    p12 = image[xi+2, yi+3]
                else:
                    p12 = 0

                if 0 <= yi < y and 0 <= xi < x - 3:
                    p13 = image[xi+3, yi]
                else:
                    p13 = 0
                if 0 <= yi < y-1 and 0 <= xi < x - 3:
                    p14 = image[xi+3, yi+1]
                else:
                    p14 = 0
                if 0 <= yi < y-2 and 0 <= xi < x - 3:
                    p15 = image[xi+3, yi+2]
                else:
                    p15 = 0
                if 0 <= yi < y-3 and 0 <= xi < x - 3:
                    p16 = image[xi+3, yi+3]
                else:
                    p16 = 0

                lhs = np.matrix([[f(xi-xi, a), f(xi+1-xi, a), f(xi+2-xi, a), f(xi+3-xi, a)]])
                mid = np.matrix([[p1, p2, p3, p4],
                                 [p5, p6, p7, p8],
                                 [p9, p10, p11, p12],
                                 [p13, p14, p15, p16]])
                rhs = np.matrix([[f(yi-yi, a)], [f(yi+1-yi, a)], [f(yi+2-yi, a)], [f(yi+3-yi, a)]])
                new_image[i, j] = np.dot(np.dot(lhs, mid), rhs)

        return new_image

    def lanczos_interpolation(self, image, fx, fy):
        n = 2
        x = image.shape[0]
        y = image.shape[1]

        def sinc(ang):
            if ang == 0:
                return 1
            else:
                return math.sin(math.pi*ang)/(math.pi*ang)

        def l(x, n):
            if abs(x) <= n:
                return sinc(x)*sinc(x/n)
            else:
                return 0

        new_x = fx * x
        new_y = fy * y
        r_ratio = new_x / x
        c_ratio = new_y / y
        new_x = int(new_x)
        new_y = int(new_y)
        new_image = np.zeros([new_x, new_y])
        nearest_row = np.array(range(x))
        nearest_col = np.array(range(y))

        nearest_row = nearest_row * r_ratio
        nearest_col = nearest_col * c_ratio

        nearest_row = np.ceil(nearest_row)
        nearest_col = np.ceil(nearest_col)
        for i in range(new_x):
            for j in range(new_y):
                w = 0
                sum = 0
                xi = np.abs(nearest_row - i).argmin()
                yi = np.abs(nearest_col - j).argmin()
                for i1 in range(-n+1, n):
                    for j1 in range(-n+1, n):
                        w = w + l(i1, n)*l(j1, n)

                for i1 in range(-n+1, n):
                    for j1 in range(-n+1, n):
                        sum = sum + image[xi, yi]*l(i1, n)*l(j1, n)

                if w != 0:
                    new_image[i, j] = sum/w
                else:
                    new_image[i, j] = 0

        return new_image
