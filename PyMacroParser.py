# coding=utf-8
import sys
from enum import Enum


class PreTreamentOrder(Enum):
    IFDEF = "#ifdef"
    IFNDEF = "#ifndef"
    ELSE = "#else"
    ENDIF = "#endif"
    DEFINE = "#define"
    UNDEF = "#undef"


class PyMacroParser:
    codes = []
    pre_define_macros = []

    # 返回源代码去掉注释以及空行之后的代码，返回类型为list，代码的每一行作为list的item
    def load(self, f):
        try:
            with open(f) as base_file:
                code_with_comments = base_file.read()
                code_without_comments = remove_comments(code_with_comments)
                # print code_without_comments
                for code in code_without_comments.split("\n"):
                    if code.split():
                        self.codes.append(code)
        except BaseException as e:
            print e

    def preDefine(self, s):
        pre_define_s = s.split(";")
        if pre_define_s:
            pass
        else:
            self.pre_define_macros = []
        pass

    def dumpDict(self):
        code_read = []
        variable_defined = {}
        for i in range(0, len(self.codes)):
            code = self.codes[i].strip()
            order, variable, value = split_code(code)
            if order == PreTreamentOrder.DEFINE.value:
                variable_defined[varialbe] = value
            elif order == PreTreamentOrder.UNDEF.value:
                variable_defined[variable] = None
            elif order == PreTreamentOrder.IFDEF.value:
                endif_pos = find_endif(order, codes[i + 1:])
                else_pos = find_else(order, codes[i + 1:])
                if variable_defined.has_key(variable):
                    # 如果被定义了，那么直接找到与之对应的#endif
                    pass
                else:
                    pass

    def dump(self, f):
        pass

# 递归处理#ifdef或者#ifndef下的内容
def recursive_extract(codes):
    code_read = []
    variable_defined = {}




# 找到与order_if配对的#else, order_if可以是#ifdef也可以是#ifndef
def find_else(order_if, codes):
    order_list = []
    order_list.append(order_if)
    i = 1
    while i < len(codes):
        code = codes[i]
        order, variable, value = split_code(code)
        if order == PreTreamentOrder.IFDEF.value or order == PreTreamentOrder.IFNDEF.value:
            order_list.append(order)
        elif order == PreTreamentOrder.ELSE.value:
            if len(order_list) == 1:
                return i
            else:
                order_list.pop()
        i += 1
    return None


# 找到与order_if配对的#endif, order_if可以是#ifdef也可以是#ifndef
def find_endif(order_if, codes):
    order_list = []
    order_list.append(order_if)
    i = 1
    while i < len(codes):
        code = codes[i]
        order, variable, value = split_code(code)
        if order == PreTreamentOrder.IFDEF.value or order == PreTreamentOrder.IFNDEF.value:
            order_list.append(order)
        elif order == PreTreamentOrder.ENDIF.value:
            if len(order_list) == 1:
                return i
            else:
                order_list.pop()
        i += 1
    return None


# 将一行代码分为指令，参数，参数值三部分
def split_code(code):
    code = code.strip()
    if len(code.split()) == 1:
        return code.split()[0], None, None
    elif len(code.split()) == 2:
        order = code.split()[0].strip()
        variable = code.split()[1].strip()
        return order, variable, None
    else:
        order = code.split()[0].strip()
        variable = code.split()[1].strip()
        value = "".join(code.split()[2:])
        return order, variable, value


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
    a.load("test_find_if_else_end.cpp")
    print a.codes
    print "codes length: " + str(len(a.codes))
    print "else pos: " + str(find_else(PreTreamentOrder.IFNDEF.value, a.codes))
    print "end pos: " + str(find_endif(PreTreamentOrder.IFNDEF.value, a.codes))


if __name__ == '__main__':
    main()
