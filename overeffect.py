from os import listdir as list_files
from PIL import Image, ImageSequence
from flask import Flask, render_template, redirect, url_for, send_from_directory
app = Flask(__name__)

default_timeout = 3
file_timings = dict()
state = 'ready:file:{}'.format(default_timeout)
audio_extensions = ['.wav', '.mp3']
image_extensions = ['.png', '.jpg']


# Web server routes

@app.route('/')
def control_panel():
    build_file_list()
    cache_gif_timings()
    global file_timings
    return render_template('control.html', files_data=file_timings)


@app.route('/paneldirect')
def control_panel_direct():
    global file_timings
    return render_template('control.html', files_data=file_timings)


@app.route('/overlay')
def overlay():
    return render_template('overlay.html')


@app.route('/state')
def return_state():
    global state
    print('Current state: {}'.format(state))
    return state


@app.route('/request/<new_state>/<new_file>/<time_out>')
def request_state(new_state, new_file, time_out):
    global state
    current_state = state.split(':')[0]
    if current_state == 'ready' or new_state == 'ready':
        state = new_state + ':' + new_file + ':' + time_out
        print('Entering new state: {}'.format(state))
    return redirect(url_for('control_panel_direct'))


@app.route('/reset_state')
def reset_state():
    print('State reset to ready')
    global state
    state = 'ready:none:{}'.format(default_timeout)
    return ''


# Methods below here

def build_file_list():
    print('Building file list')
    global file_timings
    files = list_files('./static/assets/')
    # do only non gifs in this method
    nongifs = [file for file in files if not file.endswith('.gif')]
    for file in nongifs:
        file_timings[file] = 0.0


def cache_gif_timings():
    print('Caching file timings')
    global file_timings  # get the global variable
    files = list_files('./static/assets/')
    # Filter for gifs
    gifs = [file for file in files if file.endswith('.gif')]
    for gif in gifs:
        # Open the gif
        img = Image.open('./static/assets/' + gif)
        durations = []
        # Store the duration amount of every frame
        for frame in ImageSequence.Iterator(img):
            durations.append(frame.info['duration'])
        # divide by 1000 for seconds (durations are in ms)
        duration = sum(durations) / 1000
        # store it in the timings dict
        file_timings[gif] = duration
        print(gif + ' is ' + str(duration) + ' seconds long')


if __name__ == '__main__':
    app.run(debug=True)
