class RootError(Exception):
    """Raise when another root is attempting to connect to a tree when there is
    already a root for a tree"""
    pass


class DuplicateNode(Exception):
    """If a node is a duplicate it will not be added."""
    pass