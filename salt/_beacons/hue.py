# -*- coding: utf-8 -*-
'''
Beacon to emit hue status
'''

# Import Python libs
from __future__ import absolute_import
import logging

# Import Salt libs
import salt.utils

# Import Hue Lib
try:
    from phue import Bridge
    HAS_HUE = True
except ImportError:
    HAS_HUE = False

log = logging.getLogger(__name__)

__virtualname__ = 'hue'


def __virtual__():
    if HAS_HUE:
        return __virtualname__
    else:
        return False


def validate(config):
    '''
    Validate the beacon configuration
    '''

    if not isinstance(config, list):
        return False, 'Configuration for hue beacon must be a list.'

    for item in config:
        if not isinstance(item, dict):
            return False, 'Configuration key for hue beacon must be a dict.'
        if 'bridges' in item:
            for ip, data in item['bridges'].items():
                has_username = data.get('username', False)
                if not has_username:
                    return False, 'Username must be present for bridge {0}'.format(ip)

    return True, 'Valid beacon configuration'

def beacon(config):
    '''
    Emit the status of all lights connected on the bridge.

    Bridge information specify in beacons.conf

    .. code-block:: yaml

        beacons:
          hue:
            127.0.0.1:
              username: blabla
    '''
    log.trace('load beacon starting')


    ret = []

    bridges = {}
    for item in config:
        if 'bridges' in item:
            bridges = item['bridges']

    for ip, data in bridges.items():
        username = data.get('username')

        bridge = Bridge(ip=ip, username=username)

        bridge_data = {
            'ip': ip,
            'lights': {}
        }


        should_append = False
        for light in bridge.lights:
            light_id = light.light_id
            status = bridge.get_light(light_id, 'on')
            if not status:
                should_append = True
                bridge_data['lights'][light_id] = status
        if should_append:
            ret.append(bridge_data)
        
    return ret
