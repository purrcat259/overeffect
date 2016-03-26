import wave
from mutagen.mp3 import MP3
from os import listdir as list_files
from PIL import Image, ImageSequence
from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

files_data = []
default_timeout = 3
state = 'ready:file:{}'.format(default_timeout)
image_types = ['png', 'jpg', 'bmp']
audio_types = ['wav', 'mp3', 'ogg']
video_types = ['mp4']


# Web server routes

@app.route('/')
def control_panel():
    global files_data
    return render_template('control.html', files_data=files_data)


@app.route('/overlay')
def overlay():
    return render_template('overlay.html')


# Getters routes

@app.route('/state')
def return_state():
    global state
    print('Current state: {}'.format(state))
    return state

# Setters routes


@app.route('/rebuild_filelist')
def rebuild_filelist():
    build_file_list()
    return redirect(url_for('control_panel'))


@app.route('/request/<new_state>/<new_file>')
def request_state(new_state, new_file):
    global state
    current_state = state.split(':')[0]
    if current_state == 'ready' or new_state in ['ready', 'interrupt']:
        global files_data
        state = new_state + ':' + new_file + ':' + str(return_file_data(new_file)['duration'])
        print('Entering new state: {}'.format(state))
    return redirect(url_for('control_panel'))


@app.route('/set_busy_state/<something>')
def set_busy(something):
    print('Now busy showing {}'.format(something))
    global state
    state = 'busy:{}:busy'.format(something)
    return ''


# Used to clear up whatever is going on now before moving to ready state
@app.route('/set_clear_state/<int:return_location>')
def set_clear(return_location):
    print('Now clearing all content')
    global state
    state = 'clear:clear:clear'
    # 0 for redirect to control panel (used by button)
    # 1 for empty return (used by overlay)
    if return_location == 0:
        return redirect(url_for('control_panel'))
    if return_location == 1:
        return ''


@app.route('/reset_state')
def reset_state():
    print('State reset to ready')
    global state
    state = 'ready:none:{}'.format(default_timeout)
    return ''


# File methods below here

def return_file_data(file_name):
    global files_data
    return [file for file in files_data if file['full_name'] == file_name][0]


def build_file_list():
    print('Building file list')
    global files_data
    files = list_files('./static/assets/')
    # reset the variable here to avoid ghost files
    files_data = []
    # set data
    for file in files:
        current_file = dict()
        current_file['path'] = './static/assets/' + file
        current_file['full_name'] = file
        current_file['name'] = file.split('.')[0]
        current_file['extension'] = file.split('.')[1]
        current_file['duration'] = ''
        if current_file['extension'] == 'gif':
            current_file['type'] = 'gif'
            # if it is a gif, set the duration
            # TODO: Add durations for all other file types
            current_file['duration'] = return_gif_duration(file)
        if current_file['extension'] in audio_types:
            current_file['type'] = 'audio'
            current_file['duration'] = return_audio_duration(file)
        elif current_file['extension'] in video_types:
            current_file['type'] = 'video'
        elif current_file['extension'] in image_types:
            current_file['type'] = 'image'

        files_data.append(current_file)


def return_gif_duration(gif):
    # Open the gif
    img = Image.open('./static/assets/' + gif)
    durations = []
    # Store the duration amount of every frame
    for frame in ImageSequence.Iterator(img):
        durations.append(frame.info['duration'])
    # divide by 1000 for seconds (durations are in ms)
    duration = sum(durations) / 1000
    print('\t' + gif + ' is ' + str(duration) + ' seconds long')
    return str(duration)


def return_audio_duration(audio_file):
    extension = audio_file.split('.')[-1]
    # for WAV files:
    # Adapted from: https://stackoverflow.com/questions/7833807/get-wav-file-length-or-duration
    if extension == 'wav':
        with wave.open('./static/assets/' + audio_file, 'r') as file:
            frames = file.getnframes()
            rate = file.getframerate()
            duration = round(frames / float(rate), 2);
            print('\t' + audio_file + ' is ' + str(duration) + 's long')
        return duration
    elif extension == 'mp3':
        audio = MP3('./static/assets/' + audio_file)
        duration = round(audio.info.length, 2)
        print('\t' + audio_file + ' is ' + str(duration) + 's long')
        return str(duration)


if __name__ == '__main__':
    # Cache files on startup
    build_file_list()
    app.run(host='0.0.0.0', port=5000, debug=True)
