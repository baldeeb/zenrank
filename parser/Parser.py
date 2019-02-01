# inspired by http://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang/

import sys
import os
import re
import clang.cindex
import parser.scope
import nodeTools
import builder

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
            print (node.name(), node.use_count, node.keywords)

        repo = nodeTools.Node('uhad_fusion')
        classes = [node for node in self.nodes.values() if node.kind  is clang.cindex.CursorKind.CLASS_DECL]
        classNames = [klass.name() for klass in classes]
        klassNodes = nodeTools.connectListToNode(classNames, repo)
        for node in klassNodes:
            klass = self.nodes[node.name]
            node.baseWeight = klass.use_count
            nodeTools.connectKeywordsToNode(klass.keywords, node)

            if len(klass.children) > 0:
                methodNames = [method.name() for method in klass.children]
                methodNodes = nodeTools.connectListToNode(methodNames, node)

                for methodNode in methodNodes:
                    method = self.nodes[methodNode.name]
                    methodNode.baseWeight = method.use_count
                    nodeTools.connectKeywordsToNode(method.keywords, methodNode)

        nodeTools.printGraph(nodeTools.keywordDict)


    def parse_file(self, file):
        index = clang.cindex.Index.create()
        tu = index.parse(file, ['-I/home/jashar/Code/uhad_fusion_refactor/src'])
        self.walk_tree(tu.cursor);

    def parse_node(self, cursor, parent):
        node = parser.scope.Scope(parent)
        node.parse(self.nodes, cursor)

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
        if parser.scope.is_node(cursor) and not is_system_header(cursor):
            self.parse_node(cursor, parent)
            parse_children = False

        if parse_children:
            for c in cursor.get_children():
                self.walk_tree(c, parent)


if __name__ == '__main__':
    p = Parser()
    p.parse_repo(sys.argv[1])

    searchwords = {"distance", "Pythagorous", "D"}
    import matcher
    import ranker
    matcher.matchKeyWordsToSearchWords(nodeTools.keywordDict, searchwords, verbose=True)
    ranker.rankGraph(nodeTools.keywordDict)

    # printGraph(keywordDict)

    results = builder.collectResults(nodeTools.keywordDict)

    for (key, value) in results:
        print("Word: " + key + ", Rank: " + str(value))
