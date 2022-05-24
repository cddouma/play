import string
import sys
from typing import Any, Dict
from dataclasses import dataclass, field

from lark import Lark, Transformer
from lark.indenter import PythonIndenter


from typing import Any, Dict
from dataclasses import dataclass, field

import IR, Callgraph

class Parser:
    def __init__(self) -> None:
        self.python3 = Lark.open_from_package('lark', 'python.lark', ['grammars'], 
                            parser='lalr', postlex=PythonIndenter(), start='file_input')

    def parsePython2IR(self, path):
        with open(path, 'r') as inputfile:
            return python_parser3.parse(inputfile.read(), transformer=graphs.IR.Python2SimpleIR().transform())
    
    def parsePython2Callgraph(self, path):
        with open(path, 'r') as inputfile:
            return python_parser3.parse(inputfile.read(), transformer=graphs.Callgraph.Python2Callgraph().transform())


def main(args):
    print("hello world, this is me:")
    python_parser3 = Lark.open_from_package('lark', 'python.lark', ['grammars'], 
                                            parser='lalr', postlex=PythonIndenter(), start='file_input')
    with open("input/basic.py", 'r') as inputfile:
        tree = python_parser3.parse(inputfile.read())
        print(f"tree: {tree}")

    print("IR")
    ir = IR.Python2SimpleIR().transform(tree)
    print(ir)

    print("Callgraph")
    cg = Callgraph.python2Callgraph(tree)
    print(cg.nodes)
    print(cg.edges)

if __name__ == "__main__":
    main(sys.argv)
