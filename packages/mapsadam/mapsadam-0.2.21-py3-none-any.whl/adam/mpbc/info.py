#!/usr/bin/python3
""" Information on MPBC's MDMA Program """

import boto3

from iso3166 import countries


class Session:
    """ User session information """

    def __init__(self):
        self.authorization_status = False
        self.configuration_status = False

        self.data = {
            'user_id' : None,
            'secret' : None,
            'first_name' : None,
            'last_name' : None,
            'site_ids' : {},
            'study_ids' : {},
            'PIN' : None,
            'training_status' : False,
            'last_study_id' : None,
            'last_subject_id' : '',
            'last_visit_id' : None,
            'datetime' : None
        }

        self.initials = None


    def is_authorized(self):
        return self.authorization_status


    def is_configured(self):
        return self.configuration_status


    def authorize(self):
        with open('/tmp/session.conf', 'r') as d:
            for line in d.readlines():
                key, value = line.strip().split('=')
                if key == 'study_ids' or key == 'site_ids':
                    value = self.convert_str(value)
                self.data[key] = value
            study_ids = self.data['study_ids'].copy()
            self.data['last_study_id'] = study_ids.pop()
        self.generate_user_initials()
        self.authorization_status = True


    def deauthorize(self):
        self.authorization_status = False
        self.data = {
            'user_id' : None,
            'secret' : None,
            'first_name' : None,
            'last_name' : None,
            'site_ids' : {},
            'study_ids' : {},
            'PIN' : None,
            'training_status' : False,
            'last_study_id' : None,
            'last_subject_id' : '',
            'last_visit_id' : None,
            'datetime' : None
        }

        self.initials = None


    def generate_user_initials(self):
        self.initials = self.data['first_name'][0] + self.data['last_name'][0]


    def update_user(self):
        with open('/tmp/session.conf', 'w') as s:
            for key, value in self.data.items():
                if type(value) == set:
                    value = "{'" + "', '".join(str(x) for x in value) + "'}"
                elif type(value) != str:
                    value = str(value)
                s.write(key + '=' + value + '\n')


    def update_session(self, **kwargs):
        for key, value in kwargs.items():
            self.data[key] = value


    def convert_str(self, string):
        return set(string[1:-1].replace("'",'').split(', '))


class Default:
    """ Default saved information """

    def __init__(self):
        with open('/etc/opt/adam/default.info', 'r') as d:
            data = (x.strip() for x in d.readlines()[:5])
            study, site, participant, visit, timestamp = data
        self.STUDY = study
        self.SITE = site
        self.PARTICIPANT = participant
        self.VISIT = visit
        self.TIMESTAMP = timestamp


    def write(self, config):
        with open('/etc/opt/adam/default.info', 'w') as d:
            for param in config:
                d.write(param + '\n')


class Device:

    def __init__(self):
        with open('/etc/opt/adam/device.conf', 'r') as d:
            data = (x.strip() for x in d.readlines()[:6])
            site, ssid, psk, pin, cstatus = data 
        self.SITE = site
        self.PIN = pin
        self.SSID = ssid
        self.PSK = psk
        self.CSTATUS = cstatus
        self.NIP = None
        self.pins_match = False
        self.sidebar_data = {}
        self.show_sbar = False
        self.hide_sbar = False


    def write(self):
        """
        Opens device.conf and writes class objects to the file
        """
        with open('/etc/opt/adam/device.conf', 'w') as d:
            d.write(self.SITE + '\n')
            d.write(self.SSID + '\n')
            d.write(self.PSK + '\n')
            d.write(self.PIN + '\n')
            d.write(self.CSTATUS +'\n')


    def reset(self):
        """
        Device reset function. Sets class parameters to None type
        """
        self.SITE = None
        self.SSID = None
        self.PSK = None
        self.PIN = None
        self.CSTATUS = None

        self.configure(None)


    def write_site(self, site):
        self.SITE = site
        self.configure('site')


    def write_wpa(self, ssid, psk):
        self.SSID = ssid
        self.PSK = psk
        self.configure('network')


    def write_pin(self, pin):
        self.NIP = self.PIN
        self.PIN = pin
        self.configure('pin')

    
    def compare_pins(self, entered_pin):
        if entered_pin == self.PIN:
            self.pins_match = True
            self.NIP = None
        else:
            self.PIN = self.NIP


    def configure(self, cstatus='configured'):
        self.CSTATUS = cstatus
        self.write()
        

    def is_configured(self):
        return self.CSTATUS == 'configured'


    def toggle_sbar(self, state):
        if state == 'open':
            self.show_sbar = True
        else:
            self.show_sbar = False


    def hide_sidebar(self):
        self.hide_sbar = True


    def unhide_sidebar(self):
        self.hide_sbar = False


    def get_sidebar(self, sidebar='default'):
        if sidebar == 'config':
            self.sidebar_data = {
                'active' : self.show_sbar,
                'hidden' : self.hide_sbar,
                'method' : 'select_config_submenu',
                'title' : 'Settings',
                'icon' : 'fas fa-cogs',
                'submenu' : [
                    {
                        'name' : 'pin',
                        'title' : 'PIN Configuration',
                        'icon' : 'fas fa-lock'
                    },
                    {
                        'name' : 'exit',
                        'title' : 'Exit',
                        'icon' : 'fas fa-window-close'
                    }
                ]
            }
        elif sidebar == 'help':
            self.sidebar_data = {
                'active' : self.show_sbar,
                'hidden' : self.hide_sbar,
                'method' : 'select_help_submenu',
                'title' : 'Help',
                'icon' : 'fas fa-info-circle',
                'submenu' : [
                    {
                        'name' : 'overview',
                        'title' : 'Overview',
                        'icon' : 'fas fa-info-circle'
                    },
                    {
                        'name' : 'connections',
                        'title' : 'Connections',
                        'icon' : 'fas fa-info-circle'
                    },
                    {
                        'name' : 'network',
                        'title' : 'Network',
                        'icon' : 'fas fa-wifi'
                    },
                    {
                        'name' : 'auth',
                        'title' : 'Authentication',
                        'icon' : 'fas fa-lock'
                    },
                    {
                        'name' : 'record',
                        'title' : 'Record',
                        'icon' : 'fas fa-video'
                    },
                    {
                        'name' : 'upload',
                        'title' : 'Upload',
                        'icon' : 'fa fa-upload'
                    },
                    {
                        'name' : 'exit',
                        'title' : 'Exit',
                        'icon' : 'fas fa-window-close'
                    }
                ]
            }
        else:
            self.sidebar_data = {
                'active' : self.show_sbar,
                'hidden' : self.hide_sbar,
                'method' : 'select_menu',
                'title' : 'Home',
                'icon' : 'fas fa-home',
                'submenu' : [
                    { 
                        'name' : 'record',
                        'title' : 'Record a Session',
                        'icon' : 'fas fa-video'
                    },
                    {
                        'name' : 'test',
                        'title' : 'Equipment Setup',
                        'icon' : 'fas fa-tasks'
                    },
                    {
                        'name' : 'config',
                        'title' : 'Settings',
                        'icon' : 'fas fa-cogs'
                    },
                    {
                        'name' : 'help',
                        'title' : 'Help',
                        'icon' : 'fas fa-info-circle'
                    },
                    {
                        'name' : 'lock',
                        'title' : 'Lock',
                        'icon' : 'fas fa-lock'
                    }
                ]
            }
        return self.sidebar_data



class Program:
    """ Data class to store MDMA Program information"""

    COUNTRIES = {c.name : c.alpha2 for c in countries}

    STUDIES = ['MAPP1', 'MT1', 'MAPP2', 'MT2', 'MP18', 'MAPP3']

    SITES = {
        '00' : (
            'Santa Cruz Test Site', 
            ['MAPP1', 'MT1', 'MAPP2', 'MT2', 'MP18', 'MAPP3'], 
            'us-west-1'
        ),
        '01' : (
            'Charleston', 
            ['MAPP1', 'MT1'], 
            'us-east-1'
        ),
        '02' : (
            'Boulder', 
            ['MAPP1', 'MT1'], 
            'us-west-2'
        ),
        '03' : (
            'Fort Collins', 
            ['MAPP1'], 
            'us-west-2'
        ),
        '04' : (
            'Los Angeles', 
            ['MAPP1'], 
            'us-west-1'
        ),
        '05' : (
            'New Orleans', 
            ['MAPP1'], 
            'us-east-1'
        ),
        '06' : (
            'University of California, San Francisco', 
            ['MAPP1'], 
            'us-west-1'
        ),
        '07' : (
            'San Francisco Insight and Integration Center', 
            ['MAPP1'], 
            'us-west-1'
        ),
        '09' : (
            'University of Wisconsin at Madison', 
            ['MAPP1'], 
            'us-east-2'
        ),
        '10' : (
            'New York University',
            ['MAPP1'],
            'us-east-1'
        ),
        '11' : (
            'Affective Care', 
            ['MAPP1'],
            'us-east-1'
        ),
        '12' : (
            'Boston',
            ['MAPP1'],
            'us-east-1'
        ),
        '13' : (
            'University of British Columbia',
            ['MAPP1'],
            'ca-central-1'
        ),
        '14' : (
            'Dr. Simon Amar, LLC', 
            ['MAPP1'], 
            'ca-central-1'
        ),
        '15' : (
            'Beer Yaakov',
            ['MAPP1'], 
            'me-south-1'
        ),
        '16' : (
            'Tel Hashomer',
            ['MAPP1'],
            'me-south-1'
        ),
        '17' : (
            'Cardiff',
            ['MP18'],
            'eu-central-1'
        ),
        '18' : (
            'Leiden/Oegstgeest',
            ['MP18'],
            'eu-central-1'
        ),
        '19' : (
            'Maastricht',
            ['MP18'],
            'eu-central-1'
        ),
        '20' : (
            'Prague',
            ['MP18'],
            'eu-central-1',
        ),
        '22' : (
            'Portugal',
            ['MP18'],
            'eu-central-1'
        ),
        '23' : (
            'Norway',
            ['MP18'],
            'eu-central-1'
        ),
        '24' : (
            'Berlin',
            ['MP18'],
            'eu-central-1'
        ),
        '26' : (
            'Finland',
            ['MP18'],
            'eu-central-1'
        ),
        '30' : (
            'Santa Fe', 
            ['MT1', 'MT2'], 
            'us-west-1'
        )
    }

    VISITS =  [
        'V01',
        'V02',
        'V04',
        'V05',
        'V06',
        'V07',
        'V09',
        'V10',
        'V11',
        'V12',
        'V14',
        'V15',
        'V16',
        'V17',
        'V18',
        'V20'
    ]

    PARTICIPANTS = {
        '{:02}{:02}0{:02}'.format(study, site, participant) \
        for study in {11, 12, 13, 16, 17, 18} \
        for site in range(1, 40) \
        for participant in range(1, 99)
    }

    PARTICIPANTS = PARTICIPANTS.union({'TEST', 'PARTD', 'TOAD'})
