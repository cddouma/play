from typing import Any, Dict
from dataclasses import dataclass, field

from lark import Transformer

@dataclass(kw_only=True)
class IRNode:
    pass

@dataclass
class Function(IRNode):
    name: str
    parameters: Any
    body: Any

@dataclass
class Class(IRNode):
    name: str
    data: Any

@dataclass
class StatementNode(IRNode):
    pass

@dataclass
class Statement(StatementNode):
    kind: str
    data: Any

@dataclass
class ExpressionNode(IRNode):
    pass

@dataclass
class Call(ExpressionNode):
    function: Any
    arguments: Any

@dataclass
class NameRef(ExpressionNode):
    name: str

@dataclass
class Expression(ExpressionNode):
    kind: str
    data: Any

class Python2SimpleIR(Transformer):
    def file_input(self, stmts):
        return stmts

    def classdef(self, items):
        return Class(name=items[0], data=items[1:])
    
    def funcdef(self, items):
        print(items)
        return Function(name=items[0], parameters=items[1], body=items[3])

    # auxiliry
    def suite(self, items):
        return list(items)
    def parameters(self, items):
        return list(items)
    def arguments(self, items):
        return list(items)

    # expressions
    def funccall(self, items):
        return Call(function=items[0], arguments=items[1])
    def var(self, data):
        return NameRef(data)

    # statements
    def expr_stmt(self, data):
        return Statement("expr", data)
    def assign_stmt(self, data):
        return Statement("assign", data)
    def del_stmt(self, data):
        return Statement("del", data)
    def pass_stmt(self, data):
        return Statement("pass", data)
    def break_stmt(self, data):
        return Statement("break", data)
    def continue_stmt(self, data):
        return Statement("continue", data)
    def return_stmt(self, data):
        return Statement("return", data)
    def yield_stmt(self, data):
        return Statement("yield", data)
    def raise_stmt(self, data):
        return Statement("raise", data)
    def import_stmt(self, data):
        return Statement("import", data)
    def global_stmt(self, data):
        return Statement("global", data)
    def nonlocal_stmt(self, data):
        return Statement("nonlocal", data)
    def assert_stmt(self, data):
        return Statement("assign", data)
    def async_stmt(self, data):
        return Statement("async", data)
    def if_stmt(self, data):
        return Statement("if", data)
    def while_stmt(self, data):
        return Statement("while", data)
    def for_stmt(self, data):
        return Statement("for", data)
    def try_stmt(self, data):
        return Statement("try", data)
    def with_stmt(self, data):
        return Statement("with", data)
    def match_stmt(self, data):
        return Statement("match", data)
    def NAME(self, data):
        return str(data)
    def STRING(self, data):
        # todo: strip quotes, handle interpreted stings, etc.
        return str(data)
    def LONG_STRING(self, data):
        # todo: strip quotes, handle interpreted stings, etc.
        return str(data)
    def DEC_NUMBER(self, data):
        return int(data, 10)
    def HEX_NUMBER(self, data):
        return int(data, 16)
    def OCT_NUMBER(self, data):
        return int(data, 8)
    def BIN_NUMBER(self, data):
        return int(data, 2)
    def FLOAT_NUMBER(self, data):
        raise RuntimeError("Float number not handled yet")
    def IMAG_NUMBER(self, data):
        raise RuntimeError("IMAG number not handled yet")