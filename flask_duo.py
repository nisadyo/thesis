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
DOWNLOAD_FOLDER = '/Users/riyaniannisa/Downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER 
@app.route('/') 
def hello_world():
    return render_template("index.html")
@app.route('/recorder', methods = ['GET', 'POST'])
def record_file():
   if request.method == 'POST':
      fname="audio.wav"
      f_in_new_name="new_in_audio.wav"
      os.system('rm static/audio.wav')
      os.system('cp ~/Downloads/audio.wav ~/Downloads/audio-master/flaskweb/static')
      frek, chn = tryreadwav.tryReadWavRecord(os.path.join(app.config['UPLOAD_FOLDER'],fname))
      
      time.sleep(5)
      
      rate_in, data_in = wavfile.read("static/audio.wav")
      print(data_in)
      new_data = np.array([[y for i in range(2)] for y in data_in])
      print(new_data)
      wavfile.write("static/new_in_audio.wav", rate_in, new_data)
      
      os.system('rm fftfilterbank.cfg')
      f = open("fftfilterbank.cfg", "a")
      f.write("nchannels_in = " + str(2) + "\nfragsize = 64\nsrate = 44100\nmhalib = mhachain\niolib = MHAIOFile\nmha.algos=[ fftfilterbank ]\nmha.fftfilterbank.f = " + re.sub(",","",str(frek)) + "\nmha.fftfilterbank.fail_on_unique_bins = no\nmha.fftfilterbank.ovltype = linear\nio.in = " + os.path.join(app.config['UPLOAD_FOLDER'],f_in_new_name) + "\nio.out = " + os.path.join(app.config['UPLOAD_FOLDER'], "out_" + fname) + "\n")
      
      f.close()
      conf= "mha --interactive ?read:fftfilterbank.cfg cmd=start cmd=quit"
      os.system(conf)
      time.sleep(5)
      rate, data = wavfile.read("static/out_audio.wav")
      new_out = np.array([[y for i in range(2)] for y in data])
      print(rate)
      print(data)
      print('hello')
      wavfile.write("static/new_out_audio.wav", rate, data)
      os.system('rm ~/Downloads/audio.wav')
      return render_template("result.html",audio="static/new_out_"+fname)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      fname = f.filename
      if fname[-4:]!='.wav':
          fname=fname+".wav"
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],fname))
      frek, chn = tryreadwav.tryReadWavAudio(os.path.join(app.config['UPLOAD_FOLDER'],fname))

      # ganti conf dengan
      os.system('rm fftfilterbank.cfg')
      f = open("fftfilterbank.cfg", "a")
      f.write("nchannels_in = " + str(chn) + "\nfragsize = 64\nsrate = 44100\nmhalib = mhachain\niolib = MHAIOFile\nmha.algos=[ fftfilterbank ]\nmha.fftfilterbank.f = " + re.sub(",","",str(frek)) + "\nmha.fftfilterbank.fail_on_unique_bins = no\nmha.fftfilterbank.ovltype = linear\nio.in = " + os.path.join(app.config['UPLOAD_FOLDER'],fname) + "\nio.out = " + os.path.join(app.config['UPLOAD_FOLDER'], "out_" + fname) + "\n")
      f.close()
      conf= "mha --interactive ?read:fftfilterbank.cfg cmd=start cmd=quit"
      os.system(conf)
      return render_template("result.html",audio="static/out_"+fname)
