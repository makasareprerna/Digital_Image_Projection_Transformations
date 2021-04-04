#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Oct 31 11:47:32 2019

@author: Parth
"""
import numpy as np
import tkinter as tk
import math as m
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
import cv2

# Import packages containing operations
from transformations import imgshear, imgwarp, interpolation, reflection,\
                             resample, rotation, resample, translation, perspective


# Creating objects for the class
Rotate_obj = rotation.rotation()
Translation_obj = translation.translation()
Warp_obj = imgwarp.imgwarp()
Reflect_obj = reflection.reflection()
Shear_obj = imgshear.imgshear()
Perspective_obj = perspective.perspective()
Scaling_obj = resample.resample()

img_path = None
InputImage = None
InputImage_copy = None
InputImage_PIL = None
img = None
SelectPointsFlag = 0
PerspectivePoints = []


##############################################################################################################
"""CALBACK FUNCTIONS"""


def OpenFileCB():
    global img_path
    global InputImage
    global InputImage_copy
    global InputImage_PIL
    global img

    ImageOptions.filename = filedialog.askopenfilename(initialdir=".",
                                                       title="Select file",
                                                       filetypes=(("Image Files", "*.jpg *.jpeg *.png *.gif"),
                                                                  ("All Files", "*.*")))
    img_path = ImageOptions.filename
    InputImage = cv2.imread(img_path, 0)
    # print(InputImage.shape)
    InputImage_copy = InputImage.copy()

    # cv2.imshow("!@#",InputImage)

    InputImage_PIL = Image.fromarray(InputImage).resize((800, 800), Image.ANTIALIAS)

    # print(InputImage_np)
    img = ImageTk.PhotoImage(InputImage_PIL)

    canvas.itemconfig(image_disp, image=img)
    ImageFrame.update()


def ResetCB():
    global img_path
    global InputImage
    global InputImage_copy
    global InputImage_PIL
    global img

    # Resetting all the vars to 0
    # Rotate Slider
    Rotate_var.set(0)
    #RotateSlider.set(value = 0)

    # Translate Spinner
    XTrans_var.set(value=0)
    YTrans_var.set(value=0)

    # Warp Spinner
    XWarp_var.set(0)
    YWarp_var.set(0)
    
    #Scale Spinner
    ScaleX_var.set(0)
    ScaleY_var.set(0)

    InputImage_PIL = Image.fromarray(InputImage_copy).resize((800, 800), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(InputImage_PIL)
    canvas.itemconfig(image_disp, image=img)
    ImageFrame.update()


def RotateLeftCB():
    degrees_to_rotate = RotateSlider.get() - 90
    RotateSlider.set(value=degrees_to_rotate)


def RotateRightCB():
    #print("RotateRightCB")
    degrees_to_rotate = RotateSlider.get() + 90
    RotateSlider.set(value=degrees_to_rotate)


def RotateCB(angle):

    global img
    global InputImage
    angle_flt = float(angle)
    angle_in_radians = (m.radians(angle_flt))
    # print(InputImage.size)
    RotatedImg = Rotate_obj.rotate(InputImage, angle_in_radians)
    RotatedImg_PIL = Image.fromarray(RotatedImg).resize((800, 800), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(RotatedImg_PIL)
    canvas.itemconfig(image_disp, image=img)


def XYTransCB():
    global img_path
    global InputImage
    global InputImage_copy
    global InputImage_PIL
    global img

    InputImage = Translation_obj.translateImage(InputImage, XTrans_var.get(), YTrans_var.get())
    InputImage_PIL = Image.fromarray(InputImage).resize((800, 800), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(InputImage_PIL)
    canvas.itemconfig(image_disp, image=img)

    img = ImageTk.PhotoImage(InputImage_PIL)
    canvas.itemconfig(image_disp, image=img)
    # ImageFrame.update()


def WarpCB():
    global img_path
    global InputImage
    global InputImage_copy
    global InputImage_PIL
    global img

    InputImage = Warp_obj.imgwarp(InputImage, XWarp_var.get(), YWarp_var.get())
    InputImage_PIL = Image.fromarray(InputImage).resize((800, 800), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(InputImage_PIL)
    canvas.itemconfig(image_disp, image=img)

    img = ImageTk.PhotoImage(InputImage_PIL)
    canvas.itemconfig(image_disp, image=img)


def ShearCB():
    global img_path
    global InputImage
    global InputImage_copy
    global InputImage_PIL
    global img

    if(ShearType_var.get() == 0):
        InputImage = Shear_obj.horizontalShear(InputImage, ShearVal_var.get())
    elif (ShearType_var.get() == 1):
        InputImage = Shear_obj.verticalShear(InputImage, ShearVal_var.get())

    InputImage_PIL = Image.fromarray(InputImage).resize((800, 800), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(InputImage_PIL)
    canvas.itemconfig(image_disp, image=img)


def XReflectCB():
    global img_path
    global InputImage
    global InputImage_copy
    global InputImage_PIL
    global img

    InputImage = Reflect_obj.reflectX(InputImage)
    InputImage_PIL = Image.fromarray(InputImage).resize((800, 800), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(InputImage_PIL)
    canvas.itemconfig(image_disp, image=img)


def YReflectCB():
    global img_path
    global InputImage
    global InputImage_PIL
    global img

    InputImage = Reflect_obj.reflectY(InputImage)
    InputImage_PIL = Image.fromarray(InputImage).resize((800, 800), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(InputImage_PIL)
    canvas.itemconfig(image_disp, image=img)
    
def ScaleCB():
    global img_path
    global InputImage
    global InputImage_PIL
    global img
    
    print(ScaleX_var.get())
    print(ScaleY_var.get())
    print(ScalingType_var.get())
    
    
    InputImage = Scaling_obj.resize(InputImage, ScaleX_var.get(), ScaleY_var.get(), ScalingType_var.get())
    InputImage_PIL = Image.fromarray(InputImage)#.resize((800, 800), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(InputImage_PIL)
    canvas.itemconfig(image_disp, image=img)



def SelectPointsEvent(event):
    global SelectPointsFlag
    global PerspectivePoints
    #print(SelectPointsFlag)
    #print("Click captured")

    point = (event.x, event.y)    
    PerspectivePoints.append(point)
    
    if(SelectPointsFlag != 0):
        canvas.create_line(PerspectivePoints[SelectPointsFlag - 1][0], PerspectivePoints[SelectPointsFlag - 1][1],
                          PerspectivePoints[SelectPointsFlag][0], PerspectivePoints[SelectPointsFlag][1], tags = 'line') 
    
    SelectPointsFlag += 1
    if(SelectPointsFlag == 4):
        canvas.create_line(PerspectivePoints[3][0], PerspectivePoints[3][1],
                          PerspectivePoints[0][0], PerspectivePoints[0][1], tags = 'line') 
        canvas.unbind("<Button-1>")
    
def SelectPointsCB():
    global SelectPointsFlag
    global PerspectivePoints
    
    #Clearing the list of points, Square and setting the flag to zero
    del PerspectivePoints[:]
    canvas.delete('line')
    SelectPointsFlag = 0
    
    #print("flag is: ", SelectPointsFlag)
    
    canvas.bind("<Button-1>", SelectPointsEvent)
    
def PerspectiveTransformCB():
    global img_path
    global InputImage
    global InputImage_copy
    global InputImage_PIL
    global img
    global PerspectivePoints
    global SelectPointsFlag


    InputImage = Perspective_obj.perspective_transform(InputImage, PerspectivePoints)
    InputImage_PIL = Image.fromarray(InputImage).resize((800, 800), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(InputImage_PIL)
    canvas.itemconfig(image_disp, image=img)

    img = ImageTk.PhotoImage(InputImage_PIL)
    canvas.itemconfig(image_disp, image=img)
    del PerspectivePoints[:]
    canvas.delete('line')
    SelectPointsFlag = 0
    
    # ImageFrame.update()
    

##############################################################################################################


root = tk.Tk()
root.state("normal")  # to make it full screen
root.title("Image Geometric Transformations -- DIPShifts")
# root.geometry("1200x800")
root.config(bg="grey80")


'''###Parent Frame: root###'''
root.columnconfigure(0, weight=1)
root.columnconfigure(2, weight=10)
root.rowconfigure(0, weight=1)

# Setting the Imageframe to display image
ImageFrame = tk.Toplevel(root)

#ImageFrame = ttk.Frame(root, width=800, height=800, relief="ridge", padding = [5,5])
#ImageFrame.grid(row = 0, column = 0, columnspan = 2)

# Setting The frame where edit options would be given
EditFrame = ttk.Frame(root, width=400, height=800, relief="ridge")
EditFrame.grid(row=0, column=2)

'''###Parent Frame: ImageFrame###'''
# Setting canvas and putting image on canvas
canvas = tk.Canvas(ImageFrame, width=800, height=800)
# creating a placeholder grey screen
img = Image.new('RGB', (800, 1280), (200, 200, 200))
img = ImageTk.PhotoImage(img)

image_disp = canvas.create_image(400, 400, image=img)
canvas.pack(fill=tk.BOTH, expand=1)


'''###Parent Frame: EditFrame###'''

notebook = ttk.Notebook(EditFrame)
notebook.grid(row=0, column=0, stick='nsew')

ImageOptions = ttk.Frame(EditFrame)
ImageOptions.grid(row=1, column=0, stick='nsew')

'''###Parent Frame: ImageOptions###'''
BrowseButton = tk.Button(ImageOptions, text="Browse", command=OpenFileCB)
BrowseButton.grid(row=0, column=0, stick='nsew')

ResetButton = tk.Button(ImageOptions, text="Reset", command=ResetCB)
ResetButton.grid(row=0, column=4, stick='nsew')


'''###Parent Frame: Notebook###'''
RotateFrame = ttk.Frame(notebook)
TranslateFrame = ttk.Frame(notebook)
WarpFrame = ttk.Frame(notebook)
ShearFrame = ttk.Frame(notebook)
ReflectionFrame = ttk.Frame(notebook)
ScalingFrame = ttk.Frame(notebook)
PerspectiveFrame = ttk.Frame(notebook)


# Adding Tabs to Notebook
notebook.add(RotateFrame, text="Rotate")
notebook.add(TranslateFrame, text="Translate")
notebook.add(WarpFrame, text="Warp")
notebook.add(ShearFrame, text="Shear")
notebook.add(ReflectionFrame, text="Reflection")
notebook.add(ScalingFrame, text="Scaling")
notebook.add(PerspectiveFrame, text="Perspective")


'''###Parent Frame: RotateFrame###'''
Rotate_var = tk.IntVar()
RotateLeftButton = ttk.Button(RotateFrame, text='rotate left', command=RotateLeftCB)
RotateLeftButton.grid(row=1, column=0)

RotateRightButton = ttk.Button(RotateFrame, text='rotate right', command=RotateRightCB)
RotateRightButton.grid(row=1, column=1)

RotateSlider = tk.Scale(RotateFrame, command=RotateCB, from_=0, variable=Rotate_var,
                        length=300, orient=tk.HORIZONTAL, to=360, relief='flat')
RotateSlider.grid(row=0, column=0, columnspan=2)


'''###Parent Frame: TranslateFrame###'''
# Declaring TKVariables to track changes
XTrans_var = tk.IntVar()
XTrans_var.set(0)
YTrans_var = tk.IntVar()
YTrans_var.set(0)

XTranslate = tk.Spinbox(TranslateFrame, from_=0, to=800, textvariable=XTrans_var)
XTranslate.grid(row=0, column=0)

YTranslate = tk.Spinbox(TranslateFrame, from_=0, to=800, textvariable=YTrans_var)
YTranslate.grid(row=0, column=1)

TranslateButton = tk.Button(TranslateFrame, text="Apply Translation", command=XYTransCB)
TranslateButton.grid(row=1, column=1, stick='nsew')


'''###Parent Frame: WarpFrame###'''
XWarp_var = tk.IntVar()
XWarp_var.set(0)
YWarp_var = tk.IntVar()
YWarp_var.set(0)


XWarp = tk.Spinbox(WarpFrame, from_=0, to=100, textvariable=XWarp_var)
XWarp.grid(row=0, column=0)

YWarp = tk.Spinbox(WarpFrame, from_=0, to=100, textvariable=YWarp_var)
YWarp.grid(row=0, column=1)

HVWarping = tk.Button(WarpFrame, text="Apply Warping", command=WarpCB)
HVWarping.grid(row=1, column=1, stick='nsew')


'''###Parent Frame: SheerFrame###'''
ShearType_var = tk.IntVar()
ShearType_var.set(0)
ShearVal_var = tk.DoubleVar()
ShearVal_var.set(0)


ShearingFactor = ttk.Radiobutton(ShearFrame, text='Horizontal', variable=ShearType_var, value='0')
ShearingFactor.grid(row=0, column=0, stick='nsew')

ShearingFactor = ttk.Radiobutton(ShearFrame, text='Vertical', variable=ShearType_var, value='1')
ShearingFactor.grid(row=0, column=1, stick='nsew')

ShearingFactor = tk.Spinbox(ShearFrame, from_=0, to=1, textvariable=ShearVal_var, increment=0.01)
ShearingFactor.grid(row=1, column=0, stick='nsew')


ApplyShearing = tk.Button(ShearFrame, text="Apply Shearing", command=ShearCB)
ApplyShearing.grid(row=2, column=0, stick='nsew')


'''###Parent Frame: ReflectionFrame###'''
ReflectTop = tk.Button(ReflectionFrame, text="Reflect Along X Axis", command=XReflectCB)
ReflectTop.grid(row=0, column=0, stick='nsew')

ReflectLeft = tk.Button(ReflectionFrame, text="Reflect Along Y Axis", command=YReflectCB)
ReflectLeft.grid(row=1, column=0, stick='nsew')


'''###Parent Frame: ScalingFrame###'''
ScalingType_var = tk.StringVar()
ScalingType_var.set(0)
ScaleX_var = tk.DoubleVar()
ScaleX_var.set(0)
ScaleY_var = tk.DoubleVar()
ScaleY_var.set(0)

ScaleX = tk.Spinbox(ScalingFrame, from_=0, textvariable = ScaleX_var, increment=0.1)
ScaleX.grid(row=0, column=0, columnspan = 2, stick='nsew')

ScaleY = tk.Spinbox(ScalingFrame, from_=0, textvariable = ScaleY_var, increment=0.01)
ScaleY.grid(row=0, column=2, columnspan = 2, stick='nsew')

NNRadioBtn = ttk.Radiobutton(ScalingFrame, text="Nearest Neighbour",  variable = ScalingType_var, value = 'nearest_neighbor')
NNRadioBtn.grid(row=1, column=0, stick='nsew')

BilinearRadioBtn = ttk.Radiobutton(ScalingFrame, text="Bilinear", variable = ScalingType_var, value = 'bilinear')
BilinearRadioBtn.grid(row=1, column=1, stick='nsew')

BicubicRadioBtn = ttk.Radiobutton(ScalingFrame, text="Bicubic", variable = ScalingType_var, value = 'bicubic')
BicubicRadioBtn.grid(row=1, column=2, stick='nsew')

LancozRadioBtn = ttk.Radiobutton(ScalingFrame, text="Lancoz", variable = ScalingType_var, value = 'lanczos')
LancozRadioBtn.grid(row=1, column=3, stick='nsew')

ApplyScaling = ttk.Button(ScalingFrame, text = "Apply Scaling", command = ScaleCB)
ApplyScaling.grid(row = 2, column = 0)

'''###Parent Frame: PerspectiveFrame###'''
SelectPointsButton = ttk.Button(PerspectiveFrame, text = "Click here to select points on the image"
                               , command = SelectPointsCB)
SelectPointsButton.grid(row = 0, column = 0)

ApplyPerspectiveTransform = ttk.Button(PerspectiveFrame, text = "Apply Perspective Transform"
                               , command = PerspectiveTransformCB)
ApplyPerspectiveTransform.grid(row =1, column = 0)

if (__name__ == '__main__'):
    root.mainloop()
