__author__ = 'Zhifei Chen'

import ast
import _ast


def combineClassGroup(class_group, new_set):  # class_group: [set,set]
    combined_set = new_set.copy()
    for new_class in new_set:
        for class_set in class_group:
            if new_class in class_set:
                combined_set = class_set | combined_set
                class_group.remove(class_set)
    class_group.append(combined_set)
    return class_group


class ClassStructureAST(ast.NodeVisitor):

    def __init__(self, classgroups):
        self.classgroups = classgroups

    def visit_ClassDef(self, node):
        new_class = set([node.name])
        for item in node.bases:
            if isinstance(item, _ast.Name):
                new_class.add(item.id)
            elif isinstance(item, _ast.Attribute):
                new_class.add(item.attr)
        combineClassGroup(self.classgroups, new_class)
        # print new_class, self.classgroups


if __name__ == '__main__':
    myAst = ClassStructureAST([])
    # myAst.reset()
    f = open('test.py', 'r')
    lines = f.read()
    f.close()
    n = ast.parse(lines)
    myAst.visit(n)
    print(myAst.classgroups)

    # print(combineClassGroup([set(['qq','ww']), set(['ee',])], set(['ee', 'rr'])))
    # print(combineClassGroup([set(['qq','ww']), set(['ee',])], set(['rr'])))
    # print(combineClassGroup([set(['qq','ww']), set(['ee',])], set(['ee', 'rr', 'qq'])))
