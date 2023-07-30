__author__ = 'Zhifei Chen'

# match patterns & record methods scope
# del delattr containers,


import _ast
import ast

import astunparse


class PatternAST(ast.NodeVisitor):

    def __init__(self):
        self.source = None
        self.methods = []  # 'method', 'params', 'startlineno', 'endlineno'
        self.patterns = []  # delname/delsubscript/delattribute, getattr/hasattr/delattr

    @staticmethod
    def count_lines(node):
        childnodes = list(ast.walk(node))
        lines = set()
        for n in childnodes:
            if hasattr(n, 'lineno'):
                lines.add(n.lineno)
        return min(lines), max(lines)

    def visit_FunctionDef(self, node):
        funcName = node.name.strip()
        stmt = astunparse.unparse(node.args)
        arguments = stmt.strip().split(",")
        arguments = [a.lstrip().rstrip() for a in arguments]
        startlineno, endlineno = self.count_lines(node)
        self.methods.append([funcName, ', '.join(arguments), startlineno, endlineno])
        self.generic_visit(node)

    # 'getattr', 'hasattr', 'delattr'
    def visit_Call(self, node):
        funcName = astunparse.unparse(node.func).strip()
        if funcName in ('getattr', 'hasattr', 'delattr'):
            self.patterns.append([funcName, node.lineno])
        self.generic_visit(node)

    def traverseDelTargets(self, targets, lineno):
        for t in targets:
            if isinstance(t, _ast.Tuple):
                self.traverseDelTargets(t.elts, lineno)
            elif isinstance(t, _ast.Name):
                self.patterns.append(['delname', lineno, t.id])
            elif isinstance(t, _ast.Subscript):
                self.patterns.append(['delsubscript', lineno])
            elif isinstance(t, _ast.Attribute):
                self.patterns.append(['delattribute', lineno])

    # del name, del subscript, del attribute
    def visit_Delete(self, node):
        self.traverseDelTargets(node.targets, node.lineno)
        self.generic_visit(node)

    # def visit_TryExcept(self, node):
    #     self.trySet.append(node.body)
    #     self.handlerSet.append(node.handlers)
    #     expset = []
    #     for handle in node.handlers:
    #         # print handle.type
    #         if handle.type is not None:
    #             expset.append(astunparse.unparse(handle.type).rstrip('\n'))
    #         else:
    #             expset.append('')
    #     self.exceptionSet.append(expset)
    #     self.orelseSet.append(node.orelse)
    #     self.generic_visit(node)
    #
    # def reset(self):
    #     del self.trySet[:]


if __name__ == '__main__':
    myAst = PatternAST()
    # myAst.reset()
    f = open('test.py', 'r')
    lines = f.read()
    f.close()
    n = ast.parse(lines)
    myAst.visit(n)
    for item in myAst.patterns:
        print(item)
    for m in myAst.methods:
        print(m)
    # print 'try:\n',myAst.trySet
    # print 'handler:\n',myAst.handlerSet
    # print 'exception:\n',myAst.exceptionSet
    # print 'orelse:\n', myAst.orelseSet
