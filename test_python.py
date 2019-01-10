# coding=utf-8

import  time


# 判读是不是聚合
def main():
    # print 'int: '
    # print choose_type("04444000000000000004uI64")
    # print choose_type("04444000000000000004")
    # print choose_type("0x8A40000000000010uLL")
    # print choose_type("900000000001ull")
    # print choose_type("0x0")
    # print 'i am request,\xE6\x88\x91\xE6\x98\xAF\xE8\xAF\xB7\xE6\xB1\x82'.decode(
    #     'utf-8').encode('utf-8')
    # print 'float: '
    # print choose_type('-1f')
    # print choose_type('2e-1')
    # print choose_type('2e3')
    # print choose_type('15.75')
    # print choose_type('.3f')
    # print choose_type('0.0f')
    # print choose_type('1.f')

    # print 'character: '
    # print choose_type("'A'")
    # print choose_type("\"A\"")

    # print 'bool:'
    # print choose_type('true')
    # print choose_type('false')
    # print choose_type("\'true\'")
    # print choose_type("'false'")
    # print is_bool_constant('true')

    # print "string:"
    # print choose_type("L\"\x66\"")
    # print choose_type("\"{'hello'}\"")

    # print "union: "
    # # print choose_type("{}")
    # # ((2.0, "abc"), (1.5, "def"), (5.6, "7.2"))
    # union_str = '{ {2.0, "abc\""}, {1.5, "def"}, {5.6f, "7.2"}, 5.0, 7.5, 3.8, {"{\""}, }'

    # string_str = '"\\a\\\\\',,\\"\\x64 \\",,\\n\\r,,,,\\t\\x67,,,\\x68\\\\\\\\")'
    #
    # print string_str.decode('string-escape')
    # print is_string_constant('L"hello" L"world"')
    # print is_string_constant('"hello" "world"')
    #
    # string_str_2 = 'u"\"helloworld"'
    # print is_string_constant(string_str_2)
    # print string_str_2.decode('string-escape')
    # print string_str

    # with open('test_2.cpp') as f:
    #     contents = f.readlines()
    # content = contents[0]
    # for i in content:
    #     print i

    pass


            # print choose_type(union_str)
    # for item in union_str:
    #     if item == '"':
    #         print item


    

if __name__ == '__main__':
    main()



def test_union():
    # 测试聚合部分
    print "test union:"

    # print find_boundary_in_union('"hello",')
    # print find_boundary_in_union("'\x43'")
    # print find_boundary_in_union('L"hello world"')
    # print find_boundary_in_union('{"{}",\'}\',\'{\'}')
    # print find_boundary_in_union("false")
    # print find_boundary_in_union("true")
    #
    # print is_union_constant('{L"hello world"}')
    # print '{ " "  ,{"}",\'}\', "hello"},  "helloworld", {"cxy"}}'
    # print "union:"
    # print is_union_constant(
    #     '{"",{"}",\'}\', "hello"}, "helloworld", {"cxy\"}}')
    # print is_union_constant('{{"2f", 3f}}')
    # print is_union_constant('{2f, 2.3, 2e1, {20, "hellow"}}')
    # print is_union_constant('{,}')
    #

# def test_number():
#     print 'int: '
#     print choose_type("0xf4")
#     print choose_type("-2u")
#     print choose_type("+-+2u")
#     print choose_type("2")
#     print choose_type("-+-2u")
#     print choose_type('0x2a')
#     print choose_type('01')
#     print choose_type("04444000000000000004uI64")
#     print choose_type("04444000000000000004")
#     print choose_type("0x8A40000000000010uLL")
#     print choose_type("900000000001ull")
#     print choose_type("0")
#     print choose_type("00")
#     print choose_type("0x0")
#     print 'i am request,\xE6\x88\x91\xE6\x98\xAF\xE8\xAF\xB7\xE6\xB1\x82'.decode(
#         'utf-8').encode('utf-8')
#     print 'float: '
#     print choose_type('-1f')
#     print choose_type('+-1f')
#     print choose_type('2e-1')
#     print choose_type('2e3')
#     print choose_type('15.75')
#     print choose_type('.3f')
#     print choose_type('0.0f')
#     print choose_type('1.f')


# def test_character():
#     print "test character: "
#     print is_character_constant("'\12'")
#     print is_character_constant("'\x12'")
#     print is_character_constant("'012'")
#     print is_character_constant("'0x12'")
#     print is_character_constant("'\t'")
#     print is_character_constant("'abc'")
#     print is_character_constant("'a'")
#     print is_character_constant("'\xab'")
#     print is_character_constant("'\t\n'")
