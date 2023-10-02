from rich.console import Console
import sys

from .dataset import Dataset, InvalidDatasetName
from .hierarchy import Hierarchy
from .shell import command


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
