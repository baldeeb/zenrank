# inspired by http://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang/

import sys
import os
import re
import clang.cindex
import parser.node
import nodeTools

def is_system_header(cursor):
    return cursor.location.file is not None and cursor.location.file.name.startswith('/usr')


class Parser:

    def __init__(self):
        self.nodes = {};

    def parse_repo(self, repo_folder):
        print(repo_folder)
        result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(repo_folder) for f in filenames if re.match('.*\.[hc][p]*$', f)]

        print(result)

        for file in result:
            print(file)
            self.parse_file(file)

        for key,node in self.nodes.items():
            print (node.name(), node.keywords)

        repo = nodeTools.Node('uhad_fusion')
        classes = [node for node in self.nodes.values() if node.kind  is clang.cindex.CursorKind.CLASS_DECL]
        klassNodes = nodeTools.connectListToNode([klass.name() for klass in classes], repo)
        for node in klassNodes:
            klass = self.nodes[node.name]
            methodNames = [method.name() for method in klass.children]
            methodNodes = nodeTools.connectListToNode(methodNames, node)


    def parse_file(self, file):
        index = clang.cindex.Index.create()
        tu = index.parse(file, ['-I/home/jashar/Code/uhad_fusion_refactor/src'])
        self.walk_tree(tu.cursor);

    def parse_node(self, cursor, parent):
        node = parser.node.Node(parent)
        node.parse(cursor)

        if parent is not None:
            parent.children.append(node)

        id = node.name()

        if id in self.nodes:
            self.nodes[id].merge_with(node)
        else:
            self.nodes[id] = node

        for c in cursor.get_children():
            self.walk_tree(c, node)

    def walk_tree(self, cursor, parent=None):
        parse_children = True
        if parser.node.is_node(cursor) and not is_system_header(cursor):
            self.parse_node(cursor, parent)
            parse_children = False

        if parse_children:
            for c in cursor.get_children():
                self.walk_tree(c, parent)


if __name__ == '__main__':
    p = Parser()
    p.parse_repo(sys.argv[1])
