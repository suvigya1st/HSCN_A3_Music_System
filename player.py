from flask import Flask, Response
from flask import url_for
from flask import render_template ,send_from_directory
from flask import Markup 
import os
from mutagen.mp3 import MP3
import getmusicfiles
import vlc
import urllib

app = Flask(__name__)

from gevent.wsgi import WSGIServer
http_server=WSGIServer(('',5002),app)

tracklist=[]
getmusicfiles.generatefilepaths()
files=open('musicfiles','rb')
ind=0
playing = False
music=files.readlines()
for songs in music:
	song=songs.strip()
	songname=os.path.split(song)[1]
	audio=MP3(song)
	lengthSec=int(audio.info.length)
	length=str(lengthSec/60)+':'+str(lengthSec%60)
	d={"track":ind,
		"name":songname,
		"length":length,
		"file":song
	}
	tracklist.append(d)
	ind+=1

musicObj=vlc.MediaPlayer()
musicObj.audio_set_volume(100)

currentTrackInfo=0

currentTrackTime=0
def getTrackData(trackId):
	for tracks in tracklist:
		if tracks["track"]==trackId:
			return tracks

@app.route('/media/<int:songid>')
def returnMusic(songid):
	global musicObj,playing,currentTrackInfo
	#s=urllib.unquote(songname).decode('utf8')
	#songname=s
	for track in tracklist:
		if track["track"] == songid:
			filename=track["file"]
			currentTrackInfo=track["track"]
			break
	musicObj.stop()
	musicObj=vlc.MediaPlayer("file://"+filename)
	if playing:
		musicObj.play()

	return send_from_directory(os.path.split(filename)[0],os.path.split(filename)[1])

@app.route('/action/play/<id>',methods=['POST'])
def playsong(id):
	global playing
	playing = True
	global musicObj
	playing = True
	musicObj.set_time(int(float(id)*1000)-50)
	musicObj.play()
	return '200'

@app.route('/tracktime/<tracktime>',methods=['POST'])
def updateTrackTime(tracktime):
	global currentTrackTime
	currentTrackTime=float(tracktime)
	return '200'

@app.route('/action/pause/<id>',methods=['POST'])
def pause(id):
	global musicObj
	playing=False
	musicObj.pause()
	return "200"
@app.route('/')
def home():
	global currentTrackTime,currentTrackInfo
	tracks=Markup(tracklist)
	return render_template('index.html',tracklist=tracks,currentTrackInfo=currentTrackInfo,currentTrackTime=currentTrackTime)

if __name__=="__main__":
	#app.run(host='127.0.0.1',port=80,debug=True)
	print "Server up and running!"
	http_server.serve_forever()
