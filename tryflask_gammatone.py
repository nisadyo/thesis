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
# D:\caca\thesis\env\Scripts\activate.bat
# set FLASK_APP=tryflask_gammatone.py
# flask run --host=0.0.0.0
UPLOAD_FOLDER = 'D:\\caca\\thesis\\static'

DOWNLOAD_FOLDER = 'C:\\Users\\"nanang saiful"\\Downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER 
ovltype = 'rect'

@app.route('/') 
def hello_world():
    return render_template("index.html")

@app.route('/recorder', methods = ['GET', 'POST'])
def record_file():
   if request.method == 'POST':
      fname="audio.wav"
      f_in_new_name="new_in_audio.wav"
      os.system("del static\\audio.wav")
      os.system('copy C:\\Users\\"nanang saiful"\\Downloads\\audio.wav static')
      fs, fcoef, norm = tryreadwav.tryReadGammatone(os.path.join(app.config['UPLOAD_FOLDER'],fname))
      
      time.sleep(5)
      
      rate_in, data_in = wavfile.read("static/audio.wav")
      print(data_in)
      new_data = np.array([[y for i in range(2)] for y in data_in]) #biar channel jadi 2
      print(new_data)
      wavfile.write("static/new_in_audio.wav", rate_in, new_data)
      
      os.system('del gammatone.cfg')
      f = open("gammatone.cfg", "a")
      f.write("nchannels_in = " + str(2) + "\nfragsize = 64\nsrate = "+str(rate_in)+"\nmhalib = mhachain\niolib = MHAIOFile\nmha.algos=[ gtfb_analyzer ]\nmha.gtfb_analyzer.coeff = " + re.sub("'","",str(['{:.30f}'.format(round(x,30)) for x in fcoef[0]] )).replace(",","") + "\nmha.gtfb_analyzer.norm_phase = " + re.sub("'","",str(['{:.30f}'.format(round(x,30)) for x in norm[0]] )).replace(",","") + "\nio.in = " + os.path.join(app.config['UPLOAD_FOLDER'],f_in_new_name) + "\nio.out = " + os.path.join(app.config['UPLOAD_FOLDER'], "out_" + fname) + "\n")
      f.close()
      
      conf= "mha --interactive ?read:gammatone.cfg cmd=start cmd=quit"
      os.system(conf)
      time.sleep(5)
      rate, data = wavfile.read("static/out_audio.wav")
    #   new_out=data
      new_out = np.array([[y[i] for i in range(8)] for y in data])
      print('hello')
      wavfile.write("static/new_out_audio.wav", rate, new_out)
      os.system('del C:\\Users\\"nanang saiful"\\Downloads\\audio.wav')
      return render_template("result.html",audio="static/new_out_"+fname)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      fname = f.filename
      if fname[-4:]!='.wav':
          fname=fname+".wav"
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],fname))
      fs, fcoef, norm = tryreadwav.tryReadGammatone(os.path.join(app.config['UPLOAD_FOLDER'],fname))

      # ganti conf dengan
      os.system('del gammatone.cfg')
      f = open("gammatone.cfg", "a")
      f.write("nchannels_in = " + str(chn) + "\nfragsize = 64\nsrate = " + str(fs) + "\nmhalib = mhachain\niolib = MHAIOFile\nmha.algos=[ gammatone ]\nmha.gammatone.coeff = " + re.sub("'","",str(['{:.30f}'.format(round(x,30)) for x in fcoef[0]] )).replace(",","") + "\nmha.gtfb_analyzer.norm_phase = " + re.sub("'","",str(['{:.30f}'.format(round(x,30)) for x in norm[0]] )).replace(",","") + "\nio.in = " + os.path.join(app.config['UPLOAD_FOLDER'],fname) + "\nio.out = " + os.path.join(app.config['UPLOAD_FOLDER'], "out_" + fname) + "\n")
      f.close()
      conf= "mha --interactive ?read:gammatone.cfg cmd=start cmd=quit"
      os.system(conf)
      return render_template("result.html",audio="static/out_"+fname)
