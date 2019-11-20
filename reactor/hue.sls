{#
hue_reactor:
  runner.hue.check:
    - minion: {{ data['id'] }}
    - ip: {{ data['ip'] }}
    - lights: {{ data['lights'] }}
#}

{#
{% for id, state in data['lights'].items() %}
switch_light_{{ id }}_on:
  local.hue.set_light:
    - tgt: {{ data['id'] }}
    - args:
      - bridge_ip: {{ data['ip'] }}
      - transitiontime: 10
      - light_id: {{ id }}
{% endfor %}
#}
