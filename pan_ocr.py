import pytesseract
import numpy as np
import cv2
import re
import validation
from PIL import Image, ImageEnhance
from datetime import datetime
import ftfy
import base64
from image_morphing import process_image
from flask import flash
import os

#provide ull path to your tesseract executable.
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Name\AppData\Local\Tesseract-OCR\tesseract.exe'


def remove_noise(image):
    return cv2.medianBlur(image,5)


def get_grayscale(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)


def brightness(im):
    #Enhance the image brightness by 1.8 times.
    enhancer = ImageEnhance.Brightness(Image.fromarray(im))
    enhanced_image = enhancer.enhance(1.8)
    return enhanced_image


def brightness2(im):
    #Enhance the image brightness by 1.5 times.
    enhancer = ImageEnhance.Brightness(Image.fromarray(im))
    enhanced_image = enhancer.enhance(1.5)
    return enhanced_image

def check_brightness(im):
    X,Y = 0,0
    image=Image.fromarray(im)
    image=image.convert("RGB")
    pixelRGB = image.getpixel((X,Y))
    R,G,B = pixelRGB
    brightness = sum([R,G,B])/3
    return brightness

def pan_image_process(image):
    """
    For improving the readability of image we are perfoming the below steps
    1.Convert the image to Gray scale format.
    2.Resize the image with variable height and width.
    3.Remove the noise.
    4.Enhance the brightness.

    Check the blur value of the image. If it is less then the thresold value
    then indicate the users about it clearity.

    return the extracted words from the image.
    """
    resized_img = []
    response = ''
    Base = ''
    img = process_image(image)
    dimensions = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    height = img.shape[0]
    width = img.shape[1]
    channels = img.shape[2]

    if (height > 768) and (width > 1024):
        height = 768
        width = 1024
        dim = (width, height)
        rmv_noise = remove_noise(img)
        resized_img = cv2.resize(rmv_noise, dim, interpolation = cv2.INTER_AREA)
    elif (height < 300) and (width < 400):
        resized_img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    else:
        resized_img = img

    brightness_level = check_brightness(resized_img)
    if brightness_level<250:
        imgbrightness = brightness(resized_img)
    else:
        imgbrightness=brightness2(resized_img)

    blur_value = cv2.Laplacian(resized_img, cv2.CV_64F).var()
    if blur_value <= 200.00 or resized_img.shape[0] <= 320:
        if not blur_value >= 650:
            flash("Uploaded image is blur, we are not able to fetch all the details. Please upload a clear image.")

    gray_image = get_grayscale(imgbrightness)
    image_text = pytesseract.image_to_string(gray_image,lang = 'eng')
    image_text = ftfy.fix_text(image_text)
    image_text = ftfy.fix_encoding(image_text)
    response += image_text + '\n'
    return response


def prepare_pan_data(pan_data_text):
    """
    Extract relevant information from pan data.
    Approch that has been amde to get neccessary information is
    1.Convert pancard image text to list.
    2.Remove the white space, blank line and new line.
    3.Searching for PAN
        First search text "Permant account number" if found then the immidiate
        next list element is the PAN number, if not found then apply
        regex pattern to find the PAN number and then validate the PAN number.
    4.Find the string "INCOME TAX DEPARTMENT" and "GOVT. OF INDIA" and remove
    them from the list.
    5.Remove all the elements from the list which contains any smallcase letter
    (because all the relevant information in pan card are in uppercase)
    6.Find the DOB using the regular expression pattern.
    7 Now we left with the list which contains the name and father name, so get
    get the names and validate them.
    8.prepare the dictionary and return the same.
    """

    #nitializing data variable
    name = ''
    fname = ''
    dob = ''
    pan_no = []
    pan_number = ''
    pan_detail_list = []

    # Clearing out the unwanted and emty space
    lines = pan_data_text.split('\n')
    for line in lines:
        s = line.strip()
        s = line.replace('\n','')
        s = s.rstrip()
        s = s.lstrip()
        pan_detail_list.append(s)
    pan_detail_list = list(filter(None, pan_detail_list))


    #Searching for PAN string
    pan_string = '(Pormanam|Number|umber|Account|ccount|count|Permanent|\
    ermanent|manent|wumm)$'
    line_no = -1
    for wordline in pan_detail_list:
        word_lst = wordline.split( )
        if ([word for word in word_lst if re.search(pan_string, word)]):
            lineno = pan_detail_list.index(wordline)
            pan_no = pan_detail_list[lineno+1:]
            pan_detail_list.remove(pan_detail_list[lineno])
            break
    if pan_no:
        try:
            pan_number = validation.validate_pan_no(pan_no[0])
            pan_detail_list.remove(pan_number)
        except:
            pan_number = ''
    else:
        pan_number = ''

    #Get PAN number using RegEx pattern
    if pan_number == '':
        pan_reg_exp = re.compile(r'^[A-Z0-9]{5}[A-Z0-9]{4}[A-Z]$')
        for wordline in pan_detail_list:
            if pan_reg_exp.findall(wordline):
                pan_number = validation.validate_pan_no(wordline)
                pan_detail_list.remove(wordline)


    #Searching GOV text string and remove them
    gov_string = '(INCOMETAXDEPARWENT @|mcommx|INCOME|TAX|GOW|GOVT|GOVERNMENT|\
    OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA)$'
    for wordline in pan_detail_list:
            word_lst = wordline.split( )
            if ([word for word in word_lst if re.search(gov_string, word)]):
                pan_detail_list.remove(wordline)

    #Remove smallcase elements form list
    pan_detail_list = [ele for ele in pan_detail_list if not any(c for c in ele if c.islower())]


    #Searching DOB using RegEx pattern
    date_reg_exp = re.compile(r'\d{2}[-/]\d{2}[-/]\d{4}')
    for wordline in pan_detail_list:
        if date_reg_exp.findall(wordline):
            dob = wordline
            pan_detail_list.remove(wordline)


    #Get name & father name and validate them
    try:
        name = validation.validate_name(pan_detail_list[0])
    except:
        name = ''

    try:
        fname =validation.validate_father_name( pan_detail_list[1])
    except:
        fname = ''

    data = {
        'Name' : name,
        'Father name' : fname,
        'Date of birth' : dob,
        'PAN number' : pan_number,
    }

    return data


def get_pan_details(image):
    pan_details = pan_image_process(image)
    pan_data = prepare_pan_data(pan_details)
    return pan_data

def face_detect(image):
    #Detect the face and save the face image.
    #return 1 if found face in pancard else 0.
    image = cv2.imread('static/'+image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(30, 30)
    )

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x-10, y-10), (x + w + 10, y + h + 10), (0, 255, 0), 2)
            face_color = image[y-10:y + h + 10, x-10:x + w + 10]
            face_path = os.path.join('static', 'face.jpg')
            cv2.imwrite(face_path, face_color)
        return 1
    return 0
