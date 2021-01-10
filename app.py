from flask import Flask, request, jsonify, render_template, flash
from pan_ocr import get_pan_details, face_detect
import os

ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'as%#$5YTfg&^*jg97&(&VJ&'
app.config["UPLOAD_FOLDER"] = 'static'

#set the cache control max age to this number of seconds.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods = ['GET', 'POST'])
def upload_pancard():
  if request.method == 'POST':
    pan_card_image = request.files["file"]
    if pan_card_image:
      if allowed_file(pan_card_image.filename):
        path = os.path.join(app.config["UPLOAD_FOLDER"], 'pancard.jpg')
        pan_card_image.save(path)
        #get pancard details like name, father name, dob, pan number etc.
        data = get_pan_details('pancard.jpg')
        #get face image from pan card
        face = face_detect('pancard.jpg')
        pan_img = os.path.join(app.config["UPLOAD_FOLDER"], 'pancard.jpg')
        return render_template('pan_upload.html', data = data, pan_image = pan_img, face = face)
      else:
        flash('Only PNG, JPG and JPEG files are allowed !')
        return render_template('pan_upload.html')
    else:
      flash('Please select a file !')
      return render_template('pan_upload.html')
  else:
    return render_template('pan_upload.html')

if __name__ == '__main__':
  app.run()
