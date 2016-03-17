from os import listdir as list_files
from flask import Flask, render_template, redirect, url_for, send_from_directory
app = Flask(__name__)

state = 'ready:file'


@app.route('/')
def control_panel():
    files = list_files('./static/assets/')
    return render_template('control.html', files=files)


@app.route('/overlay')
def overlay():
    return render_template('overlay.html')


@app.route('/state')
def return_state():
    global state
    print('Current state: {}'.format(state))
    return state


@app.route('/request/<new_state>/<new_file>')
def request_state(new_state, new_file):
    global state
    current_state = state.split(':')[0]
    if current_state == 'ready' or new_state == 'ready':
        print('Entering new state: {}'.format(new_state + ':' + new_file))
        state = new_state + ':' + new_file
    return redirect(url_for('control_panel'))


@app.route('/reset_state')
def reset_state():
    print('State reset to ready')
    global state
    state = 'ready:none'
    return ''


if __name__ == '__main__':
    app.run(debug=True)
