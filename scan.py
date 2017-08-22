# A simple app to scan and read receipts.
# Project goal: To extract vendor name, date, and total from a scanned image of a receipt.

# Code built using the following tutorials:
# http://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/

# SCANNER CODE
# import the necessary packages
# import the necessary packages
from PIL import Image
from resizeimage import resizeimage
import pytesseract
import argparse
import cv2
import os
from ast import literal_eval
import difflib

# construct the argument parse and parse the arguments
def processing_type():
    ap = argparse.ArgumentParser()

    ap.add_argument("-p", "--preprocess", type=str, default="blur",
        help="type of preprocessing to be done")
    args = vars(ap.parse_args())
 
# load the example image and convert it to grayscale

def resize_image():
    with Image.open("test.jpg") as img:
    # Lots of experiments to resize, crop, or convert the image to improve quality:
    # Start by printing the color mode of the original image
        # print(img.mode)
    # Get the image dimensions
        # w, h = img.size
        # print(w,h, img.mode)
    # Calculate new dimensions based on doubling the width & height
        # new_width = w*2
        # new_height = h*2
        # print(new_width)
    # resize image
        # img = resizeimage.resize_contain(img, [new_height, new_width])
    
    # Convert image to rgb (from RGBA) in order to save it as .jpg:
    # https://github.com/python-pillow/Pillow/issues/2005
        img = img.convert("RGB")
        print(img.mode)
        img = img.rotate(270)
        img.save('test-rgb.jpg', img.format)
        # print(type(img))
        # print(w,h, img.mode)

        img.close()

def grayscale():
    # test 1 (small file, 80kb):
    image = cv2.imread('small-scan.jpg')

# Select the file to read from various test images:
    #test cropped image:
    # image = cv2.imread('test-crop.jpg')

    #test 3 (original file size 1.9 MB):
    # image = cv2.imread('test.jpg')
    
    # test resized image:
    # image = cv2.imread('test-rgb.jpg')
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image", image)
    return image, gray

def process():
# check to see if we should apply thresholding to preprocess the image
    image, gray = grayscale()
    if args["preprocess"] == "thresh":
        gray = cv2.threshold(gray, 0, 255,
            cv2.THRESH_TRUNC | cv2.THRESH_OTSU)[1]
        return image, gray
    elif args ["preprocess"] == "custom":
        gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,2 | cv2.THRESH_OTSU)
        return image, gray
        
    # make a check to see if median blurring should be done to remove noise
    elif args["preprocess"] == "blur":
        gray = cv2.medianBlur(gray, 3)
        return image, gray

# write the grayscale image to disk as a temporary file so we can apply OCR to it
def ocr(image, gray):  
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    print("ocr output type:", type(text), len(text))
    
    # show the output images
    # cv2.imshow("Image", image)
    # cv2.imshow("Output", gray)
    # cv2.waitKey(0)
    return text

# load clean test data
def get_test_set():
    with open("goal_text.txt") as file:
        chars = file.read()
        print(len(chars))
        return chars

# test for character-level accuracy
def compare_text(ocr_text, test_text):
    # Create a visual comparison of texts
    diff = difflib.ndiff(ocr_text.splitlines(keepends=True),test_text.splitlines(keepends=True))
    print(''.join(diff), end="")
   
    # Calculate accuracy on character level
    s = difflib.SequenceMatcher(None, ocr_text,test_text)
    ratio = round(s.ratio(),2)    
    print("Difference ratio: ", ratio)

processing_type()
image, gray = grayscale()
ocr_text = ocr(image, gray)
test_text = get_test_set()
compare_text(ocr_text,test_text)

