
"""
import ast

def find_methods_in_python_file(file_path):
    methods = []
    classes = []
    other = []
    o = open(file_path, "r")
    text = o.read()
    p = ast.parse(text)
    for node in ast.walk(p):
        if isinstance(node, ast.FunctionDef):
            methods.append(node.name)
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        if isinstance(node, ast.Expr):
            other.append(node.name)

    print(methods, '\n\n', classes, "\n\n", other)
"""

'''
import ast
from pprint import pprint


def main():
    with open(input(), "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(alias.name)
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)


if __name__ == "__main__":
    main()

#https://www.mattlayman.com/blog/2018/decipher-python-ast/
'''
'''
import ast

class FuncLister(ast.NodeVisitor):

    def visit_FunctionDef(self, node):
        print('FunctionDef', node.name)
        self.generic_visit(node)

with open(input(), 'r') as f:
    tree = ast.parse(f.read())
    print(FuncLister().visit(tree))

'''


import ast

def walk (node):
    """ast.walk() skips the order, just walks, so tracing is not possible with it."""
    end = []
    end.append(node)
    for n in ast.iter_child_nodes(node):
        # Consider it a leaf:
        if isinstance(n, ast.Call):
            end.append(n)
            continue
        end += walk(n)
    return end

def calls (tree):
    """Prints out exactly where are the calls and what functions are called."""
    tree = walk(tree) # Arrange it into our list
    # First get all functions in our code:
    functions = {}
    for node in tree:
        if isinstance(node, (ast.FunctionDef, ast.Lambda)):
            functions[node.name] = node
    # Find where are all called functions:
    stack = []
    for node in tree:
        if isinstance(node, (ast.FunctionDef, ast.Lambda)):
            # Entering function
            stack.append(node)
        elif stack and hasattr(node, "col_offset"):
            if node.col_offset<=stack[-1].col_offset:
                # Exit the function
                stack.pop()
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                fname = node.func.value.id+"."+node.func.attr+"()"
            else: fname = node.func.id+"()"
            try:
                ln = functions[fname[:-2]].lineno
                ln = "at line %i" % ln
            except: ln = ""
            print ("Line", node.lineno, "--> Call to", fname, ln)
            if stack:
                print ("from within", stack[-1].name+"()", "that starts on line", stack[-1].lineno)
            else:
                print ("directly from root")

code = """
import os

def f1 ():
    print ("I am function 1")
    return "This is for function 2"

def f2 ():
    print (f1())
    def f3 ():
        print( "I am a function inside a function!")
    f3()
f2()
print ("My PID:", os.getpid())
"""

tree = ast.parse(code)

calls(tree)
