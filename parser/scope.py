import clang.cindex
import parser.keywords


def is_node(cursor):
    node_kinds = set([clang.cindex.CursorKind.CXX_METHOD, \
                     clang.cindex.CursorKind.CLASS_DECL, \
                     clang.cindex.CursorKind.NAMESPACE])
    return cursor.kind in node_kinds

def class_from_type_ref(cursor):
    type_name = cursor.displayname;
    parts = type_name.split()
    if len(parts) == 2:  # 'class Foo'
        type_name = parts[1]
    return type_name

class Scope:

    def __init__(self, parent=None):
        self.id = None
        self.kind = None
        self.keywords = {}
        self.use_count = 1
        self.base_name = ''
        self.parent = parent
        self.children = []
        self.varNameToType = {}

    def name(self):
        rv = ''
        if self.parent is not None:
            rv = self.parent.name() + '::'
        return rv + self.base_name

    def add_keywords_from(self, text):
        for word in parser.keywords.find_keywords(text):
            self.keywords[word] = self.keywords.get(word, 0) + 1

    def recursive_search_for(self, cursor, kind):
        if cursor.kind is kind:
            return cursor

        for c in cursor.get_children():
            found = self.recursive_search_for(c, kind)
            if found is not None:
                return found

    def parse_var_decl(self, db, cursor):
        var_name = cursor.displayname
        self.add_keywords_from(var_name)

        typeCursor = self.recursive_search_for(cursor, clang.cindex.CursorKind.TYPE_REF)
        if typeCursor is not None:
            typename = class_from_type_ref(typeCursor)
            if typename in db:
                classNode = db[typename]
                classNode.use_count += 1
                self.varNameToType[var_name] = classNode

    def parse_call_expr(self, db, cursor):
        methodName = cursor.displayname
        self.add_keywords_from(methodName)

        memberRefExprCursor = self.recursive_search_for(cursor, clang.cindex.CursorKind.MEMBER_REF_EXPR)
        if memberRefExprCursor is None:
            return

        declRefExprCursor = self.recursive_search_for(memberRefExprCursor, clang.cindex.CursorKind.DECL_REF_EXPR)
        if declRefExprCursor is None:
            tempScope = Scope(self.parent)
            tempScope.base_name = methodName + '()';#TODO: Handle method call with arguments
            if tempScope.name() in db:
                actualNode = db[tempScope.name()]
                actualNode.use_count += 1
        else:
            var_name = declRefExprCursor.displayname
            var_type = self.varNameToType[var_name]
            for child in var_type.children:
                if methodName in child.base_name:
                    child.use_count += 1


    def parse_block(self, db, cursor):
        if cursor.kind is clang.cindex.CursorKind.VAR_DECL:
            self.parse_var_decl(db, cursor)
        elif cursor.kind is clang.cindex.CursorKind.CALL_EXPR:
            self.parse_call_expr(db, cursor)

        if cursor.kind is clang.cindex.CursorKind.TYPE_REF:
            type_name = class_from_type_ref(cursor)
            if type_name in db:
                klass = db[type_name]
                klass.use_count += 1

        comment = cursor.raw_comment;
        if comment is not None:
            self.add_keywords_from(comment)

        for child in cursor.get_children():
            self.parse_block(db, child)

    def parse(self, db, cursor):
        self.kind = cursor.kind
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
                self.parse_block(db, c)
            if c.kind is clang.cindex.CursorKind.TYPE_REF:
                type_name = class_from_type_ref(c)
                self.parent = parser.scope.Scope(self.parent)
                self.parent.base_name = type_name


    def merge_with(self, other_node):
        for key in other_node.keywords:
            self.keywords[key] = self.keywords.get(key,0) + other_node.keywords[key]

