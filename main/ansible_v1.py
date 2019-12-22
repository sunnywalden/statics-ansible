#!/usr/bin/python
# coding=utf-8
# author: sunnywalden@gmail.com

import json
import subprocess as sub

file_json = '../tmp/ecs_all.json'
final_xml = '../tmp/ecs_all.xml'


def ansible_cmd():
    ansible_cmd = 'ansible all ' + \
                  ' -i ../tmp/ecs_all.yml -m shell -a ' + \
                  '"check_name=`docker stats --no-stream|grep NAME|grep -v grep|wc -l` && hostname && \
    if [[ \${check_name} -ne 1 ]];then docker stats --no-stream|awk \'{print \$1","\$3\$4","\$6\$7}\'; \
    else docker stats --no-stream|awk \'{print \$2","\$4","\$6}\';fi"'
    return ansible_cmd


def get_host():
    with open(file_json) as f:
        host_infos = json.loads(f.read())

    return host_infos


def docker_stats(docker_mem, host, f):
    container_mem_list = docker_mem.split()
    print('Debug {0} docker mem str {1}'.format(host["instance_name"], docker_mem))
    if len(container_mem_list) == 14 and 'CONTAINER' not in container_mem_list:
        container_name = container_mem_list[1]
        container_mem_use = container_mem_list[3]
        container_mem_limit = container_mem_list[5]
        try:
            mem_str = host["instance_name"] + ',' + host["public_ip"] + ',' + \
                      str(host["memory"]) + \
                      'G,' + container_name + ',' + \
                      str(container_mem_use) + ',' + str(container_mem_limit)
        except TypeError as e:
            print(container_mem_use, container_mem_limit)
        else:
            f.write(mem_str + '\n')
            print('Save to excel success!'.format(mem_str))
    elif len(container_mem_list) < 14 and 'CONTAINER' not in container_mem_list:
        print(container_mem_list)
    else:
        pass


def container_info(host, mem_str, f):
    mem_list = mem_str.split(b'\n')
    print('Debug host {} docker stat {}'.format(host["instance_name"], mem_str))
    if len(mem_list) > 2:
        container_mems = mem_list[1:]
        for container_mem in container_mems:
            docker_stats(container_mem, host, f)
    elif len(mem_list) > 0:
        print(mem_list)
    else:
        pass


def ansible_cli():
    cmd = ansible_cmd()
    try:
        retcode, output = sub.getstatusoutput(cmd)
    except Exception as e:
        pass
    else:
        print(output)
        with open('../tmp/tmp.txt', 'w+') as f:
            f.write(output)


def host_info(ip):
    hosts = get_host()
    for host in hosts:
        inner_ip = host["private_ip"]
        public_ip = ["public_ip"]
        if ip in (inner_ip, public_ip):
            return host
    return None


def info_parse():
    with open('../tmp/tmp.txt', 'r') as f:
        with open('../tmp/res.csv', 'w+') as f1:
            f1.write('主机名称,主机IP,主机内存(G),容器名称,分配内存(G),占用内存,所属服务,备注\n')
            host_name, public_ip, mem, docker_name, mem_use, mem_limit = '', '', '', '', '', '',
            while True:
                try:
                    line = f.readline()
                    print("Dealing with line {0}".format(line))
                except Exception as e:
                    break
                else:
                    if line:
                        if '>>' in line:
                            host_ip = line.split()[0]
                            host_dict = host_info(host_ip)
                            if not host_dict: continue
                            mem = str(host_dict["memory"]) + 'G' if host_dict["memory"] else ''
                            host_name = host_dict["instance_name"]
                            public_ip = host_dict["public_ip"] if host_dict["public_ip"] else host_dict["private_ip"]
                        if 'GiB' or 'MiB' in line:
                            if len(line.split()) < 3:
                                pass
                            try:
                                docker_name = line.split()[0].split('.')[0]
                                mem_use = line.split()[1]
                                mem_limit = line.split()[2]
                            except IndexError as e:
                                print('Parse error {}'.format(line))
                            else:
                                docker_mem = (host_name, public_ip, mem, docker_name, mem_use, mem_limit)
                                if 'CPU' in line or '|' in line or 'CHANGED' in line:
                                    pass
                                else:
                                    f1.write(','.join(docker_mem) + '\n')
                    else:
                        break


if __name__ == '__main__':
    ansible_cli()
    info_parse()
