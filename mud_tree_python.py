#!/usr/bin/env python3

import subprocess

def main():
    zfs_list = subprocess.run("zfs list -H -o name", shell=True, stdout=subprocess.PIPE, text=True).stdout.splitlines()
    print(zfs_list) 