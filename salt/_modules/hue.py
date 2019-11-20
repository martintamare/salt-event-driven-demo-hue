# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Import Python libs
import logging
import random

# Import salt libs
#import salt.utils.compat
#import salt.utils.odict as odict

from salt.exceptions import CommandExecutionError

logger = logging.getLogger(__name__)

# Import third party libs
try:
    from phue import Bridge
    HAS_HUE = True
except ImportError:
    HAS_HUE = False


# Define the module's virtual name
__virtualname__ = 'hue'

def __virtual__():
    '''
    Only load if phue library exist.
    '''
    if not HAS_HUE:
        return False
    else:
        return __virtualname__


def _get_hue_username(bridge_ip):
    """Get bridge username from ip."""
    hue_config = __salt__['pillar.get']('hue_config', {})
    if bridge_ip not in hue_config:
        raise CommandExecutionError('No bridge in pillar with ip {0}'.format(bridge_ip))
    if 'username' not in hue_config[bridge_ip]:
        raise CommandExecutionError('No username in pillar for bridge {0}'.format(bridge_ip))

    return hue_config[bridge_ip]['username']


def get_lights_ids(bridge_ip):
    """Return an array with light_id."""
    username = _get_hue_username(bridge_ip)
    b = Bridge(ip=bridge_ip, username=username)
    lights_ids = []
    for light in b.lights:
        lights_ids.append(light.light_id)
    return lights_ids


def get_lights(bridge_ip):
    """Return an array with light_id."""
    username = _get_hue_username(bridge_ip)
    b = Bridge(ip=bridge_ip, username=username)
    lights = []
    for light in b.lights:
        lights.append(light.name)
    return lights


def get_light_status(bridge_ip, light_id):
    """Get status of a light."""
    username = _get_hue_username(bridge_ip)
    b = Bridge(ip=bridge_ip, username=username)
    return b.get_light(light_id, 'on')


def switch_light_on(bridge_ip, light_id):
    """Switch on a light."""
    username = _get_hue_username(bridge_ip)
    b = Bridge(ip=bridge_ip, username=username)
    b.set_light(light_id, 'on', True)
    return True


def switch_light_off(bridge_ip, light_id):
    """Switch on a light."""
    username = _get_hue_username(bridge_ip)
    b = Bridge(ip=bridge_ip, username=username)
    b.set_light(light_id, 'on', False)
    return True


def set_light(bridge_ip, light_id, 
              transitiontime=10,
              brightness=None, 
              hue=None, 
              saturation=None):
    username = _get_hue_username(bridge_ip)
    b = Bridge(ip=bridge_ip, username=username)


    if brightness is None:
        brightness = random.randint(100, 254)
    if hue is None:
        hue = random.randint(0, 65535)
    if saturation is None:
        saturation = random.randint(0, 254)

    command = {
        'transitiontime': transitiontime,
        'bri': brightness,
        'on': True,
        'hue': hue,
        'sat': saturation,
    }
    b.set_light(light_id, command)
