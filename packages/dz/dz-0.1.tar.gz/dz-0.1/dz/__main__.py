#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import sys
from multiprocessing import Pool
from collections import ChainMap
import argcomplete
import itertools
import argparse
import subprocess
import json
import pathlib
import itertools
from pathlib import Path
from tqdm import tqdm
from output import *


class HostTable(Table):
    fields = ["hostname", "datacenter", "version", "manufacturer", "product", "serial", "sku", "cpu_type", "ram", "disk", "cpus", ]
    byte_fields = ["ram", "disk"]
    default_fields = ["hostname", "ram", "disk"]
    default_sort = ["datacenter", "hostname"]

class ZoneTable(Table):
    fields = ["uuid", "zonename", "brand", "create_timestamp", "image_uuid", "billing_id", "owner_uuid", "alias", "state", "server_uuid", "datacenter_name", "quota", "ram", "type"]# "hostname"
    default_fields = ["uuid", "type", "state", "ram", "quota", "alias"]
    default_sort = ["ram", "quota", "alias", "uuid"]


def ssh(host, args, **kwargs):
    if '@' not in host:
        host = 'root@' + host
    return subprocess.run(["ssh", host] + args, **kwargs)


def _fetch_sysinfo(hostname):
    proc = ssh(hostname, ["sysinfo"], capture_output=True, encoding="utf-8")
    if proc.returncode != 0:
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        sys.exit(proc.returncode)
    return json.loads(proc.stdout)


def _fetch_zones(hostname):
    proc = ssh(hostname, ["vmadm", "lookup", "-j"], capture_output=True, encoding="utf-8")
    if proc.returncode != 0:
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        sys.exit(proc.returncode)
    return json.loads(proc.stdout)


def zone_completer(**kwargs):
    dz = DeployZone('~/.dz/default.json') # TODO: hardcodedfor now
    return list(dz.config['host_via_uuid'].keys()) + list(dz.config['uuid_via_alias'].keys())


class DeployZone():
    def __init__(self, config):
        self.config_file = pathlib.Path(config).expanduser()
        self._load()

    def _load(self):
        try:
            self.config = json.load(open(self.config_file))
        except FileNotFoundError:
            self.config = {
                'hosts': {},
            }

        # build indexes
        self._zones = []
        self._host_via_uuid = {}
        self._uuid_via_alias = {}
        for host, data in self.config['hosts'].items():
            self._zones += data['zones']
            self._host_via_uuid.update({zone['uuid']: host for zone in data['zones']})
            self._uuid_via_alias.update({zone['alias']: zone['uuid'] for zone in data['zones']})

    def _save(self):
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)

    def _lookup_host_and_zone(self, host, zone):
        if host:
            return host, zone
        if zone in self._host_via_uuid:
            host = self._host_via_uuid[zone]
            return host, zone
        if zone in self._uuid_via_alias:
            zone = self._uuid_via_alias[zone]
            host = self._host_via_uuid[zone]
            return host, zone
        print('Unknown zone, please specify host or refresh cache')
        sys.exit(-1)

    def _cached_zones(self):
        pass

    def _index_host_via_uuid(self):
        
        dict(ChainMap(*host_via_uuid.values()))

    def _get_datasets(self, zone, filter_nested=False):
        zone = self.config['host_via_uuid'][zone]
        datasets = []
        if 'zfs_filesystem' in zone:
            datasets += [zone['zfs_filesystem']]
        for disk in zone['disks']:
            if 'zfs_filesystem' in disk:
                datasets += [disk['zfs_filesystem']]
        if 'datasets' in zone:
            datasets += zone['datasets']
        if filter_nested:
            fake_pathed = [Path('/' + d) for d in datasets]
            filtered = [p for p in set(fake_pathed) if not set(p.parents).intersection(set(fake_pathed))]
            datasets = [str(d)[1:] for d in filtered]
        return datasets

    def refresh(self, host, quiet, **kwargs):
        if host:
            hosts = [host]
        else:
            hosts = self.config['hosts'].keys()

        with Pool(processes=10) as pool:
            i = pool.imap_unordered(self.host_refresh, hosts)
            if not quiet:
                i = tqdm(i, unit='', total=len(hosts))
            [x for x in i]

    def host_refresh(self, hostname):
        sysinfo = _fetch_sysinfo(hostname)
        zones   = _fetch_zones(hostname)
        self.config['hosts'][hostname] = {
            'sysinfo': {
                'hostname':     hostname,
                'datacenter':   sysinfo.get('Datacenter Name'),
                
                'version':      sysinfo.get('Live Image'),
                'manufacturer': sysinfo.get('Manufacturer'),
                'product':      sysinfo.get('Product'),
                'serial':       sysinfo.get('Serial Number'),
                'sku':          sysinfo.get('SKU Number'),
                'cpu_type':     sysinfo.get('CPU Type'),
                
                'ram':   int(sysinfo.get('MiB of Memory', 0)) * 1024 * 1024,
                'disk':  int(sysinfo.get('Zpool Size in GiB', 0)) * 1024 * 1024 * 1024,
                'cpus':  int(sysinfo.get('CPU Count', 0)),
            },
            'zones': zones,
        }
        self._save()

    def host_add(self, hostname, **kwargs):
        self.host_refresh(hostname)
        print('Successfully added')

    def host_remove(self, hostname, **kwargs):
        del self.config['hosts'][hostname]
        self._save()
        print('Successfully removed')
    
    def host_list(self, **kwargs):
        HostTable([h['sysinfo'] for h in self.config['hosts'].values()]).write(**kwargs)

    def zone_list(self, **kwargs):
        ZoneTable(self._zones).write(**kwargs)


    def zone_start(self, host, zone, **kwargs):
        host, zone = self._lookup_host_and_zone(host, zone)
        ssh(host, ["vmadm", "start", zone], encoding="utf-8")
        self.host_refresh(host)

    def zone_stop(self, host, zone, **kwargs):
        host, zone = self._lookup_host_and_zone(host, zone)
        ssh(host, ["vmadm", "stop", zone], encoding="utf-8")
        self.host_refresh(host)

    def zone_reboot(self, host, zone, **kwargs):
        host, zone = self._lookup_host_and_zone(host, zone)
        ssh(host, ["vmadm", "reboot", zone], encoding="utf-8")
        self.host_refresh(host)

    def zone_update(self, host, zone, properties, **kwargs):
        host, zone = self._lookup_host_and_zone(host, zone)
        ssh(host, ["vmadm", "update", zone] + properties, encoding="utf-8")
        self.host_refresh(host)


    def zone_shell(self, host, zone, console = None, user = None, **kwargs):
        host, zone = self._lookup_host_and_zone(host, zone)
        if console:
            print('To end the serial console session press ENTER then CTRL-] then .')
            args = ["-t", "vmadm", "console", zone]
        elif user:
            args = ["-t", "zlogin", "-l", user, zone]
        else:
            args = ["-t", "zlogin", zone]
        proc = ssh(host, args)


    def backup_create(self, host, zone, **kwargs):
        if not zone:
            pass
            # backup all zones?

        host, zone = self._lookup_host_and_zone(host, zone)
        print(self._get_datasets(zone))
        pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', help='Use config information from file (~/.dz/default.json)', default='~/.dz/default.json')
    subparsers = parser.add_subparsers()
    
    # zone commands
    parser_list = subparsers.add_parser('list', help='List zones')
    parser_list.add_argument('-j', '--json', action='store_true', help='output json')
    parser_list.add_argument('-o', '--output', help='output fields')
    parser_list.add_argument('-s', '--sort', help='sort by fields')
    parser_list.add_argument('-f', '--filter', help='filter')
    parser_list.set_defaults(func="zone_list")
    
    parser_refresh = subparsers.add_parser('refresh', help='Refresh cache')
    parser_refresh.add_argument('-H', '--host', help='host')
    parser_refresh.add_argument('-q', '--quiet', action='store_true', help="don't show progressbar")
    parser_refresh.set_defaults(func="refresh")
    
    
    parser_start = subparsers.add_parser('start', help='Start a zone')
    parser_start.add_argument('-H', '--host', help='host')
    parser_start.add_argument('zone', help='zone identifier (uuid / alias)')
    parser_start.set_defaults(func="zone_start")

    parser_stop = subparsers.add_parser('stop', help='Stop a zone')
    parser_stop.add_argument('-H', '--host', help='host')
    parser_stop.add_argument('zone', help='zone identifier (uuid / alias)')
    parser_stop.set_defaults(func="zone_stop")

    parser_reboot = subparsers.add_parser('reboot', help='Reboot a zone')
    parser_reboot.add_argument('-H', '--host', help='host')
    parser_reboot.add_argument('zone', help='zone identifier (uuid / alias)')
    parser_reboot.set_defaults(func="zone_reboot")

    parser_update = subparsers.add_parser('update', help='Update a zone')
    parser_update.add_argument('-H', '--host', help='host')
    parser_update.add_argument('zone', help='zone identifier (uuid / alias)')
    parser_update.add_argument('properties', help='property=value [property=value]', nargs='*')
    parser_update.set_defaults(func="zone_update")

    parser_shell = subparsers.add_parser('shell', help='Execute shell in a zone')
    parser_shell.add_argument('-H', '--host', help='host')
    parser_shell.add_argument('-C', '--console', action='store_true', help='connects to the zone console')
    parser_shell.add_argument('-u', '--user', help='connect with the specified')
    parser_shell.add_argument('zone', help='zone identifier (uuid / alias)').completer = zone_completer
    parser_shell.set_defaults(func="zone_shell")
    
    
    # host commands
    parser_host = subparsers.add_parser('host', help='Manage known hosts')
    host_subparsers = parser_host.add_subparsers()
    
    parser_host_add = host_subparsers.add_parser('add', help='Add a host')
    parser_host_add.add_argument('hostname', help='Add hostname to system')
    parser_host_add.set_defaults(func="host_add")

    parser_host_remove = host_subparsers.add_parser('remove', help='Delete a host')
    parser_host_remove.add_argument('hostname', help='Remove hostname')
    parser_host_remove.set_defaults(func="host_remove")
    
    parser_host_list = host_subparsers.add_parser('list', help='List hosts')
    parser_host_list.add_argument('-j', '--json', action='store_true', help='output json')
    parser_host_list.add_argument('-o', '--output', help='output fields')
    parser_host_list.add_argument('-s', '--sort', help='sort by fields')
    parser_host_list.add_argument('-f', '--filter', help='filter')
    parser_host_list.set_defaults(func="host_list")


    # backup commands
    parser_backup = subparsers.add_parser('backup', help='Manage backups')
    backup_subparsers = parser_backup.add_subparsers()
    
    parser_backup_create = backup_subparsers.add_parser('create', help='Createa a zone backup')
    parser_backup_create.add_argument('-H', '--host', help='host')
    parser_backup_create.add_argument('zone', help='zone identifier (uuid / alias)')
    parser_backup_create.set_defaults(func="backup_create")



    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_usage()
        sys.exit(0)

    return args


def main():
    args = parse_args()
    dz = DeployZone(config = args.config)
    getattr(dz, args.func)(**vars(args))


if __name__ == '__main__':
    main()