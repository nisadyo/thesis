from flask import Flask 
from flask import render_template,request
import os
from scipy.io import wavfile
import numpy as np
import sys
import scipy.fftpack
import tryreadwav 
import re
import time

app = Flask(__name__)
# set FLASK_APP=tryflask.py
# flask run --host=0.0.0.0
UPLOAD_FOLDER = '/Users/riyaniannisa/Downloads/audio-master/flaskweb/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
@app.route('/') 
def hello_world():
    return render_template("index.html")
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      fname = f.filename
      if fname[-4:]!='.wav':
          fname=fname+".wav"
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],fname))
      frek, chn = tryreadwav.tryreadwav(os.path.join(app.config['UPLOAD_FOLDER'],fname))

      # ganti conf dengan
      os.system('rm fftfilterbank.cfg')
      f = open("fftfilterbank.cfg", "a")
      f.write("nchannels_in = " + str(chn) + "\nfragsize = 64\nsrate = 44100\nmhalib = mhachain\niolib = MHAIOFile\nmha.algos=[ fftfilterbank ]\nmha.fftfilterbank.f = " + re.sub(",","",str(frek)) + "\nmha.fftfilterbank.fail_on_unique_bins = no\nmha.fftfilterbank.ovltype = linear\nio.in = " + os.path.join(app.config['UPLOAD_FOLDER'],fname) + "\nio.out = " + os.path.join(app.config['UPLOAD_FOLDER'], "out_" + fname) + "\n")
      f.close()
      conf= "mha --interactive ?read:fftfilterbank.cfg cmd=start cmd=quit"
      os.system(conf)
      return render_template("result.html",audio="static/out_"+fname)
