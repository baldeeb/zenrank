
import clang.cindex


class Method:

    def __init__(self):
        self.comments = []
        self.variable_names = [];
        self.times_called = 0

    def add_to_call_count(self):
        self.times_called = self.times_called + 1

    def add_comment(self, comment):
        self.comments.append(comment)

    def parse(self, cursor):
        # comment = cursor.brief_comment();
        # if comment is not None:
        #     self.comments.append(comment)

        for c in cursor.get_children():
            if c.kind is clang.cindex.CursorKind.PARM_DECL:
                self.variable_names.append(c.spelling)
            if c.kind is clang.cindex.CursorKind.COMPOUND_STMT:
                pass
