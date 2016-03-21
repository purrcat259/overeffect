from os import listdir as list_files
from PIL import Image, ImageSequence
from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

files_data = []
default_timeout = 3
state = 'ready:file:{}'.format(default_timeout)


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


@app.route('/request/<new_state>/<new_file>/<time_out>')
def request_state(new_state, new_file, time_out):
    global state
    current_state = state.split(':')[0]
    if current_state == 'ready' or new_state in ['ready', 'interrupt']:
        state = new_state + ':' + new_file + ':' + time_out
        print('Entering new state: {}'.format(state))
    return redirect(url_for('control_panel'))


@app.route('/set_busy_state')
def set_busy():
    print('Now busy showing something')
    global state
    state = 'busy:busy:busy'
    return ''


@app.route('/reset_state')
def reset_state():
    print('State reset to ready')
    global state
    state = 'ready:none:{}'.format(default_timeout)
    return ''


# File methods below here

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
        if current_file['extension'] == 'gif':
            # if it is a gif, set the duration
            # TODO: Add durations for other file types
            current_file['duration'] = return_gif_duration(file)
        else:
            current_file['duration'] = '0.0'
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


if __name__ == '__main__':
    # Cache files on startup
    build_file_list()
    app.run(host='0.0.0.0', port=5000, debug=True)
