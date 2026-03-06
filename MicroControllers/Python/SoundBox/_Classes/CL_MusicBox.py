#!/usr/bin/env python
# -*- coding: utf8 -*-
import os

class CL_MusicBox: 
  import os.path
  import subprocess
  import shutil
  import time
  import alsaaudio
  from time import sleep

  try:
    from mutagen.mp3 import MP3
  except ImportError:
    MP3 = None

  def __init__(self):
    self.songnum = -1
    self.album_tracknum =-1
    self.albumpath = ""
    self.t_end = 0
    self.mp3files = ""
    self.b_stop_music = 0
    self.b_print = 0
    self.process = None
    self._mixer_name = None
    self._mixer_cardindex = None
    self._player_cmd = None
##    self.b_checkinputs = 0
    projectPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
    self.Path = os.path.join(projectPath,'Files','Sounds')
    self.musicpath = self.Path
    self.switcher = {
          0: "",
          1: "Sounds1/"
      }

  def _get_mixer(self):
    if self._mixer_name is not None:
      try:
        if self._mixer_cardindex is None:
          return self.alsaaudio.Mixer(self._mixer_name)
        return self.alsaaudio.Mixer(self._mixer_name, cardindex=self._mixer_cardindex)
      except Exception:
        self._mixer_name = None
        self._mixer_cardindex = None
      
    return self.detect_mixer()
      
  def detect_mixer(self):
    candidates = []
    for mixer_name in ('PCM', 'Master', 'Speaker', 'Digital', 'Headphone'):
      candidates.append((mixer_name, None))

    # Discover mixers from ALSA so Pi/USB cards with custom names are supported.
    try:
      for mixer_name in self.alsaaudio.mixers():
        candidates.append((mixer_name, None))
    except Exception:
      pass

    try:
      for card_index, _ in enumerate(self.alsaaudio.cards()):
        try:
          for mixer_name in self.alsaaudio.mixers(cardindex=card_index):
            candidates.append((mixer_name, card_index))
        except Exception:
          pass
    except Exception:
      pass

    seen = set()
    for mixer_name, card_index in candidates:
      key = (mixer_name, card_index)
      if key in seen:
        continue
      seen.add(key)

      try:
        if card_index is None:
          mixer = self.alsaaudio.Mixer(mixer_name)
        else:
          mixer = self.alsaaudio.Mixer(mixer_name, cardindex=card_index)
        self._mixer_name = mixer_name
        self._mixer_cardindex = card_index
        print(f"Using mixer '{mixer_name}' on card {card_index if card_index is not None else 'default'} for volume control")
        return mixer
      except Exception:
        pass

    return None

  def import_jsonConfigFile(self,configFile):
    import json
    if not os.path.exists(configFile):
      print(f"ERROR: Config file does not exsist: {configFile}")
      return False
    with open(configFile) as f:
      jsonConfig = json.load(f)
      self.switcher = {}
      for slide in jsonConfig["Sounds"]:
        self.switcher[slide["ID"]] = slide["Subfolder"]
      
      
  def _get_player_cmd(self, filestr):
    if self._player_cmd is not None:
      return self._player_cmd + [filestr]

    if self.shutil.which('mpg123') is not None:
      self._player_cmd = ['mpg123', '-q']
    elif self.shutil.which('mpg321') is not None:
      self._player_cmd = ['mpg321', '-q']
    elif self.shutil.which('ffplay') is not None:
      self._player_cmd = ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet']
    else:
      raise FileNotFoundError(
        "No audio player found. Install one with: sudo apt install -y mpg123"
      )

    return self._player_cmd + [filestr]

  def set_volume(self,volume):
    m = self._get_mixer()
    if m is not None:      
      m.setvolume(volume)
      print(f"set Volume = {volume}")

  def get_volume(self):
    m = self._get_mixer()
    if m is not None:
      return m.getvolume()
    return [80]

  def volume_plus(self):
    current_vol = self.get_volume()
    if current_vol[0] <= 90:
      new_volume = current_vol[0]+5
      self.set_volume(new_volume)
      self.sleep(0.5)

  def volume_minus(self):
    current_vol = self.get_volume()
    if current_vol[0] >= 60:
      new_volume = current_vol[0]-5
      self.set_volume(new_volume)
      self.sleep(0.5)

  def timer(self,delay):
      t_now = self.time.time()
      if delay > 0:
          self.t_end = t_now+delay+0.5
      elif delay == 0:
          self.t_end = t_now
      if t_now >= self.t_end:
          return True
      else:
          return False

  def is_playing(self):
    if self.process is not None:
      return self.process.poll() is None
    return not(self.timer(-1))


  def stop_music(self):
      try:
          if self.process is not None and self.process.poll() is None:
              self.process.terminate()
          self.timer(0)
      except:
          pass
  ##        subprocess.call(['killall','mpg123'])
      return

  def load_playlist(self,musicpath):
      self.mp3files = [f for f in self.os.listdir(musicpath) if (f[-4:] == '.mp3') | (f[-4:] == '.wav')]
      self.mp3files.sort()

  def refresh_PlayList(self,ID):
      #if ID<0 or ID>9:
        #return
      Folder = self.switcher.get(ID,"")
      new_musicpath = os.path.join(self.Path,Folder)
      if (self.musicpath != new_musicpath):
        if (Folder == ""):
          print(f"ERROR: NFC ID <ID> is not defined in switcher")
          
        if not os.path.exists(new_musicpath):
          print(f"ERROR: Path does not exsist: {new_musicpath}")
          return False
        else:
          self.musicpath = new_musicpath
          self.load_playlist(self.musicpath)
          self.songnum =-1
          if self.b_print>0:
            print( "refresh playlist:: ",self.musicpath)
            for f in range(0,len(self.mp3files)):
              print ("  - ",self.mp3files[f])
            print (" ")
          return True
      else:
        return False

  def play_song(self,IND):  
      if self.songnum == IND:                
        self.stop_music()
        self.songnum = -1
        return

      self.stop_music()
      
      if (IND>=len(self.mp3files)):
          print("too many files:: IND = ",IND," numel(mp3files) = ",len(self.mp3files))
##          all_lights_out()
##          alert(3)
          return
      mp3file = self.mp3files[IND]
      filestr = os.path.join(self.musicpath,mp3file)
      print(filestr+" ; ")
      cmd = self._get_player_cmd(filestr)
      self.process = self.subprocess.Popen(cmd)
      mp3len = self.get_mp3_length(filestr)
      self.timer(mp3len)
      self.PID = self.process.pid
      if self.b_print>0:
          print(" ... '",mp3file,"' is playing","   PID=",self.PID ,"    length = ", mp3len)
      self.songnum =IND
      return

  def play_album(self,cd_num):
      self.stop_music()
      self.album_tracknum = 0
      self.Album_name = "CD"+str(cd_num+1)+"/"
      self.albumpath = self.musicpath+self.Album_name
      print(self.albumpath)
      self.load_playlist(self.albumpath)

      if (self.album_tracknum>=len(self.mp3files)):
          print("too many files:: album_tracknum = ",self.album_tracknum," numel(mp3files) = ",len(self.mp3files))
##          all_lights_out()
##          alert(3)
          return
##      mp3file = self.mp3files[self.album_tracknum]
##      filestr = self.albumpath+mp3file
##      print(filestr+" ; ")
##      cmd = ["mpg123","-q",filestr,"&"]
##      self.process = self.subprocess.Popen(cmd)
##      mp3len = self.get_mp3_length(filestr)
##      self.timer(mp3len)
##      self.PID = self.process.pid
##      if b_print>0:
##          print " ... '",mp3file,"' is playing","   PID=",self.PID ,"    length = ", mp3len
      self.play_track()
      self.songnum =cd_num
      return

  def skip_track(self,direction):
    #print(self.album_tracknum)
    if (direction == -1) & (self.album_tracknum>0) :
      self.album_tracknum += direction
    elif (direction ==  1) & (self.album_tracknum<(len(self.mp3files)-1)) :
      self.album_tracknum += direction
    else:
      return
    self.play_track()
    #print(self.album_tracknum)
    return

  def play_track(self):
    self.stop_music()

    mp3file = self.mp3files[self.album_tracknum]
    filestr = self.albumpath+mp3file
    print(filestr+" ; ")
    cmd = self._get_player_cmd(filestr)
    self.process = self.subprocess.Popen(cmd)
    mp3len = self.get_mp3_length(filestr)
    self.timer(mp3len)
    self.PID = self.process.pid
    if self.b_print>0:
        print(f" ... '{mp3file}' is playing  [ PID={self.PID}  |  length = {mp3len} ]")
    #self.songnum =IND
    return

  def get_mp3_length(self,Filename):
##    print(Filename)
    if self.MP3 is None:
      return 0
    audio = self.MP3(Filename)
    return (audio.info.length)
