#!/usr/bin/python3
""" Utility Classes and Functions """

import os.path
import socket
import subprocess as sp
from threading import Thread
from datetime import datetime
from time import strftime, gmtime

import boto3
import pyudev
from flask import render_template, request


class Recording:
    """
    Simple class for Recording
    """

    def __init__(self):
        """
        Initializes the peripheral recording equipment
        """
        self.webcams = []
        self.microphones = []

        devices = sp.Popen(['arecord', '-l'], stdout=sp.PIPE).communicate()[0]
        for device in devices.rstrip().decode().split('\ncard ')[1:]:
            hw, name = device.split(':')[:2]
            if 'C920' in name:
                self.webcams.append(int(hw))
            elif 'AT2020USBi' in name:
                self.microphones.append(int(hw))


    def start(self):
        """
        Starts a recording process
        """
        sp.Popen(
            [   '/usr/local/bin/supervisorctl', 
                'start', 'record'
            ], 
            stdout=sp.PIPE
        )


    def status(self):
        """
        Returns the status of the recording process
        """
        child = sp.Popen(
            [   '/usr/local/bin/supervisorctl', 
                'status', 'record'
            ], 
            stdout=sp.PIPE
        )
        status = child.communicate()[0].decode().split()[1]
        return status


    def stop(self):
        """
        Stops the recording process
        """
        pid = self.get_pid()
        sp.Popen(['sudo', 'kill', pid], stdout=sp.PIPE)
        sp.Popen(
            [   '/usr/local/bin/supervisorctl',
                'stop', 'record'
            ],
            stdout=sp.PIPE
        )


    def encrypt(self): 
        """
        Packages and encrypts the resultant media files
        """
        sp.Popen(
            [   '/usr/local/bin/supervisorctl',
                'start', 'encrypt'
            ],
            stdout=sp.PIPE
        )


    def get_pid(self):
        """
        Gets and returns ffmpeg pid
        """
        child = sp.Popen(['pidof', 'ffmpeg'], stdout=sp.PIPE)
        return child.communicate()[0].strip()



class PIN:
    """
    Class for storing and checking user PINs
    """

    def __init__(self):
        """
        """
        self.correct_pin = False
        self.pin = None
        self.attempt_counter = 5

    
    def configure(self, pin):
        self.pin = pin


    def authenticate(self, entered_pin):
        """
        Checks if the entered pin is the correct pin
        """
        hashed_pin = generate_hashes('sha512sum', entered_pin.encode())
        if self.attempt_counter == 0:
            self.correct_pin = False
        elif hashed_pin == self.pin:
            self.correct_pin = True
            self.reset_counter()
        else:
            self.correct_pin = False
            self.attempt_counter -= 1
        return self.correct_pin


    def reset_counter(self):
        self.attempt_counter = 5



class USB:
    """
    Class for USB utilities
    """
    def __init__(self):
        """
        """
        self.context = pyudev.Context()
        self.verified = False
        self.data = {
            'type' : None,
            'user_id' : None,
            'secret' : None,
            'aws_access_key_id' : None,
            'aws_secret_access_key' : None
        }
        self.dev_name = '/dev/sda'
        self.partition = 2
        usb_monitor = Thread(target=self._monitor)
        usb_monitor.start()


    def _monitor(self):
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='block')
        self.monitor.start()
        for device in iter(self.monitor.poll, None):
            if device.action == 'add' and device.get('DEVTYPE') == 'disk':
                self.dev_name = device.get('DEVNAME')


    def is_storage_device_attached(self):
        devices = {dev.get('DEVNAME') for dev in self.context.list_devices()}
        return self.dev_name in devices


    def mount(self):
        sp.Popen(
            ['sudo', 'mount', self.dev_name + str(self.partition), '/mnt/key'],
            stdout=sp.PIPE
        )


    def umount(self):
        sp.Popen(['sudo', 'umount', '/mnt/key'], stdout=sp.PIPE)


    def decrypt(self):
        child = sp.Popen(
            [
                'sudo', 'openssl', 'rsautl', '-decrypt', 
                '-inkey', '/etc/keys/usb/private.key', 
                '-in', '/mnt/key/bin.enc'
            ],
            stdout=sp.PIPE
        )
        user_key = child.communicate()[0].strip().decode().splitlines()
        self.verify(user_key[1])
        if self.verified:
            self.data['type'] = user_key[0].split('=')[1]
            self.data['secret'] = generate_hashes(
                'sha512sum', 
                user_key[2].split('=')[1].encode()
            )
            for line in user_key[3:]:
                key, value = line.split('=')
                self.data[key] = value
            


    def verify(self, user_id):
        if 'user_id' in user_id:
            self.data['user_id'] = user_id.split('=')[1]
            file = '/etc/opt/adam/users/'+ self.data['user_id'] +'.conf'
            if os.path.exists(file):
                self.verified = True


    def authorize(self):
        key = 'aws_access_key_id'
        secret = 'aws_secret_access_key'
        sp.Popen(
            [
                'sudo', '/usr/bin/openssl', 'enc', '-aes-256-cbc', '-d',
                '-in', '/etc/opt/adam/users/' + self.data['user_id'] + '.conf',
                '-out', '/tmp/session.conf', '-k', self.data['secret']
            ],
            stdout=sp.PIPE
        )
        with open('/home/pi/.aws/credentials', 'w') as credentials:
            credentials.write('[default]\n')
            credentials.write(key + ' = ' + self.data[key] + '\n')
            credentials.write(secret + ' = ' + self.data[secret] + '\n')


def notify_sponsor(subject, message):
    with open('/etc/opt/adam/disclaimer.txt', 'r') as d:
        disclaimer = d.read()
    try:
        client = boto3.client('sns', region_name='us-west-2')
        response = client.publish(
            TopicArn = 'arn:aws:sns:us-west-2::ADAM_notification',
            Subject = 'SERPENT: ' + subject,
            Message = message + disclaimer
        )
    except:
        pass


def illuminate():
    child = sp.Popen(
        ['sudo', 'rpi-backlight', '--get-brightness'],
        stdout=sp.PIPE
    )
    if child.communicate()[0].strip().decode() == '5':
        sp.Popen(
            ['sudo', 'rpi-backlight', '--set-brightness', '100'],
            stdout=sp.PIPE
        )
    else:
        sp.Popen(
            ['sudo', 'rpi-backlight', '--set-brightness', '5'],
            stdout=sp.PIPE
        )


def generate_hashes(function, secret_key):
    """
    Generates a hash 
    """
    child = sp.Popen(function, stdout=sp.PIPE, stdin=sp.PIPE)
    return child.communicate(input=secret_key)[0].decode().split(' ')[0]


def encrypt_user_data(user_id, secret):
    """
    Encrypts user data with a key to the user file.
    """
    sp.Popen(
        [
            'sudo', 'openssl', 'enc', '-aes-256-cbc', '-e', '-salt',
            '-in', '/tmp/session.conf', 
            '-out', '/etc/opt/adam/users/' + user_id + '.conf',
            '-k', secret
        ],
        stdout=sp.PIPE
    )


def get_network_ssids():
    """
    Gets the network SSIDs
    """
    ssids = []
    child = sp.Popen(['iwlist', 'wlan0', 'scan'], stdout=sp.PIPE)
    for line in child.communicate()[0].decode().splitlines():    
        if line.strip().startswith('ESSID'):
            ssid = line.split('"')[1]
            if ssid != 'OutOfService':
                ssids.append(ssid)
    return ssids


def generate_wpa_supplicant(ssid, psk):
    """
    Generates a wpa_supplicant.conf file with the passed ssid and psk

    Assures the password is greater than 7 characters    
    """
    if len(psk) > 7:
        child = sp.Popen(['wpa_passphrase', ssid, psk], stdout=sp.PIPE)
        with open('/etc/wpa_supplicant/wpa_supplicant.conf', 'a') as wpa:
            for line in child.communicate()[0].decode().splitlines():
                if line.strip().startswith('#'):
                   continue
                line+='\n'
                wpa.write(line)


def check_upload():
    """
    Checks if the upload supervisorctl task is running
    """
    c = sp.Popen(
        ['/usr/local/bin/supervisorctl', 'status', 'upload'],
        stdout=sp.PIPE
    )
    s = ' '.join(c.communicate()[0].decode().strip().split()).split(' ')[1]
    return s is 'RUNNING'


def connect():
    """
    Establish a network interface
    """
    sp.Popen(
        ['/usr/local/bin/supervisorctl', 'start', 'connect'], 
        stdout=sp.PIPE
    )
    sp.Popen(
        ['/usr/local/bin/supervisorctl', 'start', 'reversessh'],
        stdout=sp.PIPE
    )


def reversessh():
    """
    Establish a reverse
    """
    sp.Popen(
        ['/usr/local/bin/supervisorctl', 'start', 'reversessh'],
        stdout=sp.PIPE
    )


def shutdown():
    sp.Popen(['sudo', 'shutdown'], stdout=sp.PIPE)


def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname("google.com")
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except:
     pass
  return False


def get_curtime():
    return strftime("%Y%m%d-%H%M%S", gmtime())


def convert_time(timestamp):
    time = datetime.strptime(timestamp, '%Y%m%d-%H%M%S')
    return time.strftime('%-I:%M:%S %p GMT on %A, %d %B %Y')


def app_version():
    pip = sp.Popen(["pip3", "freeze"], stdout=sp.PIPE)
    ver, er = pip.communicate()
    pos = str(ver).find('mapsadam') + 10
    return str(ver)[pos:pos+10].split("\\", 1)[0]
