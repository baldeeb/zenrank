import clang.cindex
import parser.keywords


def is_node(cursor):
    node_kinds = set([clang.cindex.CursorKind.CXX_METHOD, \
                     clang.cindex.CursorKind.CLASS_DECL, \
                     clang.cindex.CursorKind.NAMESPACE])
    return cursor.kind in node_kinds

class Node:

    def __init__(self, parent=None):
        self.id = None
        self.keywords = {}
        self.base_name = ''
        self.parent = parent

    def name(self):
        rv = ''
        if self.parent is not None:
            rv = self.parent.name() + '::'
        return rv + self.base_name

    def add_keywords_from(self, text):
        for word in parser.keywords.find_keywords(text):
            self.keywords[word] = self.keywords.get(word, 0) + 1

    def parse_block(self, cursor):
        self.kind = cursor.kind
        if cursor.kind is clang.cindex.CursorKind.VAR_DECL or cursor.kind is clang.cindex.CursorKind.CALL_EXPR:
            self.add_keywords_from(cursor.spelling)

        comment = cursor.raw_comment;
        if comment is not None:
            self.add_keywords_from(comment)

        for child in cursor.get_children():
            self.parse_block(child)


    def parse(self, cursor):
        self.id = cursor.get_usr()
        comment = cursor.brief_comment;
        if comment is not None:
            self.add_keywords_from(comment)

        self.base_name = cursor.displayname
        self.add_keywords_from(cursor.spelling)
        for c in cursor.get_children():
            if c.kind is clang.cindex.CursorKind.PARM_DECL:
                self.add_keywords_from(c.spelling)
            if c.kind is clang.cindex.CursorKind.COMPOUND_STMT:
                self.parse_block(c)
            if c.kind is clang.cindex.CursorKind.TYPE_REF:
                type_name = c.displayname;
                parts = type_name.split()
                if len(parts) == 2:# 'class Foo'
                    type_name = parts[1]
                self.parent = parser.node.Node(self.parent)
                self.parent.base_name = type_name


    def merge_with(self, other_node):
        for key in other_node.keywords:
            self.keywords[key] = self.keywords.get(key,0) + other_node.keywords[key]

