#!/usr/bin/env python3

import subprocess

def main():
    zfs_list = subprocess.run("zfs list -o name", shell=True, stdout=subprocess.PIPE, text=True)
    print(zfs_list.stdout) 