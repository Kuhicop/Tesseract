# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import os


def main():
    import parseimgs
    text = parseimgs.parse()
    print("Found text: \n" + text)

main()
