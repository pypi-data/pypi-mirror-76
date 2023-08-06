#!/usr/bin/python3
"""
Application to Record, Secure, and Transfer Clinical Therapy Video

John Poncini
Video and Informatics Systems Associate
MAPS Public Benefit Corporation
"""

import os
import json

from threading import Thread
from time import sleep

from flask import (
    Flask, jsonify, render_template, request, 
    url_for, redirect, send_from_directory
)

from tools import util
from mpbc import info


app = Flask(__name__)
program = info.Program
recording = util.Recording()
default = info.Default()
session = info.Session()
device = info.Device()
pin = util.PIN()
usb = util.USB()
ssids = util.get_network_ssids()
SITE = default.SITE
connected=False
upload_status=False


def authorize(func):
    """
    Authorizes the user to perform the system functions 
    """
    def wrapper(*args, **kwargs):
        print('Authorized')
        if not session.is_authorized():
            return render_pin()
        return func(*args, **kwargs)
    return wrapper


def config(func):
    """
    Configuration check
    """
    def wrapper(*args, **kwargs):
        if device.is_configured():
            template = render_pin()
        else:
            template = config.next()
        return func(*args, **kwargs)
    return wrapper


@authorize
def render_index():
    """
    Renders the index page with the default parameters
    """
    if usb.data['type'] == 'TREK':
        recording = util.Recording()
        default = info.Default()
        return render_template(
            'index.html',
            sidebar = device.get_sidebar(),
            name = 'record',
            studies = session.data['study_ids'],
            visits = program.VISITS,
            participants = program.PARTICIPANTS,
            study = session.data['last_study_id'],
            participant = session.data['last_subject_id'],
            visit = session.data['last_visit_id']
        )
    elif usb.data['type'] == 'WEST':
        return render_template(
            'select_network.html',
            name = 'network',
            ssid = device.SSID,
            ssids = util.get_network_ssids(),
            sidebar = device.get_sidebar('config')
        )


def render_pin(incorrect_pin=False):
    """
    Renders the PIN entry page
    """
    return render_template(
        'enter_pin.html',
        incorrect_pin = incorrect_pin,
        remaining_attempts = pin.attempt_counter
    )


@app.route('/favicon.ico', methods = ['GET'])
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 
        'favicon.ico', mimetype='image/vnd.microsoft.icon'
    )


@app.route('/')
def root():
    """
    ADAM Initialization
    """
    util.notify_sponsor(
        'ADAM online',
        program.SITES[default.SITE][0] + ' has a device online.'
    )
    return render_template('usb_key.html')


@app.route('/check_usb')
def check_usb():
    """
    TREK Authorization funciton
    """
    if usb.is_storage_device_attached():
        usb.mount()
        sleep(1)
        usb.decrypt()
        return jsonify(verified=usb.verified), 202
    else:
        return jsonify(attached_device=False), 500


@app.route('/unlock')
def unlock():
    """
    Authorizes an End User session 

    Configures Authentication protocol
    """
    usb.authorize()
    sleep(3)
    session.authorize()
    if not session.data['PIN']:
        return render_template(
            'setup_pin.html',
            different_pins = False
        )
    else:
        pin.configure(session.data['PIN'])
        return render_pin()


@app.route('/lock')
def lock():
    """
    Deauthorizes an End User session

    Locks ADAM functions
    """
    util.notify_sponsor(
            'Session Logout',
            session.data['first_name'] + ' ' + session.data['last_name'] +
            ' has logged out at ' + program.SITES[default.SITE][0] + '.'
        )
    session.deauthorize()
    return render_template('usb_key.html')


@app.route('/home')
def home():
    """
    Renders the index page
    """
    return render_index()


@app.route('/check_config')
def check_config():
    """
    TREK PIN Configuration Check
    """
    session.deauthorize()
    device = info.Device()
    if device.is_configured():
        return render_pin()
    elif device.CSTATUS == 'factory':
        return render_template('welcome.html')
    else:
        return render_template(
            'resume_config.html',
            resume_from = device.CSTATUS
        )


@app.route('/enter_pin')
def enter_pin():
    """
    Returns the enter a PIN page
    """
    return render_pin()


@app.route('/check_pin', methods = ['GET'])
def check_pin():
    """
    TREK Authentication function
    """
    entered_pin = request.args.get('entered_pin')
    pin.authenticate(entered_pin)
    return '200'


@app.route('/setup_pin', methods = ['GET'])
def setup_pin():
    """
    TREK PIN Configuration
    """
    entered_pin = request.args.get('entered_pin')
    device.write_pin(entered_pin)
    return '200'


@app.route('/confirm_pin', methods = ['GET'])
def confirm_pin():
    """
    TREK PIN Configuration Confirmation
    """
    entered_pin = request.args.get('entered_pin')
    device.compare_pins(entered_pin)
    return '200'


@app.route('/return_pin', methods = ['GET'])
def return_pin():
    """
    TREK Authentication
    """
    if pin.attempt_counter < 1:
        util.notify_sponsor(
            'Failed Login Attempt',
            session.data['first_name'] + ' ' + session.data['last_name'] +
            ' attempted to login with the incorrect PIN at ' +
            program.SITES[default.SITE][0] + '.'
        )
        return render_template('error.html')
    if pin.correct_pin:
        util.notify_sponsor(
            'Successful Login',
            session.data['first_name'] + ' ' + session.data['last_name'] +
            ' has logged in at ' + program.SITES[default.SITE][0] + '.'
        )
        return render_index()
    return render_pin(True)


@app.route('/verify_pin', methods = ['GET'])
def verify_pin():
    return render_template('verify_pin.html')


@app.route('/compare_pins', methods = ['GET'])
def compare_pins():
    if device.pins_match:
        hashed_pin = util.generate_hashes('sha512sum', device.PIN.encode())
        session.update_session(PIN = hashed_pin)
        session.update_user()
        util.encrypt_user_data(
            session.data['user_id'],
            session.data['secret']
        )
        util.notify_sponsor(
            'Successful PIN Setup',
            session.data['first_name'] + ' ' + session.data['last_name'] +
            ' has setup an account at ' + program.SITES[default.SITE][0] + '.'
        )
        return render_index()
    else:
        return render_template(
            'setup_pin.html',
            different_pins = True
        )


@app.route('/complete_pin', methods = ['GET'])
def complete_pin():
    return render_template(
        'confirm_pin.html',
        sidebar = device.get_sidebar('config')
    )


@app.route('/matched_pins', methods = ['GET'])
def matched_pins():
    if device.pins_match:
        if device.is_configured():
            return render_template(
                'config_menu.html'
            )
        else:
            return render_template(
                'successfully_configured.html'
            )
    else:
        return render_template(
            'configure_pin.html',
            name = 'pin',
            sidebar = device.get_sidebar('config')
        )


#@authorize
@app.route('/navigation', methods=['GET'])
def navigation():
    btn = request.args.get('btn')
    if btn == 'continue':
        return render_index()
    elif btn == 'back':
        return render_pin()


@app.route('/start_configuration', methods=['GET'])
def start_configuration():
    device.toggle_sbar('open')
    return render_template(
        'select_network.html',
        name = 'network',
        ssids = util.get_network_ssids(),
        sidebar = device.get_sidebar('config')
    )


@app.route('/complete_configuration', methods=['GET'])
def complete_configuration():
    device.toggle_sbar('closed')
    device.configure()
    print(device.PIN)
    pin = util.PIN(device.PIN)
    return render_index()


#@authorize
@app.route('/start_recording', methods=['POST', 'GET'])
def start_recording():
    recording = util.Recording()
    btn = request.args.get('btn')
    study = request.args.get('study')
    participant = request.args.get('participant')
    visit = request.args.get('visit')
    timestamp = util.get_curtime()
    user_id = session.data['user_id']
    secret = session.data['secret']
    default = info.Default()
    config = [
        study,
        SITE,
        participant,
        visit,
        timestamp,
        str(len(recording.webcams)),
        str(len(recording.microphones))
    ]
    default.write(config)
    session.update_session(
        last_study_id = study,
        last_subject_id = participant,
        last_visit_id = visit,
        datetime = timestamp
    )
    session.update_user()
    util.encrypt_user_data(user_id, secret)

    if participant in program.PARTICIPANTS:
        if btn == 'start':
            recording.start()
            return render_template('initialize.html')
        elif btn == 'test':
            return render_template('test.html')
    else:
        return render_index()


#@authorize
@app.route('/confirm_recording', methods=['POST', 'GET'])
def confirm_recording():
    default = info.Default()
    sleep(1)
    if recording.status() == 'RUNNING':
        util.notify_sponsor(
            'Recording Started',
            '{} {} started to record {}, {} at {} at {}.'.format(
                session.data['first_name'],
                session.data['last_name'],
                default.PARTICIPANT,
                default.VISIT,
                program.SITES[default.SITE][0],
                util.convert_time(default.TIMESTAMP)
            )
        )
        return render_template('recording.html')
    else:
        return render_template('error.html')


#@authorize
@app.route('/cancel_recording', methods=['POST', 'GET'])
def cancel_recording():
    recording.stop()
    return render_template('recording.html')


#@authorize
@app.route('/pause_recording', methods=['POST', 'GET'])
def pause_recording():
    default = info.Default()
    util.notify_sponsor(
        'Recording Paused',
        '{} {} paused the recording of {}, {} at {}.'.format(
            session.data['first_name'],
            session.data['last_name'],
            default.PARTICIPANT,
            default.VISIT,
            util.convert_time(util.get_curtime())
        )
    )
    recording.stop()
    return '200'


#@authorize
@app.route('/resume_recording', methods=['POST', 'GET'])
def resume_recording():
    default = info.Default()
    config = [
        default.STUDY ,
        default.SITE,
        default.PARTICIPANT ,
        default.VISIT ,
        util.get_curtime(),
        str(len(recording.webcams)),
        str(len(recording.microphones))
    ]
    default.write(config)
    util.notify_sponsor(
        'Recording Resumed',
        '{} {} resumed recording {}, {} at {}.'.format(
            session.data['first_name'],
            session.data['last_name'],
            default.PARTICIPANT,
            default.VISIT,
            util.convert_time(default.TIMESTAMP)
        )
    )
    recording.start()
    return '200'


#@authorize
@app.route('/stop_recording', methods=['POST', 'GET'])
def stop_recording():
    default = info.Default()
    util.notify_sponsor(
        'Recording Stopped',
        '{} {} stopped recording {}, {} at {}.'.format(
            session.data['first_name'],
            session.data['last_name'],
            default.PARTICIPANT,
            default.VISIT,
            util.convert_time(util.get_curtime())
        )
    )
    recording.stop()
    Thread(target = recording.encrypt).start()
    return render_index()


@app.route('/toggle_sidebar', methods=['GET'])
def toggle_sidebar():
    state = request.args.get('state')
    device.toggle_sbar(state)
    return '200'


@app.route('/menu', methods=['GET'])
def select_menu():
    btn = request.args.get('btn')
    if btn == 'test':
        return render_template
            'test.html',
            name = 'test',
            ssids = util.get_network_ssids(),
            sidebar = device.get_sidebar()
        )
    elif btn == 'config':
        return render_template(
            'select_network.html',
            name = 'network',
            ssids = util.get_network_ssids(),
            sidebar = device.get_sidebar('config')
        )
    elif btn == 'help':
        return render_template(
            'help.html',
            name = 'overview',
            index = 0,
            sidebar = device.get_sidebar('help')
        )
    elif btn == 'lock':
        return redirect(url_for('lock'))
    else:
        return render_index(


@app.route('/config_submenu', methods=['GET'])
def select_config_submenu():
    btn = request.args.get('btn')
    if btn == 'home':
        return render_index()
    elif btn == 'site':
    elif btn =
    menu = {
        'home' : render_index(),
        'site' : render_template(
            'select_site.html',
            name = 'site',
            configured = device.is_configured(),
            sites = program.SITES,
            site = default.SITE,
            sidebar = device.get_sidebar('config')
        ),
        'pin' : render_template(
            'configure_pin.html',
            name = 'pin',
            sidebar = device.get_sidebar('config')
        ),
        'back' : render_index(),
        'exit' : render_index()
    }
    return menu[btn]


@app.route('/get_wifi', methods=['POST', 'GET'])
def get_wifi():
    btn = request.args.get('btn')
    ssid = request.args.get('ssid')
    psk = request.args.get('psk')
    if btn == 'refresh':
        return render_template(
            'select_network.html',
            name = 'network',
            ssids = util.get_network_ssids(),
            sidebar = device.get_sidebar('config')
        )
    if btn == 'back':
        return render_index()
    device.write_wpa(ssid, psk)
    util.generate_wpa_supplicant(ssid, psk)
    util.connect()
    if not util.is_connected():
        return render_template(
            'select_network.html',
            name = 'network',
            ssids = util.get_network_ssids(),
            sidebar = device.get_sidebar('config')
        )
    return render_index()

@app.route('/pin_page', methods=['GET'])
def pin_page():
    return render_template(
        'configure_pin.html',
        name = 'pin',
        sidebar = device.get_sidebar('config')
    )

@app.route('/update_connection_status', methods=['GET'])
def update_connection_status():
    global connected
    if util.is_connected():
        connected = True
        return '200'
    else:
        connected = False
        return '500'


# Only used on wifi setup page so that next page load shows wifi true.
# No longer used.
@app.route('/set_connection_status', methods=['GET'])
def set_connection_status():
    status = request.args.get('status')
    global connected
    if status == 'False':
        connected = False
        return '200'
    else:
        connected = True
        return '200'
    return 500


@app.route('/setup_connection', methods=['POST', 'GET'])
def setup_connection():
    ssid = request.args.get('ssid')
    psk = request.args.get('psk')
    try:
        device.write_wpa(ssid, psk)
        util.generate_wpa_supplicant(ssid, psk)
        util.connect()
        return '200'
    except:
        return '500'


# Just used for testing
@app.route('/get_connection_variable', methods=['GET'])
def check_connection():
    global connected
    print(connected)
    if connected:
        return '200'
    else:
        return '500'


@app.route('/check_upload_status', methods=['GET'])
def check_upload_status():
    global upload_status
    if util.check_upload():
        upload_status = True
        return '200'
    else:
        upload_status = False
        return '500'


@app.route('/get_site', methods=['GET'])
def get_site():
    btn = request.args.get('btn')
    site = request.args.get('site')
    device.write_site(site)
    if btn == 'back':
        return render_template(
            'welcome.html'
        )
    elif btn == 'continue':
        return render_template(
            'select_network.html',
            name = 'network',
            ssid = device.SSID,
            ssids = util.get_network_ssids(),
            sidebar = device.get_sidebar('config')
        )


@app.route('/help_config_submenu', methods=['GET'])
def select_help_submenu():
    btn = request.args.get('btn')
    index = 0
    sidebar = device.get_sidebar('help')
    if btn == 'home':
        return render_index()
    elif btn == 'overview':
        return render_template(
            'help.html',
            name = 'overview',
            index = 0,
            sidebar = sidebar
        )
    elif btn == 'connections':
        return render_template(
            'help.html',
            name = 'connections',
            index = 1,
            sidebar = sidebar
        )
    elif btn == 'network':
        return render_template(
            'help.html',
            name = 'network',
            index = 2,
            sidebar = sidebar
        )
    elif btn == 'auth':
        return render_template(
            'help.html',
            name = 'auth',
            index =3,
            sidebar = sidebar
        )
    elif btn == 'record':
        return render_template(
            'help.html',
            name = 'record',
            index = 4,
            sidebar = sidebar
        )
    elif btn == 'upload':
        return render_template(
            'help.html',
            name = 'upload',
            index = 5,
            sidebar = sidebar
        )
    else: 
        return render_index()


@app.route('/shutdown', methods=['GET'])
    util.shutdown()
    return '200'


@app.route('/enlighten', methods=['GET'])
def enlighten():
    util.illuminate()
    return '200'

def main():
    app.run()

@app.context_processor
def inject_variables():
    return dict(
        wifi=connected,
        uploading=upload_status,
        initials=session.initials
    )

if __name__ == '__main__':
    main()
