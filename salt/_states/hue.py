# -*- coding: utf-8 -*-

# Import python libs
from __future__ import absolute_import, unicode_literals, print_function
import re
import sys

# Import 3rd-party libs
from salt.ext import six


def light_on(
        name,
        bridge_ip):
    '''
    '''
    ret = {'name': name,
           'result': False,
           'changes': {},
           'comment': ''}

    try:
        light_id = int(name)
        lights = __salt__['hue.get_lights_ids'](bridge_ip)
    except ValueError:
        light_id = name
        lights = __salt__['hue.get_lights'](bridge_ip)

    if light_id not in lights:
        ret['comment'] = 'Light {0} does not exist on bridge {1}'.format(name, bridge_ip)
        return ret

    status = __salt__['hue.get_light_status'](bridge_ip, light_id)
    if status:
        ret['result'] = True
        ret['comment'] = 'Light {0} is already on'.format(light_id)
        return ret

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = 'Light {0} would be turned on'.format(light_id)
        return ret

    result = __salt__['hue.switch_light_on'](bridge_ip, light_id)
    if result:
        ret['result'] = result
        ret['comment'] = 'Light {0} was turned on'.format(light_id)
        return ret
    return ret


def light_off(
        name,
        bridge_ip):
    '''
    '''
    ret = {'name': name,
           'result': False,
           'changes': {},
           'comment': ''}

    try:
        light_id = int(name)
        lights = __salt__['hue.get_lights_ids'](bridge_ip)
    except ValueError:
        light_id = name
        lights = __salt__['hue.get_lights'](bridge_ip)

    if light_id not in lights:
        ret['comment'] = 'Light {0} does not exist on bridge {1}'.format(name, bridge_ip)
        return ret

    status = __salt__['hue.get_light_status'](bridge_ip, light_id)
    if not status:
        ret['result'] = True
        ret['comment'] = 'Light {0} is already off'.format(light_id)
        return ret

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = 'Light {0} would be turned off'.format(light_id)
        return ret

    result = __salt__['hue.switch_light_off'](bridge_ip, light_id)
    if result:
        ret['result'] = result
        ret['comment'] = 'Light {0} was turned off'.format(light_id)
        return ret
    return ret
