PAN-OCR will fetch the relavent information like Name, Father name, PAN number, DOB and face image from the pancard.

Stpes to setup project.
1. Clone the repository https://github.com/hareshkat/pan_ocr.git
2. Go to pan_ocr folder.
3. Make virtual environment and install the required packages. (pip inatsll -r requirements.txt)
4. In pan_ocr.py, change pytesseract.pytesseract.tesseract_cmd value. It contains the path where the tesseract ocr is installed.
5. Run the app.py file.(python app.py)
6. Visit http://127.0.0.1:5000/
7. Upload pancard image to fecth the details.
