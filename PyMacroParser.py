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
    pre_define_macros = {}

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
        if self.pre_define_macros:
            self.pre_define_macros.clear()
        if len(s.split(";")) != 0:
            for macro_name in s.split(";"):
                self.pre_define_macros[macro_name] = None

    def dumpDict(self):
        macros_dict = recursive_extract(self.codes, self.pre_define_macros)
        for macro_item in macros_dict.items():
            pass
        return macros_dict

    def dump(self, f):
        pass

# 判断宏值所属的类型
def choose_type(macro_value):
    pass



# 整数常量转化
def change_Ingeger(origin_value):
    pass
def change_float(origin_value):
    pass
def change_char(origin_value):
    pass
def change_string(origin_value):
    pass
def change_union(origin_value):
    pass

# 布尔常量转换    
def change_bool(origin_value):
    if origin_value.lower() == "true":
        return True
    else:
        return False


# 递归处理内容
def recursive_extract(codes, variable_defined):
    # variable_defined = {}
    i = 0
    while i < len(codes):
        code = codes[i].strip()
        order, variable, variable_value = split_code(code)
        if order == PreTreamentOrder.DEFINE.value:
            variable_defined[variable] = variable_value
            i += 1
        elif order == PreTreamentOrder.UNDEF.value:
            if variable_defined.has_key(variable):
                variable_defined.pop(variable)
            i += 1
        elif order == PreTreamentOrder.IFNDEF.value:
            else_pos = find_else(order, codes[i:])
            end_pos = find_endif(order, codes[i:])
            if not variable_defined.has_key(variable):
                if else_pos != None:
                    recursive_extract(codes[i + 1:i + else_pos],
                                      variable_defined)                    
                else:
                    recursive_extract(codes[i + 1:i + end_pos],
                                      variable_defined)
            elif variable_defined.has_key(variable):
                if else_pos != None:
                    recursive_extract(codes[i + else_pos:i + end_pos],
                                      variable_defined)
                # else:
                #     recursive_extract(codes[i + 1:i + end_pos],
                #                       variable_defined)
            i += end_pos
        elif order == PreTreamentOrder.IFDEF.value:
            else_pos = find_else(order, codes[i:])
            end_pos = find_endif(order, codes[i:])
            if variable_defined.has_key(variable):
                if else_pos != None:
                    recursive_extract(codes[i + 1:i + else_pos],
                                      variable_defined)                    
                else:
                    recursive_extract(codes[i + 1:i + end_pos],
                                      variable_defined)
            elif not variable_defined.has_key(variable):
                if else_pos != None:
                    recursive_extract(codes[i + else_pos:i + end_pos],
                                      variable_defined)
                else:
                    recursive_extract(codes[i + 1:i + end_pos],
                                      variable_defined)
            i += end_pos
        elif order == PreTreamentOrder.ENDIF.value or order == PreTreamentOrder.ELSE.value:
            i += 1
        
    return variable_defined


# 找到与order_if配对的#else, order_if可以是#ifdef也可以是#ifndef
# 返回的是#else在codes中的位置，没有则返回None
def find_else(order_if, codes):
    i = 1
    end_pos = find_endif(order_if, codes)
    while i < len(codes[:end_pos]):
        code = codes[i]
        order, variable, variable_value = split_code(code)
        if order == PreTreamentOrder.IFDEF.value or order == PreTreamentOrder.IFNDEF.value:
            i += find_endif(order, codes[i:end_pos])
            continue
        elif order == PreTreamentOrder.ELSE.value:
            return i
        i += 1
    return None


# 找到与order_if配对的#endif, order_if可以是#ifdef也可以是#ifndef
# 返回的是#endif在codes中的位置，没有则返回None
def find_endif(order_if, codes):
    order_list = []
    order_list.append(order_if)
    i = 1
    while i < len(codes):
        code = codes[i]
        order, variable, variable_value = split_code(code)
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
        return code.split()[0].strip(), None, None
    elif len(code.split()) == 2:
        order = code.split()[0].strip()
        variable = code.split()[1].strip()
        return order, variable, None
    else:
        order = code.split()[0].strip()
        variable = code.split()[1].strip()
        value = " ".join(code.split()[2:])
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
    a.load("a.cpp")
    # a.preDefine("MC1;MC2")
    variable_defined = recursive_extract(a.codes, a.pre_define_macros)
    for item in variable_defined.items():
        print item
    # a.load("testFindIfElseEnd.cpp")
    # print find_else(PreTreamentOrder.IFDEF.value, a.codes)
    # print find_endif(PreTreamentOrder.IFDEF.value, a.codes)

if __name__ == '__main__':
    main()
