# coding=utf-8
import sys
from enum import Enum


class PyMacroParser:
    codes = []
    pre_define_macros = {}

    def load(self, f):
        try:
            with open(f) as base_file:
                code_with_comments = base_file.read()
                code_without_comments = remove_comments(code_with_comments)
                for code in code_without_comments.split("\n"):
                    if code.split():
                        self.codes.append(code)
        except BaseException as e:
            print e

    def preDefine(self, s):
        if self.pre_define_macros:
            self.pre_define_macros.clear()
        if s:
            if len(s.split(";")) != 0:
                for macro_name in s.split(";"):
                    self.pre_define_macros[macro_name] = None

    def dumpDict(self):
        pass

    def dump(self):
        pass


def recursive_extract(codes, variable_defined):
    i = 0
    while i < len(codes):
        code = codes.strip()


def split_code(code):
    code = code.strip()[1:]
    if len(code.split()) == 1:
        return "#" + code.split()[0].strip(), None, None
    elif len(code.split()) == 2:
        order = code.split()[0].strip()
        variable = code.split()[1].strip()
        return "#" + order, variable, None
    else:
        order = code.split()[0].strip()
        variable = code.split()[1].strip()
        value_index = code.find(variable) + len(variable)
        value = code[value_index:].strip()
        return "#" + order, variable, value


# 从初始的C++代码中去除注释，返回string为去除注释的c++代码
def remove_comments(code_with_comments):
    code_length = len(code_with_comments)
    index = 0
    state = 0
    code_without_comments = ""
    while index < code_length:
        c = code_with_comments[index]
        if state == 0 and c == '/':
            state = 1
        elif state == 1 and c == '*':
            state = 2
        elif state == 1 and c == '/':
            state = 4
        elif state == 1:
            # sys.stdout.write(c)
            code_without_comments += c
            state = 0
        elif state == 2 and c == '*':
            state = 3
        elif state == 2:
            state = 2
        elif state == 3 and c == '/':
            state = 0
        elif state == 3:
            state = 2

        elif state == 4 and c == '\\':
            state = 9
        elif state == 9 and c == '\\':
            state = 9
        elif state == 9:
            state = 4
        elif state == 4 and c == '\n':
            state = 0

        elif state == 0 and c == '\'':
            state = 5
        elif state == 5 and c == '\\':
            state = 6
        elif state == 6:
            state = 5
        elif state == 5 and c == '\'':
            state = 0
        elif state == 0 and c == '\"':
            state = 7
        elif state == 7 and c == '\\':
            state = 8
        elif state == 8:
            state = 7
        elif state == 7 and c == '\"':
            state = 0
        index += 1
        if (state == 0 and c != '/'
            ) or state == 5 or state == 6 or state == 7 or state == 8:
            # sys.stdout.write(c)
            code_without_comments += c
    return code_without_comments


def main():
    code = '# define data6 {1, 6, {" "}, "  ", "this    is\n data"}'
    print split_code(code)

if __name__ == '__main__':
    main()