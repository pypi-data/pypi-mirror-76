from .node import Node
from .io_nodes import InputNode, OutputNode
from .action_nodes import FunctionNode, BooleanNode, ActionNode


def get_payload_element(payload: dict, element_key: str):
    if '.' not in element_key:
        return payload.get(element_key, element_key)
    else:
        ret = payload
        keys = element_key.split('.')
        for key in keys:
            ret = ret.get(key, None)
            if ret is None:
                return key
        return ret
