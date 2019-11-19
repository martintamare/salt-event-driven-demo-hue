# -*- coding: utf-8 -*-
'''
Module for running alkivi custom functions
'''
from __future__ import absolute_import

# Import Python libs
import os
import sys
import random
import crypt
import json
import logging
import random

# Import Salt libs
import salt
import salt.version
import salt.loader
import salt.client
import salt.config
import salt.ext.six as six
from salt.utils.decorators import depends
from salt.exceptions import SaltRunnerError

from phue import Bridge

# Don't shadow built-in's.
__func_alias__ = {
    'true_': 'true',
    'false_': 'false'
}

logger = logging.getLogger(__name__)

CLIENT = salt.client.LocalClient()

def check(minion, ip, lights):
    '''
    According to the tag and minion update using cachet modules
    '''

    logger.warning('minion is {0}'.format(minion))
    logger.warning('bridge ip is {0}'.format(ip))

    id_to_update = []
    for light, status in lights.items():
        if not status:
            logger.warning('Light {0} is off'.format(light))
            id_to_update.append(light)
        else:
            logger.warning('Light {0} is on'.format(light))

    if not len(id_to_update):
        return

    username = _fetch_hue_username(minion, ip)
    logger.warning('username is {0}'.format(username))
    bridge = Bridge(ip=ip, username=username)
    lights = bridge.get_light_objects('id')

    for light_id in id_to_update:
        logger.warning('Turning on light {0}'.format(light_id))
        lights[light_id].on = True
        lights[light_id].brightness = 254
        lights[light_id].saturation = random.randint(0, 254)
        lights[light_id].hue = random.randint(0, 65535)

    return


def _fetch_hue_username(minion, ip):
    '''
    Simple function to return cachet_url and cachet_token
    '''

    result = CLIENT.cmd(minion, 'pillar.get', ['hue_config'])
    if minion not in result:
        raise SaltRunnerError('Unable to get hue_config for minion {0}'.format(minion))

    hue_config = result[minion]

    if ip not in hue_config:
        raise SaltRunnerError('No configuration for hue bridge with this ip {0}'.format(ip))

    if 'username' not in hue_config[ip]:
        raise SaltRunnerError('No username for hue bridge with this ip {0}'.format(ip))

    return hue_config[ip]['username']
