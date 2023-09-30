from rich.tree import Tree
from rich.panel import Panel
from rich.console import Console
from subprocess import run, PIPE
import sys
from pyrsistent import pset, pmap
import re


def main():
    console = Console()
    try:
        hierarchy = Hierarchy([Dataset(dataset_name) for dataset_name in zfs_list()])
        for tree in hierarchy.trees():
            console.print(tree)
    except InvalidDatasetName as e:
        console.print("Exception:", str(e), file=sys.stderr)


class Hierarchy:
    def __init__(self, datasets):
        clone_relation = pmap()
        child_relation = pmap()
        roots = pset()
        for dataset in datasets:
            if dataset.origin() is not None:
                clones = clone_relation.get(dataset.origin(), pset())
                clone_relation = clone_relation.set(
                    dataset.origin(), clones.add(dataset)
                )
            elif dataset.parent() is not None:
                children = child_relation.get(dataset.parent(), pset())
                child_relation = child_relation.set(
                    dataset.parent(), children.add(dataset)
                )
            else:
                roots = roots.add(dataset)
        self.clone_relation = clone_relation
        self.child_relation = child_relation
        self.roots = roots

    def is_cloned(self, dataset):
        return len(self.clone_relation.get(dataset, pset())) != 0

    def trees(self):
        def clone_tree(dataset, partial_tree):
            for clone in self.clone_relation.get(dataset, pset()):
                clone_tree(clone, partial_tree.add(clone.summary(), guide_style="dim"))
            return partial_tree

        def with_clones(dataset):
            if self.is_cloned(dataset):
                return Panel.fit(
                    clone_tree(dataset, Tree(dataset.summary(), guide_style="dim")),
                    style="dim",
                )
            else:
                return dataset.summary()

        def tree(root, partial_tree):
            for child in self.child_relation.get(root, pset()):
                tree(child, partial_tree.add(with_clones(child)))
            return partial_tree

        return [tree(root, Tree(with_clones(root))) for root in self.roots]


def zfs_list():
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
        if self.mounted():
            mount_info = f" → {self.mountpoint()}"
        else:
            mount_info = ""
        return f"{str(self)}{mount_info}"

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
