#!/usr/bin/env python3

import sys
import subprocess

def main():
    try:
        datasets = subprocess.run("zfs list -H -o name", shell=True, stdout=subprocess.PIPE, text=True).stdout.splitlines()
        for dataset in datasets:
            validate_dataset_name(dataset)
        print(datasets)
    except InvalidDatasetName as e:
        print("Exception:", str(e), file=sys.stderr)

import re

def validate_dataset_name(dataset_name):
    if re.match(r'^[a-zA-Z0-9/_]+$', dataset_name) is None:
        raise InvalidDatasetName(dataset_name)

class InvalidDatasetName(Exception):
   pass