#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: sunnywalden@gmail.com

import redis
import json

from ansible_v1 import get_host

file_path = '../tmp/ecs_all.yml'
file_json = '../tmp/ecs_all.json'


def all_ecs():
    r = redis.Redis(host='127.0.0.1', port=6309, db=0, password='tezign0818')

    hosts_str = r.get('instance')

    hosts = json.loads(hosts_str)

    return hosts


def write_hosts_yaml(hosts):
    test_host = hosts[0]
    print(
        test_host['instance_name'],
        test_host['public_ip'],
        test_host['private_ip'],
        test_host['region'],
        test_host['zone_id'],
        str(test_host['cpu']),
        str(test_host['memory'])
    )

    with open(file_path, 'w+') as f:
        for host in hosts:
            password = 'tezign0818'
            user = 'web'
            port = '60022'

            status = host['status']
            if status != 'Running': break
            name = host['instance_name']
            ip = host['public_ip'] if host['public_ip'] else ' '
            inner_ip = host['private_ip']
            region = host['region']
            zone = host['zone_id']
            cpu = str(host['cpu'])
            memory = str(host['memory'])

            if ip == '47.93.82.240':
                password = "SSVFDKBJNDFNJ@rfgvf3244"
            if not ip: ip = inner_ip
            if ip in ('39.105.24.131', '39.107.159.204', '60.205.148.219', '47.93.82.240'):
                user = 'root'

            f.write('[' + name.replace('-', '_') + ']' + ' \n')
            new_record = ip + ' public_ip="' + ip + '" private_ip' + '=' + '"' + inner_ip + '" zone="' + region + \
                         '" memory=' + '"' + memory + 'G' + '"' + ' ansible_ssh_user="' + \
                         user  + '" ansible_sudo_pass="' + password +  '" ansible_ssh_port=' + port + ' \n'
            f.write(new_record)
            f.write(' \n')

    with open(file_json, 'w+') as f1:
        f1.write(json.dumps(hosts))


if __name__ == '__main__':
    # hosts = all_ecs()
    hosts = get_host()
    write_hosts_yaml(hosts)
