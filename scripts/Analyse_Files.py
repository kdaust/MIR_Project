#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 21:54:33 2022

@author: kiridaust
"""

import requests
import configparser
import json
import pandas as pd
from pandas import json_normalize 
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile
import wave
import sounddevice as sd
from scipy.signal import savgol_filter
from fuzzywuzzy import fuzz
import os
import pyrle
import math
import vamp

def calc_redundancy(audio,sr, filter_size = 7, remove_len = 5, base_pattern_length = 5):
    audio = np.ndarray.flatten(audio)
    audio = np.asarray(audio).astype('float32')
    data = vamp.collect(audio, sr, "mtg-melodia:melodia")
    hop, melody = data['vector']
    melody_pos = melody[:]
    melody_pos[melody<=0] = None
    mel_norest = melody_pos[~np.isnan(melody_pos)]
    ##plt.plot(mel_norest)
    result = savgol_filter(mel_norest, filter_size, 5)
    pt4 = np.where(result==0, 1, result)
    float_midi = 69 + 12*np.log2(pt4/440.)
    int_midi = np.array([round(x) for x in float_midi])

    for (i,f) in enumerate(float_midi): 
        if f < 40: 
            float_midi[i] = 0 
            int_midi[i] = 0 

    rle = pyrle.Rle(int_midi)
    rle_vals = rle.values
    rle_runs = rle.runs
    final_notes = rle_vals[rle_runs > remove_len]
    note_diff = np.ediff1d(final_notes)
    note_diff = note_diff + abs(min(note_diff))
    note_diff = note_diff.astype(int)

    numnotes = len(note_diff)
    breaks = np.arange(0,numnotes,base_pattern_length)
    res = np.zeros(0)
    for i in range(0,len(breaks)-1):
        base_pattern = note_diff[breaks[i]:breaks[i+1]]
        bpstr = ''.join(map(str, base_pattern))
        for j in range(i+1, len(breaks)-1):
            p2str = ''.join(map(str, note_diff[breaks[j]:breaks[j+1]]))
            res = np.append(res,fuzz.ratio(bpstr,p2str))
    return(np.mean(res), np.std(res))

SAMPLE_RATE = 44100
sd.default.device = 9
# recording = sd.rec( int(SECONDS * SAMPLE_RATE), samplerate = SAMPLE_RATE, channels = 1)
# sd.wait()  # Waits for recording to finish
# sd.play(recording, int(SAMPLE_RATE))
# scipy.io.wavfile.write('recording1.wav', int(SAMPLE_RATE), recording)

scope = "user-library-read user-modify-playback-state user-read-playback-state"
    
songs = pd.read_csv('~/Desktop/MIR_Project/scripts/pop.csv')
#sp.start_playback(uris = ["spotify:track:6nYoTBmGFNgfTyRC8x1Fvp"])

songs1 = songs.loc[170:200]
songs_test = songs.loc[1:3]

sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                scope=scope,
                redirect_uri="https://thebeczone.ca/shiny/ccissdev/",
                client_id="3893dbdca69044e6aae96aaff3c25d68",
                client_secret="e953cb2d3b7f4e778cc4a5c8f458c9a1",
                show_dialog=True,
                cache_path="token.txt"),
                requests_timeout=10, 
                retries=10
        )

results_mean = []
results_sd = []
results_index = []
for index, row in songs1.iterrows():
    song_id = row['uri']
    try:
        RECORD_SECONDS = int(sp.audio_features(tracks = [song_id])[0]['duration_ms']/1000)
    except:
        sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                scope=scope,
                redirect_uri="https://thebeczone.ca/shiny/ccissdev/",
                client_id="3893dbdca69044e6aae96aaff3c25d68",
                client_secret="e953cb2d3b7f4e778cc4a5c8f458c9a1",
                show_dialog=True,
                cache_path="token.txt"),
                requests_timeout=10, 
                retries=10
        )
        RECORD_SECONDS = int(sp.audio_features(tracks = [song_id])[0]['duration_ms']/1000)
    print("Song " + str(index))
    print ("recording started")
    sp.start_playback(uris = [song_id])
    recording = sd.rec( int(RECORD_SECONDS * SAMPLE_RATE), samplerate = SAMPLE_RATE, channels = 1)
    sd.wait()  # Waits for recording to finish
    print ("recording stopped")
    print(np.max(recording))
    ##scipy.io.wavfile.write("Test_Song_"+str(index)+".wav",44100,recording)
    try:
        metric = calc_redundancy(recording,44100,filter_size=25)
        results_mean.append(metric[0])
        results_sd.append(metric[1])
        results_index.append(index)
        print("Redundancy = " + str(metric[0]))
    except:
        print("Didn't work")
    del(recording)

all_res = np.array([results_index,results_mean,results_sd])
all_res = np.transpose(all_res)
np.savetxt("Pop_results_170_200.csv", all_res, delimiter= ',')
#mean_np = np.array(results)