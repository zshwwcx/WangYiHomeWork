# coding=utf-8
import sys
from enum import Enum


class PreTreament(Enum):
    IFDEF = "#ifdef"
    IFNDEF = "#ifndef"
    ELSE = "#else"
    ENDIF = "#endif"
    DEFINE = "#define"
    UNDEF = "#undef"


class PyMacroParser:
    pre_define = ""

    # 返回源代码去掉注释以及空行之后的代码，返回类型为list
    def load(self, f):
        load_return = []
        try:
            with open(f) as base_file:
                code_with_comments = base_file.read()
                code_without_comments = remove_comments(code_with_comments)
                # print code_without_comments
                for code in code_without_comments.split("\n"):
                    if code.split():
                        load_return.append(code)
                return load_return
        except BaseException as e:
            print e
            return None

    def preDefine(self, s):
        pass

    def dumpDict(self):
        pass

    def dump(self, f):
        pass


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
        if (state == 0 and c != '/') or state == 5 or state == 6 or state == 7 or state == 8:
            # sys.stdout.write(c)
            code_without_comments += c
    return code_without_comments


def test_example():
    a1 = PyMacroParser()
    a2 = PyMacroParser()
    a1.load("a.cpp")
    filename = "b.cpp"
    a1.dump(filename)
    a2.load(filename)
    a2.dumpDict()
    a1.preDefine("MC1;MC2")
    a1.dumpDict()
    a1.dump("c.cpp")


def main():
    a = PyMacroParser()
    code_without_comments = a.load("a.cpp")
    for code in code_without_comments:
        print code


if __name__ == '__main__':
    main()
