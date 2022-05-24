from dataclasses import dataclass
from tokenize import String
from typing import Union, cast

from lark.visitors import Interpreter
from networkx import MultiDiGraph

@dataclass
class Node:
    context: 'Node'
    name: str
    def fullname(self):
        if self.context is not None:
            return f"{self.context.fullname()}.{self.name}" 
        else:
            return self.name

@dataclass
class ClassNode(Node):
    pass
    
@dataclass
class FunctionNode(Node):
    anonymous: bool = False

@dataclass
class UnknownFunctionNode(Node):
    pass

    
@dataclass
class FunctionCall(Node):
    direct: bool = True


class Python2Callgraph(Interpreter):
    """
    Collect all function definitions and function calls.
    The Interpreter class is used as that's the only way we can have a pre-post-visit function. This is needed to
    control the context in which functions are defined and calls are made without handling all nodes in the tree.

    Class definitions are only used for context. Not implemented yet are resolving variables to their types to support
    member functions of class instances (objects). This would require understanding of the types of variables and
    the class hierarchy/subtyping relationships.
    Lambda functions are not handled properly nor functions that happen through an expression (function returned or
    assigned to a variable). This would require points-to analysis to be in place.
    """
    context = None
    functions = dict()
    calls: list[FunctionCall] = list()
    _unknown_count = 0

    def _set_context(self, val):
        old = self.context
        self.context = val
        return old

    def _add_node(self, n:Node):
        if n.name is None:
            self._unknown_count += 1
            n.name = f"__unknown_{self._unknown_count}"
        self.functions[n.fullname()] = n
    def _add_edge(self, e):
        if e.name is None:
            self._unknown_count += 1
            e.name = f"__unknown_{self._unknown_count}"
        if e.name.startswith("self."):
            myself = e.context.context if isinstance(e.context, FunctionNode) else e.context
            e.name = f"{myself.fullname()}{e.name[4:]}"
        self.calls.append(e)
    
    def classdef(self, tree):
        elem = ClassNode(self.context, tree.children[0].value)
        old = self._set_context(elem)
        self.visit_children(tree)
        self._set_context(old)

    def funcdef(self, tree):
        elem = FunctionNode(self.context, tree.children[0].value)
        self._add_node(elem)
        old = self._set_context(elem)
        self.visit_children(tree)
        self._set_context(old)

    def funccall(self, tree):
        # We don't handle the dynamic dispatch at all. To do so we would need a global alias analysis and static type
        # system to resolve variables to a set of potential functions the call could reach.
        # We can use some heuristics to cover a few simple common cases:
        # * If starts with 'self.' it is a member (function/variable), and we replace 'self' with the class name.
        # * A function of a member variable becomes "<classname>.<variable>.<function>". If we support type hints
        #   we could replace <classname>.<member> with the type of the member. Same for a global variable.
        #
        callee, _ = self.visit_children(tree)
        name = callee if isinstance(callee, str) else None
        elem = FunctionCall(self.context, name)
        self._add_edge(elem)

    # crude name resolution of a function call
    def var(self, tree):
        assert tree.children[0].type == "NAME"
        return str(tree.children[0].value)
    def getattr(self, tree):
        if tree.children[0].data in ["var", "getattr"]:
            elements = self.visit_children(tree)
            return ".".join(elements)
        else:
            return tree


def python2Callgraph(tree):
    visitor = Python2Callgraph()
    visitor.visit(tree)
    cg = MultiDiGraph()
    print(f"Found the following:\n\t{visitor.functions}\n\t{visitor.calls}")
    for name, function in visitor.functions.items():
        cg.add_node(name, data=function)
    for call in visitor.calls:
        src = call.context.fullname() if call.context is not None else "__top__"
        tgt = call.name
        cg.add_edge(src, tgt, data=call)
    return cg
