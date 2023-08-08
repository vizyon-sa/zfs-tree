#!/usr/bin/env python3

from subprocess import run, PIPE
import sys
from pyrsistent import pset, pmap
import re


def main():
    try:
        datasets = [Dataset(dataset_name) for dataset_name in zfs_list()]
        child_hierarchy = pmap()
        child_hierarchy_roots = pset()
        for dataset in datasets:
            if dataset.origin() is None:
                print(f"No   parent: {dataset}")
                child_hierarchy_roots = child_hierarchy_roots.add(dataset)
            else:
                print(f"With parent: {dataset}")
                children = child_hierarchy.get(dataset.origin(), pset())
                child_hierarchy = child_hierarchy.set(dataset.origin(), children.add(dataset))
        print(f"{len(child_hierarchy_roots)} roots and {len(child_hierarchy)} entries.")
    except InvalidDatasetName as e:
        print("Exception:", str(e), file=sys.stderr)


def zfs_list():
    output = run("zfs list -H -o name", shell=True, stdout=PIPE, text=True)
    return output.stdout.splitlines()


class Dataset:
    def __init__(self, dataset_name):
        validate_dataset_name(dataset_name)
        self.name = dataset_name

    def origin(self):
        output = run(f"zfs get -H -o value origin {self.name}", shell=True, stdout=PIPE, text=True)
        if output.stdout.rstrip() != "-":
            return Dataset(output.stdout.rstrip())
        else:
            return None

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Dataset) and self.name == other.name


def validate_dataset_name(dataset_name):
    if re.match(r'^[a-zA-Z0-9/_@]+$', dataset_name) is None:
        raise InvalidDatasetName(dataset_name)


class InvalidDatasetName(Exception):
    def __init__(self, invalid_dataset_name):
        self.invalid_dataset_name = invalid_dataset_name

    def __str__(self):
        return f"{type(self).__name__}: {self.invalid_dataset_name}"
