from rich.console import Console
from subprocess import run, PIPE
import sys
import re

from .hierarchy import Hierarchy


def main():
    console = Console()
    try:
        hierarchy = Hierarchy([Dataset(dataset_name) for dataset_name in zfs_list()])
        for tree in hierarchy.trees():
            console.print(tree)
    except InvalidDatasetName as e:
        console.print("Exception:", str(e), file=sys.stderr)


def zfs_list():
    #
    # Some details about the `zfs list` invocation below:
    #
    # The `-H` option removes the headers from the `zfs list` command, making
    # it more amenable to command line output parsing with the `.splitlines()`
    # method.
    #
    # For documention of the `zfs list` command, see:
    # https://docs.oracle.com/cd/E18752_01/html/819-5461/gazsu.html
    #
    return command("zfs list -H -o name").splitlines()


class Dataset:
    def __init__(self, dataset_name):
        name = dataset_name.split("@", 1)[0]
        validate_dataset_name(name)
        self.name = name

    def origin(self):
        origin = self.zfs_get("origin")
        if origin != "-":
            return Dataset(origin)
        else:
            return None

    def parent(self):
        segments = self.name.rsplit("/", 1)
        if len(segments) < 2:
            return None
        else:
            return Dataset(segments[0])

    def summary(self):
        size_info = f" [{self.size()}]"
        if self.mounted():
            mount_info = f" → {self.mountpoint()}"
        else:
            mount_info = ""
        return f"{str(self)}{size_info}{mount_info}"

    def size(self):
        return command(f"zfs list -H -o used {self.name}")

    def mounted(self):
        return boolean(self.zfs_get("mounted"))

    def mountpoint(self):
        return self.zfs_get("mountpoint")

    def zfs_get(self, property):
        return command(f"zfs get -H -o value {property} {self.name}")

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Dataset) and self.name == other.name


def boolean(string):
    if string == "yes":
        return True
    elif string in ["no", "-"]:
        return False
    else:
        raise ValueError(
            f'The string "{string}" is neither "yes" nor "no" and can '
            "thus not be converted into neither True nor False."
        )


def command(cmd):
    return run(cmd, shell=True, stdout=PIPE, text=True).stdout.rstrip()


def validate_dataset_name(dataset_name):
    if re.match(r"^[a-zA-Z0-9/\-_\.]+$", dataset_name) is None:
        raise InvalidDatasetName(dataset_name)


class InvalidDatasetName(Exception):
    def __init__(self, invalid_dataset_name):
        self.invalid_dataset_name = invalid_dataset_name

    def __str__(self):
        return f"{type(self).__name__}: {self.invalid_dataset_name}"
