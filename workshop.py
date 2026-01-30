import inspect
import os
import json

def get_traceback_tree():
    # Capture the stack (reverse it to go from Root -> Leaf)
    stack = inspect.stack()[::-1]
    tree = {}
    for frame_info in stack:
        print(f"file: {frame_info.filename}; func: {frame_info.function}(); line {frame_info.lineno}")

    return tree

def leaf_node():
    tree = get_traceback_tree()
    print(json.dumps(tree, indent=2))

def branch_node():
    leaf_node()

branch_node()