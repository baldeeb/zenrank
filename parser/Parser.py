# inspired by http://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang/

import sys
import clang.cindex

import parser.Method


class Repo:
    def __init__(self):
        self.classes = [];


def verbose(*args, **kwargs):
    '''filter predicate for show_ast: show all'''
    return True


def no_system_includes(cursor, level):
    '''filter predicate for show_ast: filter out verbose stuff from system include files'''
    return (level != 1) or (
                cursor.location.file is not None and not cursor.location.file.name.startswith('/usr/include'))


# A function show(level, *args) would have been simpler but less fun
# and you'd need a separate parameter for the AST walkers if you want it to be exchangeable.
class Level(int):
    '''represent currently visited level of a tree'''

    def show(self, *args):
        '''pretty print an indented line'''
        print(
        '\t' * self + ' '.join(map(str, args)))

    def __add__(self, inc):
        '''increase level'''
        return Level(super(Level, self).__add__(inc))


class Parser:

    def __init__(self):
        self.repos = [];
        self.methods = {};

    def parse_repo(self, repo_folder):
        pass

    def parse_file(self, file):
        index = clang.cindex.Index.create()
        tu = index.parse(file)
        self.walk_tree(tu.cursor, no_system_includes);

        for method in self.methods:
            print(method.name, ": called ", method.times_called, " times")

    def is_method(self, cursor):
        return cursor.kind is clang.cindex.CursorKind.CXX_METHOD

    def handle_method(self, cursor, level):
        level.show("Method: ", cursor.kind, cursor.get_usr())
        unique_id = cursor.get_usr()
        if unique_id in self.methods:
            method = self.methods[unique_id]
        else:
            method = parser.Method.Method()

        if method is not None:
            method.parse(cursor)


    def walk_tree(self, cursor, predicate=verbose, level=Level()):
        if predicate(cursor, level):
            # level.show(cursor.kind, cursor.spelling, cursor.displayname, cursor.location)
            parse_children = True
            if self.is_method(cursor):
                self.handle_method(cursor, level)
                parse_children = False

            if parse_children:
                for c in cursor.get_children():
                    self.walk_tree(c, predicate, level + 1)



if __name__ == '__main__':
    p = Parser()
    p.parse_file(sys.argv[1])
