from hashlib import md5
from loguru import logger
from data_druid.structures.exceptions import RootError

logger.add('Logs/tree.log', level='DEBUG')


class FolderTree:
    """This can be used to emulated a folder. Or any type of tree that requires
    more than one branch."""
    def __init__(self, value):
        if type(value) is not dict:
            raise ValueError
        else:
            for key, data in value.items():
                setattr(self, key, data)

        self.nodes = [list() for _ in range(10)]
        self.parent = None

    def add_node(self, value):
        """Add a new node to the current tree.

        Parameters
        ----------
         value : dict
            Value of the node should be a dictionary, holding the proper keys:

            * ``id``
            * ``name``
            * ``is_folder``
            * ``is_parent``
            * ``is_root``
            * ``parent_id``.
        """
        node = FolderTree(value)
        if node.is_root:
            raise RootError

        bucket = self.set_bucket(node.id)

        if node.parent_id is not None:
            logger.info('parent node {}'.format(node.parent_id))

            # if node.parent_id == self.id:
            #     self.nodes[bucket].append(node)

            # if node.parent_id != self.id:
            r = self.search_tree(_id=node.parent_id)
            logger.debug('r:{}'.format(r))

            if r is not None:
                logger.info('found {} and placing {} in bucket {}'.format(
                    r.id, node.id, bucket
                ))
                r.nodes[bucket].append(node)
                node.parent = r
            elif r is None:
                logger.info('unable to find parent id {}'.format(
                    node.parent_id
                ))

        # if node.parent_id is None:
        #     self.nodes[bucket].append(node)

    @staticmethod
    def set_bucket(_id):
        """Using a md5 digest of the node id create a reproducible bucket
        number.

        Parameters
        ----------
        _id : str
            The node id.

        Returns
        -------
        int
            The bucket number that the node will be assigned too.
        """
        digest = md5(_id.encode()).hexdigest()
        ascii_sum = 0
        for c in digest:
            ascii_sum += ord(c)
        return ascii_sum % 10

    def search_tree(self, _id=None):
        """Using the id search the node within the tree.

        Parameters
        ----------
        _id : str
            The node's id.
        """
        if _id is not None:
            return self.search_id(_id)
        elif _id is None:
            raise ValueError

    def search_id(self, _id):
        """Search within the node tree of a specific node using the id of the
        target node.

        Parameters
        ----------
        _id : str
        """
        logger.info('Starting search in current node: {}'.format(self.id))
        if _id == self.id:
            logger.info('found {}'.format(_id))
            logger.info('self:{}'.format(self))
            return self
        else:
            for nodes in self.nodes:
                for n in nodes:
                    logger.debug('{}:{}'.format(n.id, n.name))
                    if n.id == _id:
                        return n
                    else:
                        res = n.search_id(_id)
                        if res is not None:
                            return res

    def print_node(self, level=0):
        """This will print the tree from the current node through its children
        nodes.

        Parameters
        ----------
        level : int
        """
        if self.is_root:
            print('[{}] is at level {} (root)'.format(self.name, level))

        spaces = '  '
        if level != 0:
            for _ in range(level * 2):
                spaces += ' '

        for node in self.nodes:
            for n in node:
                print('{}[{}] is at level {}'.format(spaces,
                                                     n.name, level + 1))
                n.print_node(level=level + 1)
