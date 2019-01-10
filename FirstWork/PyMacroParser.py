# coding=gbk

class PyMacroParser:
    pre_define_macros = {}
    codes = []

    # ����Դ����ȥ��ע���Լ�����֮��Ĵ��룬��������Ϊlist�������ÿһ����Ϊlist��item
    def load(self, f):
        if self.codes:
            self.codes = []
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
        if s:
            if len(s.split(";")) != 0:
                for macro_name in s.split(";"):
                    if macro_name.split():
                        self.pre_define_macros[macro_name.strip()] = None

    def dumpDict(self):
        temp_macros = self.pre_define_macros
        origin_macros_dict = recursive_extract(self.codes,
                                               temp_macros)
        new_macros_dict = {}
        for origin_macro_key in origin_macros_dict.keys():
            origin_macro_value = origin_macros_dict[origin_macro_key]
            new_macros_dict[origin_macro_key] = choose_type(origin_macro_value)
        return new_macros_dict

    def dump(self, f):
        with open(f, 'w') as dump_write:
            macro_values = self.dumpDict()
            for macro_key in macro_values.keys():
                macro_c_value = ""
                if type(macro_values[macro_key]) is int or type(macro_values[macro_key]) is float:
                    macro_c_value = str(macro_values[macro_key])
                elif type(macro_values[macro_key]) is str or type(macro_values[macro_key]) is unicode:
                    if type(macro_values[macro_key]) is unicode:
                        macro_c_value = translate_string_to_c('"' + macro_values[macro_key] + '"')
                    else:
                        macro_c_value = translate_string_to_c('"' + macro_values[macro_key] + '"')
                elif type(macro_values[macro_key]) is tuple:
                    macro_c_value = translate_union_to_c(macro_values[macro_key])
                elif type(macro_values[macro_key]) is bool:
                    if macro_values[macro_key] is False:
                        macro_c_value = 'false'
                    else:
                        macro_c_value = 'true'
                else:
                    macro_c_value = ""
                dump_write.write("#define " + macro_key + " " + macro_c_value + "\n")


# ��tupleתΪc�еľۺ�
def translate_union_to_c(value):
    i = 0
    macro_c_value = "{"
    while i < len(value):
        if type(value[i]) is int or type(value[i]) is float:
            symbol = ","
            if i == len(value) - 1:
                symbol = ""

            macro_c_value = macro_c_value + str(value[i]) + symbol
            i += 1
        elif type(value[i]) is str or type(value[i]) is unicode:
            symbol = ","
            if i == len(value) - 1:
                symbol = ""

            if value[i].startswith('u\"'):
                macro_c_value = macro_c_value + translate_string_to_c(value[i]) + symbol
            else:
                macro_c_value = macro_c_value + translate_string_to_c('"' + value[i] + '"') + symbol
            i += 1
        elif type(value[i]) is bool:
            symbol = ","
            if i == len(value) - 1:
                symbol = ""

            if value[i] is False:
                macro_c_value = macro_c_value + 'false' + symbol
            else:
                macro_c_value = macro_c_value + 'true' + symbol
            i += 1
        elif type(value[i]) is tuple:
            symbol = ","
            if i == len(value) - 1:
                symbol = ""
            macro_c_value = macro_c_value + translate_union_to_c(value[i]) + symbol
            i += 1
    macro_c_value += "}"
    return macro_c_value


# ��python�е�stringתΪc�е�string
def translate_string_to_c(value):
    write_str = ""
    if type(value) is unicode:
        write_str = "L"
    i = 0
    while i in range(0, len(value)):
        if value[i] == "\t":
            write_str += "\\t"
            i += 1
        elif value[i] == "\n":
            write_str += "\\n"
            i += 1
        elif value[i] == "\r":
            write_str += '\\r'
            i += 1
        elif value[i] == "\a":
            write_str += "\\a"
            i += 1
        elif value[i] == "\b":
            write_str += "\\b"
            i += 1
        elif value[i] == "\f":
            write_str += "\\f"
            i += 1
        elif value[i] == "\v":
            write_str += "\\v"
            i += 1
        elif value[i] == "\\":
            write_str += "\\\\"
            i += 1
        elif value[i] == "\?":
            write_str += "\\?"
            i += 1
        elif value[i] == "\'":
            write_str += "\\'"
            i += 1
        elif value[i] == '\"':
            if i == 0 or i == len(value) - 1:
                write_str += '"'
            else:
                write_str += '\\"'
                #
                # j = i - 1
                # if j > 0:
                #     count = 0
                #     while j > 0:
                #         if value[j] == '\\':
                #             count += 1
                #             j -= 1
                #         else:
                #             break
                #     if count % 2 == 0:
                #         write_str += '\"'
                #     else:
                #         write_str += '\\"'
                # else:
                #     write_str += '\"'
            i += 1

        else:
            write_str += value[i]
            i += 1
    return write_str


def choose_type(macro_value):
    try:
        if isinstance(macro_value, str):
            if is_integer_constant(macro_value) is not None:
                # print "is_integer_constant:"
                return is_integer_constant(macro_value)
            elif is_float_point_constant(macro_value) is not None:
                # print "is_float_constant:"
                return is_float_point_constant(macro_value)
            elif is_bool_constant(macro_value) is not None:
                # print "is_bool_constant:"
                return is_bool_constant(macro_value)
            elif is_character_constant(macro_value) is not None:
                # print "is_character_constant:"
                return is_character_constant(macro_value)
            elif is_string_constant(macro_value) is not None:
                return is_string_constant(macro_value)
            elif is_union_constant(macro_value) is not None:
                return is_union_constant(macro_value)
        else:
            return None
    except BaseException as e:
        print "error: " + macro_value, e
        return None


# �ж��ǲ������ͳ���, ���򷵻�ת��֮���ֵ�������򷵻�None
def is_integer_constant(macro_value):
    macro_value = macro_value.lower().strip()
    try:
        if macro_value.count("\"") == 0 and macro_value.count(
                "'") == 0 and macro_value.count('.') == 0 and macro_value.count('{') == 0:
            if macro_value[0].isdigit():
                symbol = ""
            else:
                for i in range(0, len(macro_value)):
                    if macro_value[i].isdigit():
                        break
                minus_count = macro_value.count('-')
                macro_value = macro_value[i:]
                if minus_count % 2 == 0:
                    symbol = ""
                else:
                    symbol = "-"
            if (macro_value.isdigit() and not macro_value.startswith('0')) or (
                            macro_value.isdigit() and macro_value.startswith('0')
                    and len(macro_value) == 1):
                return int(symbol + macro_value)
            elif macro_value.startswith(
                    '0') and not macro_value.startswith('0x'):
                # ����8����
                value_data = macro_value[0:len(macro_value)]
                for i in range(0, len(value_data)):
                    if not value_data[i].isdigit():
                        break
                if i == len(value_data) - 1 and value_data[i].isdigit():
                    value_data = value_data[:i + 1]
                else:
                    value_data = value_data[:i]
                return int(symbol + value_data, 8)
            elif macro_value.startswith('0x'):
                # ����16����
                value_data = macro_value[2:len(macro_value)]
                for i in range(0, len(value_data)):
                    # if not (value_data[i].isalpha()
                    #         and ord(value_data[i].lower()) in range(
                    #         97, 102 + 1)) and not value_data[i].isdigit():
                    #     break
                    if (not (value_data[i].isalpha() and value_data[i].lower() in "abcdef")) and (
                            not value_data[i].isdigit()):
                        break
                if i == len(value_data) - 1 and (value_data[i].isdigit() or value_data[i].lower() in "abcdef"):
                    value_data = value_data[:i + 1]
                else:
                    value_data = value_data[:i]
                return int(symbol + value_data, 16)
            else:
                # ����10����
                # ���2e-3���֡���
                if macro_value.count('e') == 0:
                    for i in range(0, len(macro_value)):
                        if not macro_value[i].isdigit():
                            break
                    if i == len(macro_value) - 1:
                        macro_value = macro_value[:i]

                    else:
                        macro_value = macro_value[:i]
                    return int(symbol + macro_value)
    except:
        return None


# �ж��ǲ��Ǹ��㳣��
def is_float_point_constant(macro_value):
    # ��ʱ�Ȳ������������Ƶĸ��㳣��
    try:
        macro_value = macro_value.lower().strip()
        symbol = ""
        if macro_value.count("\"") == 0 and macro_value.count("'") == 0 and macro_value.count('{') == 0:
            if macro_value[0].isdigit():
                symbol = ""
            else:
                for i in range(0, len(macro_value)):
                    if macro_value[i].isdigit() or macro_value[i] == '.':
                        break
                plus_count = macro_value[:i].count('+')
                minus_count = macro_value[:i].count('-')
                macro_value = macro_value[i:]

                if minus_count % 2 == 0:
                    symbol = ""
                else:
                    symbol = "-"
            if macro_value.count('.') == 0:
                if macro_value.count('e') != 0:
                    return float(symbol + macro_value)
                elif macro_value.endswith('f') or macro_value.endswith('L'):
                    return float(symbol + macro_value[:-1])
                else:
                    return None
            else:
                try:
                    value_data = float(symbol + macro_value)
                    return value_data
                except:
                    return float(symbol + macro_value[:len(macro_value) - 1])

    except:
        return None



# �ж��ǲ��ǲ�������
def is_bool_constant(macro_value):
    if macro_value == "true":
        return True
    elif macro_value == "false":
        return False
    else:
        return None


# Ϊcharacter�б����ṩת�����񣬱����ǿ��Ժ�deal_string_python��������
def converse_from_character_to_python_character(macro_value):
    # value 'abc'ȥ���������ŵĲ���
    macro_str = ""
    i = 0
    while i in range(0, len(macro_value)):
        if macro_value[i] == '\\':
            if macro_value[i + 1] == 't':
                macro_str += '\t'
                i += 2
            elif macro_value[i + 1] == 'a':
                macro_str += '\a'
                i += 2
            elif macro_value[i + 1] == 'b':
                macro_str += "\b"
                i += 2
            elif macro_value[i + 1] == 'f':
                macro_str += '\f'
                i += 2
            elif macro_value[i + 1] == 'n':
                macro_str += '\n'
                i += 2
            elif macro_value[i + 1] == 'r':
                macro_str += '\r'
                i += 2
            elif macro_value[i + 1] == 'v':
                macro_str += '\v'
                i += 2
            elif macro_value[i + 1] == "'":
                macro_str += "'"
                i += 2
            elif macro_value[i + 1] == '\\':
                macro_str += '\\'
                i += 2
            elif macro_value[i + 1] == '"':
                macro_str += '\"'
                i += 2
            elif macro_value[i + 1] == '?':
                macro_str += '\?'
                i += 2
            elif macro_value[i + 1] == 'x':
                end = find_sixteen_end(macro_value[i + 2:])
                macro_str += chr(int(macro_value[i + 2:i + 2 + end], 16))
                i = i + 2 + end
            elif macro_value[i + 1].isdigit() and find_eight_end(
                    macro_value[i + 1:]) > 0:
                end = find_eight_end(macro_value[i + 1:])
                macro_str += chr(int(macro_value[i + 1:i + 1 + end], 8))
                i = i + 1 + end
            else:
                macro_str += macro_value[i + 1]
                i += 2
        else:
            macro_str += macro_value[i]
            i += 1
    # print macro_value, macro_str, len(macro_str)
    return macro_str


# �ж��ǲ����ַ�����
def is_character_constant(macro_value):
    try:
        if macro_value.startswith("'") and macro_value.endswith("'"):
            actuall_value = converse_from_character_to_python_character(macro_value)[1:-1]
            if len(actuall_value) == 1:
                return ord(actuall_value)
            elif len(actuall_value) >1 :
                i = 0
                count = 0
                return_value = 0
                while i < len(macro_value):
                    return_value += pow(64, count) * ord(macro_value[i])
                    count += 1
                    i += 1
                return return_value
    except BaseException as e:
        print e
        return None


def deal_string_to_python(macro_value):
    macro_str = ""
    i = 0
    quotes_pos = []
    count = 0
    while i < len(macro_value):
        if macro_value[i] == '\\':
            if macro_value[i + 1] == 't':
                macro_str += '\t'
                i += 2
                count += 1
            elif macro_value[i + 1] == 'a':
                macro_str += '\a'
                i += 2
                count += 1
            elif macro_value[i + 1] == 'b':
                macro_str += "\b"
                i += 2
                count += 1
            elif macro_value[i + 1] == 'f':
                macro_str += '\f'
                i += 2
                count += 1
            elif macro_value[i + 1] == 'n':
                macro_str += '\n'
                i += 2
                count += 1
            elif macro_value[i + 1] == 'r':
                macro_str += '\r'
                i += 2
                count += 1
            elif macro_value[i + 1] == 'v':
                macro_str += '\v'
                i += 2
                count += 1
            elif macro_value[i + 1] == "'":
                macro_str += "'"
                i += 2
                count += 1
            elif macro_value[i + 1] == '\\':
                macro_str += '\\'
                i += 2
                count += 1
            elif macro_value[i + 1] == '"':
                macro_str += '\"'
                i += 2
                count += 1
            elif macro_value[i + 1] == '?':
                macro_str += '\?'
                i += 2
                count += 1
            elif macro_value[i + 1] == 'x':
                end = find_sixteen_end(macro_value[i + 2:])
                macro_str += chr(int(macro_value[i + 2:i + 2 + end], 16))
                i = i + 2 + end
                count = count + 1 + end
            elif macro_value[i + 1].isdigit() and find_eight_end(
                    macro_value[i + 1:]) > 0:
                end = find_eight_end(macro_value[i + 1:])
                macro_str += chr(int(macro_value[i + 1:i + 1 + end], 8))
                i = i + 1 + end
                count = count + end
            else:
                macro_str += macro_value[i + 1]
                count += 1
                i += 2
        elif macro_value[i] == '"':
            quotes_pos.append(i - count)
            macro_str += macro_value[i]
            i += 1
        else:
            macro_str += macro_value[i]
            i += 1
    return macro_str, quotes_pos


# �ж��ǲ����ַ���
def is_string_constant(macro_value):
    try:
        if macro_value.startswith('"') and macro_value.endswith('"'):
            macro_str, quotes_pos = deal_string_to_python(macro_value)
            return connect_split_alpha(macro_str, quotes_pos)
        elif macro_value.startswith('L') and macro_value.endswith('"'):
            macro_str, quotes_pos = deal_string_to_python(macro_value[1:])
            return connect_split_alpha(macro_str, quotes_pos).decode()

    except BaseException as e:
        print "error value:  " + macro_value, e
        return None


# "ABC""DEF"��������
# "abc\\" "def\\"
# define data3 "this is \" a data " "helo \""
def connect_split_alpha(macro_value, quotes_pos):
    double_quotes_value = macro_value.count('"')
    if double_quotes_value == 2 or double_quotes_value == 3 or len(quotes_pos) == 2:
        return macro_value[1:-1]
    # if len(quotes_pos) == 4:
    i = 0
    new_macro_value = ""
    while i < len(quotes_pos):
        new_macro_value += macro_value[quotes_pos[i] + 1:quotes_pos[i + 1]]
        i += 2
    return new_macro_value
    # else:
    #     return macro_value


# �ҵ�ת���8���Ƶ�ĩβ
def find_eight_end(value):
    for i in range(0, len(value)):
        if not value[i].isdigit():
            return i
        elif int(value[i]) >= 8:
            return i
    return len(value)


# �ҵ�ת��16���Ƶ�ĩβ
def find_sixteen_end(value):
    for i in range(0, len(value)):
        if value[i].isalpha():
            if value[i].lower() not in 'abcdef':
                return i
        elif not value[i].isdigit():
            return i
    return len(value) - 1


# �ж��ǲ��Ǿۺ�
def is_union_constant(macro_value):
    # �����Ƕ��ھۺ������������ν��н���
    try:
        value_list = []
        if macro_value.startswith('{'):
            i = 1
            while i < len(macro_value) - 1:
                if macro_value[i] != " " and macro_value[i] != ",":
                    boundary = find_boundary_in_union(macro_value[i:-1])
                    value_list.append(
                        choose_type(macro_value[i:i + boundary + 1]))
                    i = i + boundary + 1
                else:
                    i += 1
            return tuple(value_list)
    except BaseException as e:
        print e
        return None


def find_double_quotes_end_in_unoin(value):
    double_quotes_pos = [0]
    for i in range(1, len(value)):
        if value[i] == '"':
            flag = 0
            if value[i - 1] != '\\':
                flag = 1
            else:
                j = i - 1
                while j > 0:
                    if value[j] != '\\':
                        break
                    j -= 1
                if (i - j + 1) % 2 == 0:
                    flag = 1
            if flag == 1:
                double_quotes_pos.append(i)
    if len(double_quotes_pos) > 2:
        i = 1
        while i < len(double_quotes_pos) - 1:
            if ',' not in value[double_quotes_pos[i]:double_quotes_pos[i + 1]]:
                i += 2
            else:
                return double_quotes_pos[i] - double_quotes_pos[0]
        return double_quotes_pos[i] - double_quotes_pos[0]
    else:
        return double_quotes_pos[1] - double_quotes_pos[0]
        #     if ',' not in value[double_quotes_pos[1]:double_quotes_pos[2]]:
        #         return double_quotes_pos[3] - double_quotes_pos[0]
        #     else:
        #         return double_quotes_pos[1] - double_quotes_pos[0]
        # else:
        #     return double_quotes_pos[1] - double_quotes_pos[0]


def find_single_quotes_end_in_unoin(value):
    single_quotes_pos = [0]
    for i in range(1, len(value)):
        if value[i] == "'":
            flag = 0
            if value[i - 1] != '\\':
                flag = 1
            else:
                j = i - 1
                while j > 0:
                    if value[j] != '\\':
                        break
                    j -= 1
                if (i - j + 1) % 2 == 0:
                    flag = 1
            if flag == 1:
                single_quotes_pos.append(i)
    if single_quotes_pos:
        return single_quotes_pos[1] - single_quotes_pos[0]


# �ҵ�union�и���Ԫ�صı߽�
def find_boundary_in_union(value):
    if value.startswith('"'):
        # if value[i] == '"' and value[i - 1] != '\\':
        #     if value[i+1:].strip()[0] == ',':
        #         return i
        return find_double_quotes_end_in_unoin(value)
    elif value.startswith('L'):
        index = value.find('"')
        return index + find_double_quotes_end_in_unoin(value[index:])
    elif value.startswith("'"):
        # for i in range(1, len(value)):
        #     if value[i] == "'" and value[i - 1] != '\\':
        #         return i
        return find_single_quotes_end_in_unoin(value)
    elif value.startswith("L\""):
        # for i in range(2, len(value)):
        #     if value[i] == '"' and value[i - 1] != '\\':
        #         return i
        return find_double_quotes_end_in_unoin(value) + 2
    elif value.startswith('{'):
        # Ѱ�������������Ŷ�Ӧ���Ҵ����ţ�ȷ������
        # return find_right_big_parantheses(value)
        return find_right_big_parantheses_new(value)
    elif value[:5] == 'false':
        return 5
    elif value[:4] == 'true':
        return 4
    # elif value[0].isdigit():
    else:
        if value.find(',') == -1:
            return len(value) - 1
        else:
            return value.find(',') - 1


# Ѱ�������������Ŷ�Ӧ���Ҵ����ţ�ȷ������, value[0]='{'
def find_right_big_parantheses_new(value):
    i = 1
    symbol_list = ['{']
    while i < len(value):
        if value[i] == '"':
            i = i + find_double_quotes_end_in_unoin(value[i:]) + 1
        elif value[i] == "'":
            i = i + find_single_quotes_end_in_unoin(value[i:]) + 1
        elif value[i] == '{':
            symbol_list.append(value[i])
            i += 1
        elif value[i] == '}':
            symbol_list.pop()
            if not symbol_list:
                return i
            else:
                i += 1
        else:
            # i = i + value[i:].find(',') + 1
            i += 1


# �ݹ鴦������
def recursive_extract(codes, variable_defined):
    # variable_defined = {}
    i = 0
    while i < len(codes):
        code = codes[i].strip()
        order, variable, variable_value = split_code(code)
        if order == "#define":
            if variable:
                variable_defined[variable] = variable_value
            i += 1
        elif order == "#undef":
            if variable in variable_defined.keys():
                variable_defined.pop(variable)
            i += 1
        elif order == "#ifndef":
            else_pos = find_else(order, codes[i:])
            end_pos = find_endif(order, codes[i:])
            if not variable in variable_defined.keys():
                if else_pos != None:
                    recursive_extract(codes[i + 1:i + else_pos],
                                      variable_defined)
                else:
                    recursive_extract(codes[i + 1:i + end_pos],
                                      variable_defined)
            elif variable in variable_defined.keys():
                if else_pos != None:
                    recursive_extract(codes[i + else_pos:i + end_pos],
                                      variable_defined)
                    # else:
                    #     recursive_extract(codes[i + 1:i + end_pos],
                    #                       variable_defined)
            i += end_pos
        elif order == "#ifdef":
            else_pos = find_else(order, codes[i:])
            end_pos = find_endif(order, codes[i:])
            if variable in variable_defined.keys():
                if else_pos != None:
                    recursive_extract(codes[i + 1:i + else_pos],
                                      variable_defined)
                else:
                    recursive_extract(codes[i + 1:i + end_pos],
                                      variable_defined)
            elif not variable in variable_defined.keys():
                if else_pos != None:
                    recursive_extract(codes[i + else_pos:i + end_pos],
                                      variable_defined)
                    # else:
                    #     recursive_extract(codes[i + 1:i + end_pos],
                    #                       variable_defined)
            i += end_pos
        elif order == "#endif" or order == "#else":
            i += 1
        else:
            i += 1
    return variable_defined


# �ҵ���order_if��Ե�#else, order_if������#ifdefҲ������#ifndef
# ���ص���#else��codes�е�λ�ã�û���򷵻�None
def find_else(order_if, codes):
    i = 1
    end_pos = find_endif(order_if, codes)
    while i < len(codes[:end_pos]):
        code = codes[i]
        order, variable, variable_value = split_code(code)
        if order == "#ifdef" or order == "#ifndef":
            i += find_endif(order, codes[i:end_pos])
            continue
        elif order == "#else":
            return i
        i += 1
    return None


# �ҵ���order_if��Ե�#endif, order_if������#ifdefҲ������#ifndef
# ���ص���#endif��codes�е�λ�ã�û���򷵻�None
def find_endif(order_if, codes):
    order_list = []
    order_list.append(order_if)
    i = 1
    while i < len(codes):
        code = codes[i]
        order, variable, variable_value = split_code(code)
        if order == "#ifdef" or order == "#ifndef":
            order_list.append(order)
        elif order == "#endif":
            if len(order_list) == 1:
                return i
            else:
                order_list.pop()
        i += 1
    return None


# ��һ�д����Ϊָ�����������ֵ������
def split_code(code):
    code = code.strip()[1:].strip()
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


# �ӳ�ʼ��C++������ȥ��ע�ͣ�����stringΪȥ��ע�͵�c++����
def remove_comments(code_with_comments):
    code_length = len(code_with_comments)
    index = 0
    state = 0
    code_without_comments = ""
    while index < code_length:
        c = code_with_comments[index]
        if state == 0:
            if c == '/':
                state = 1
            elif c == "'":
                state = 6
            elif c == '"':
                state = 8
            else:
                code_without_comments += c
        elif state == 1:
            if c == '*':
                state = 2
            elif c == '/':
                state = 4
            else:
                code_without_comments = code_without_comments + '/' + c
                state = 0
        elif state == 2:
            if c == '*':
                state = 3
            else:
                state = 2
        elif state == 3:
            if c == '/':
                state = 0
                code_without_comments += " "
            elif c == '*':
                state = 3
            else:
                state = 2
        elif state == 4:
            if c == "\\":
                state = 5
            elif c == '\n':
                state = 0
                code_without_comments += c
        elif state == 5:
            if c == '\\':
                state = 5
            else:
                state = 4
        elif state == 6:
            if c == '\\':
                state = 7
            elif c == "'":
                state = 0
                code_without_comments += c
        elif state == 7:
            state = 6
        elif state == 8:
            if c == '\\':
                state = 9
            elif c == '"':
                state = 0
                code_without_comments += c
        elif state == 9:
            state = 8
        if state == 6 or state == 7 or state == 8 or state == 9:
            code_without_comments += c
        index += 1
    return code_without_comments


def main():
    a = PyMacroParser()
    # a.load("srctest-1.cpp")
    a.load("test_2.cpp")
    print a.dumpDict()
    # a.load("a.cpp")
    a.dump('a_test_b.cpp')
    b = PyMacroParser()
    b.load('a_test_b.cpp')
    print b.dumpDict()



if __name__ == '__main__':
    main()
