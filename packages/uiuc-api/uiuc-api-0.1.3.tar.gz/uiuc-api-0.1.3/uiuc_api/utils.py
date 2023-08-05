from types import GeneratorType
from lark import Tree


def reduce_tree(tree: Tree):
    """
    Recursively coverts prereq parse tree to dict for further processing.

    :param tree: A subtree of the parse tree
    :return: appropriate object based on root node of subtree passed
    """
    children = tree.children
    rule = tree.data
    if rule == "start":
        return {child.data: reduce_tree(child) for child in children}
    if rule == "course":
        subject, number = children
        subject = "".join(token.value for token in subject.children)
        number = "".join(token.value for token in number.children)
        return "{0} {1}".format(subject, number)
    elif rule == "direct":
        return (frozenset((reduce_tree(child),)) for child in children)
    elif rule == "set":
        return frozenset(reduce_tree(child) for child in children)
    elif rule in ("prereq", "coreq"):
        reqs = []
        for child in children:
            reduced = reduce_tree(child)
            if isinstance(reduced, frozenset):
                reqs.append(reduced)
            elif isinstance(reduced, GeneratorType):
                reqs.extend(reduced)
        return frozenset(reqs)
    elif rule == "other":
        return True
    else:
        raise ValueError("can't reduce tree with unrecognized rule")
