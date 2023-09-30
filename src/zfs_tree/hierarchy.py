from rich.tree import Tree
from rich.panel import Panel
from pyrsistent import pset, pmap


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
