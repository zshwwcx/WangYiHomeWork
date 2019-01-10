
#define strdef_1 "#define a 123"
#define strdef_2 "\\t"
#define  /*
*/strdef_3 "aaa"
#undef /*
*/ strdef_2
#define strdef_4 "\"\"\""

#/*
*/ define data100 1000


/*asdas
*/
	#define
#/***/define /***/define6 /* \t\v\b\n*/"123" /*\t\v\b\n*/ "345"

#define   polyTest_1   {"\x66\\',,\"\x64 \",,\n\r,,,,\t\x67,,,\x68\\\\"}
#define   polyTest_2      { {2.0, "ab\tc"},"{,,,,,,{{	}}}''''",{1.5,L	"\nde\'\"f\t\\"},		12,12,	{5.6f, "7.2"},{2222,false,{"d"   },/**45455*/{'d'  }  }  } 
#define polyTest_3 {"\\\\\\\\////////"}
#undef Ghost

#define emputyStr_1 ""
#define emputyStr_2 ''
#define emputyStr_3 "{{}"
#define space_1 "          "  //finished
#define  space_2  
#define space_3 	"	"  //Ã‚ƒø÷–√ª”–Ã·µΩ£¨’‚∏ˆ”¶∏√»Á∫Œ¥¶¿Ì°£‘› ±»œŒ™√ª”–Œ Ã‚
#define multyDef
#ifdef multyDef/*
*/#define mua
#endif
/*a*/
#define a
#define NormLnumber	123

#define ReDefine 12
#define ReDefine 21

/*//*/

/*/,//*,/*//*/*///*////asdf

/*/
xxxx
//*/

//*/
#define Notes //*/
//*/

///*/
//**/
///*
///
/*
//a
*/

#define Number_01 0x77
#define Number_02 -0x77
#define Number_03 0b10
#define Number_04 -0b10
#define Number_05 0o77
#define Number_06 -0o77
#define Number_07 77
#define Number_08 -77


#define Number_11 0x77e0
#define Number_12 -0x77e0
#define Number_17 77e0
#define Number_18 -77e0


#	define     Number_21     0x77e2   
#define Number_22 -0x77e2
#define Number_27 77e2
#define Number_28 -77e2

#define LongNum_1 1234567l
#define LongNum_2 1234567L


#define smallNum .123

#define K1-1 {{{}}}
#define K1-2 {{{},{}}}
#define K1-3 {}
#define K3 -0x20

#define K_123

#define Alpha_1 "\x41\102\103DEFG"  "HI\JKLMNO\PQ\RSTUVW\X\Z\bYZ\b\012"
#define Alpha_2 "asdf///*aaa*/"
#define Alpha_3 0
#define Alpha_4 "with tab \ta"
#define Alpha_5 "with tab 	a"

#define K4 -2.5f

#    ifndef MCTEST
#define MCTEST
                             
#ifdef MC1    

#define data1 0x20
/*cmment start*/#define /*this is comment*/ data2 2.5f
#define date3 L"this is a data"
#define data4 true
/*qqq
//*/

#ifdef MC2

#define data5 'a'
#define data6 { {2.0, "abc"}, {1.5, "def"}, {5.6f, "7.2"}} // ∏°µ„”Î◊÷∑˚¥Æ◊È≥…µƒΩ·ππÃÂ≥ı ºªØæ€∫œ£¨ ‘ŸΩ¯“ª≤Ωæ€∫œ◊È≥…¡À ˝◊È

#else //else MC2

# define data5 {5.0, 7.5, 3.8}
#define data6 'c'
#endif //end MC2

#ifdef MC3
	//#endif
#endif //end MC3

#else//else MC1

#define data1 1.0f /* this is float
may be changed
*/
#define data2 2
#define date3 false
#define data4 "this is a data"


#ifdef MC2

#define data5 'B'
#define data6 {1, 6, 3}
#define data7 0xa

#else//else MC2


#define data5 'D'
#define data6 {1, 6}

#endif //end MC2

#endif //MC1

#ifdef MC2
#undef MC2
#endif

/*‘⁄∂‡––◊¢ Õ∫Û√ÊΩÙ∏˙“ª∏ˆµ•––◊¢ Õ*///ΩÙ∏˙µƒµ•––◊¢ Õ

#endif // !MC_TEST

#define MC_TEST
