from .site import validate_site


VALIDATE_NODE_TYPE = {
    'Site': lambda v: validate_site(v)
}


def validate_node(node: dict):
    validations = VALIDATE_NODE_TYPE[node['@type']](node) if node['@type'] in VALIDATE_NODE_TYPE else []
    return list(filter(lambda v: v is not True, validations))
