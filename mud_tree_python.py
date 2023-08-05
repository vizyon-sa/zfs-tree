#!/usr/bin/env python3

import sys
import subprocess

def main():
    try:
        datasets = subprocess.run("zfs list -H -o name", shell=True, stdout=subprocess.PIPE, text=True).stdout.splitlines()
        for dataset in datasets:
            print(str(Dataset(dataset)))
    except InvalidDatasetName as e:
        print("Exception:", str(e), file=sys.stderr)

class Dataset:
    def __init__(self, dataset_name):
        validate_dataset_name(dataset_name)
        self.name = dataset_name

    def __str__(self):
        return self.name

import re

def validate_dataset_name(dataset_name):
    if re.match(r'^[a-zA-Z0-9/_]+$', dataset_name) is None:
        raise InvalidDatasetName(dataset_name)

class InvalidDatasetName(Exception):
    pass