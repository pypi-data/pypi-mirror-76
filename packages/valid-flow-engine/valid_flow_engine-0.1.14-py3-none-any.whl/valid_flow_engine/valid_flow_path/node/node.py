from __future__ import annotations
import typing
from abc import ABC, abstractmethod


class Node(ABC):
    """Base Class for all Nodes

    Arguments:
        ABC {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    @property
    def id(self):
        return self._id

    def __init__(self, node_def: dict):
        self._id = node_def.get('id')
        self._parent_node_id = node_def.get('parentNodeIDs')
        self.is_evalutated = False

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        return True


if typing.TYPE_CHECKING:
    from ..valid_flow_path import ValidFlowPath
