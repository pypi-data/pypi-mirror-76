{% from "agent/map.jinja" import agent with context %}

agent-pip-upgrade:
  cmd.run:
    - name: pip3 install --upgrade pip
    - reload_modules: true
    - onfail:
      - pip: agent-install

agent-install:
  pkg.installed:
    - pkgs:
      - ipset
      - iptables
    - refresh: true
  pip.installed:
    - pkgs:
      - aiorun
      - ipsetpy
      - odoopbx
      - OdooRPC
      - https://github.com/litnimax/panoramisk/archive/master.zip
      - pastebin
      - setproctitle
      - terminado
      - tornado-httpclient-session
    - require:
      - pkg: agent-install
    - retry: True

agent-locale:
  locale.present:
    - name: en_US.UTF-8

agent-service:
  file:
    - managed
    - name: /etc/systemd/system/odoopbx-agent.service
    - source: salt://agent/agent.service
{% if grains.virtual != "container" %}
  service:
    - running
    - name: odoopbx-agent
    - enable: True
    - require:
      - pip: agent-install
      - pkg: agent-install
      - file: agent-service
{% endif %}
