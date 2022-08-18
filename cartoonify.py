# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 16:17:19 2022

@author: filon
"""

import cv2
import easygui
import numpy as np
import imageio
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

# opens the box to choose a file and help's store file path as a string
def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)
    
def save(Resized6, ImagePath):
    #saving an image
    newName = "cartonified_image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splittext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(Resized6, cv2.COLOR_RGB2BGR))
    I = "Image saved by name" + newName + "at" + path
    tk.messagebox.showinfo(title = None, message = I)
    
def cartoonify(ImagePath):
    # Read the image
    originalimage = cv2.imread(ImagePath)
    originalimage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2RGB)
    
    # Confirm that the image is chosen
    if originalimage is None:
        print("Can not find any image. Choose approprate file")
        sys.exit()
    
    Resized1 = cv2.resize(originalimage, (960,540))
    
    #Converting the image to grayscale
    gsImage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2GRAY)
    Resized2 = cv2.resize(gsImage,(960,540))
    
    #Smoothing the image
    smoothGS = cv2.medianBlur(gsImage,5)
    Resized3 = cv2.resize(smoothGS, (960,540))
    
    # Retireve the edges of an image
    getEdge = cv2.adaptiveThreshold(smoothGS, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    Resized4 = cv2.resize(getEdge, (960,540))
    
    # remove noise and keep sharp edges
    colorImage = cv2.bilateralFilter(originalimage, 9, 300, 300)
    Resized5 = cv2.resize(colorImage, (960,540))
    
    # masking edges images
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    Resized6 = cv2.resize(cartoonImage, (960,540))
    
    # Plotting the whole transition
    images = [Resized1, Resized2, Resized3, Resized4, Resized5, Resized6]
    fig, axes = plt.subplots(3,2, figsize = (8,8), subplot_kw = {'xticks':[], 'yticks':[]},
                             gridspec_kw = dict(hspace = 0.1, wspace = 0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap = 'gray')
    
    # save button
    save1 = Button(top, text = "Save image", command = lambda: save(Resized6, ImagePath), padx = 30, pady = 5)
    save1.configure(background = '#364156', foreground = "white", font = ('calibri', 10, 'bold'))
    save1.pack(side = TOP, pady = 50) 
    
    plt.show()
    
# Main Window
top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify an Image!')
top.configure(background = 'white')
label = Label(top, background = '#CDCDCD', font = ('calibri', 20, 'bold'))

# Cartoonify button
up = Button(top, text = "Cartoonify an Image", command = upload, padx = 10, pady = 5)
up.configure(background = '#364156', foreground = "white", font = ('calibri', 10, 'bold'))
up.pack(side = TOP, pady = 50)  

top.mainloop()