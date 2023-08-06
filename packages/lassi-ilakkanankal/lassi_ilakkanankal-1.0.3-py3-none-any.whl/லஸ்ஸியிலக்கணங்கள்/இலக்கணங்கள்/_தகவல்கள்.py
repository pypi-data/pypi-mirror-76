தகவல்கள்="""{
  "python": {
    "நீட்சி": {
      "த": "பை"
    },
    "பெயர்": {
      "த": "பைத்தான்"
    },
    "பதிப்புகள்": {
      "2.0.0": [
        "single_input : _NEWLINE | simple_stmt | compound_stmt _NEWLINE",
        "?file_input : ( _NEWLINE | stmt ) *",
        "eval_input : testlist _NEWLINE ?",
        "decorator : \\"@\\" dotted_name [ \\"(\\" [ arglist ] \\")\\" ] _NEWLINE",
        "decorators : decorator +",
        "decorated : decorators ( classdef | funcdef )",
        "funcdef : \\"def\\" NAME \\"(\\" parameters \\")\\" \\":\\" suite",
        "parameters : [ paramlist ]",
        "paramlist : param ( \\",\\" param ) * [ \\",\\" [ star_params [ \\",\\" kw_params ] | kw_params ] ] \\n           | star_params [ \\",\\" kw_params ] \\n           | kw_params",
        "star_params : \\"*\\" NAME",
        "kw_params : \\"**\\" NAME",
        "param : fpdef [ \\"=\\" test ]",
        "fpdef : NAME | \\"(\\" fplist \\")\\"",
        "fplist : fpdef ( \\",\\" fpdef ) * [ \\",\\" ]",
        "?stmt : simple_stmt | compound_stmt",
        "?simple_stmt : small_stmt ( \\";\\" small_stmt ) * [ \\";\\" ] _NEWLINE",
        "?small_stmt : ( expr_stmt | print_stmt | del_stmt | pass_stmt | flow_stmt \\n          | import_stmt | global_stmt | exec_stmt | assert_stmt )",
        "expr_stmt : testlist augassign ( yield_expr | testlist ) -> augassign2 \\n         | testlist ( \\"=\\" ( yield_expr | testlist ) ) + -> assign \\n         | testlist",
        "augassign : ( \\"+=\\" | \\"-=\\" | \\"*=\\" | \\"/=\\" | \\"%=\\" | \\"&=\\" | \\"|=\\" | \\"^=\\" | \\"<<=\\" | \\">>=\\" | \\"**=\\" | \\"//=\\" )",
        "print_stmt : \\"print\\" ( [ test ( \\",\\" test ) * [ \\",\\" ] ] | \\">>\\" test [ ( \\",\\" test ) + [ \\",\\" ] ] )",
        "del_stmt : \\"del\\" exprlist",
        "pass_stmt : \\"pass\\"",
        "?flow_stmt : break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt",
        "break_stmt : \\"break\\"",
        "continue_stmt : \\"continue\\"",
        "return_stmt : \\"return\\" [ testlist ]",
        "yield_stmt : yield_expr",
        "raise_stmt : \\"raise\\" [ test [ \\",\\" test [ \\",\\" test ] ] ]",
        "import_stmt : import_name | import_from",
        "import_name : \\"import\\" dotted_as_names",
        "import_from : \\"from\\" ( \\".\\" * dotted_name | \\".\\" + ) \\"import\\" ( \\"*\\" | \\"(\\" import_as_names \\")\\" | import_as_names )",
        "?import_as_name : NAME [ \\"as\\" NAME ]",
        "?dotted_as_name : dotted_name [ \\"as\\" NAME ]",
        "import_as_names : import_as_name ( \\",\\" import_as_name ) * [ \\",\\" ]",
        "dotted_as_names : dotted_as_name ( \\",\\" dotted_as_name ) *",
        "dotted_name : NAME ( \\".\\" NAME ) *",
        "global_stmt : \\"global\\" NAME ( \\",\\" NAME ) *",
        "exec_stmt : \\"exec\\" expr [ \\"in\\" test [ \\",\\" test ] ]",
        "assert_stmt : \\"assert\\" test [ \\",\\" test ]",
        "?compound_stmt : if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated",
        "if_stmt : \\"if\\" test \\":\\" suite ( \\"elif\\" test \\":\\" suite ) * [ \\"else\\" \\":\\" suite ]",
        "while_stmt : \\"while\\" test \\":\\" suite [ \\"else\\" \\":\\" suite ]",
        "for_stmt : \\"for\\" exprlist \\"in\\" testlist \\":\\" suite [ \\"else\\" \\":\\" suite ]",
        "try_stmt : ( \\"try\\" \\":\\" suite ( ( except_clause \\":\\" suite ) + [ \\"else\\" \\":\\" suite ] [ \\"finally\\" \\":\\" suite ] | \\"finally\\" \\":\\" suite ) )",
        "with_stmt : \\"with\\" with_item ( \\",\\" with_item ) * \\":\\" suite",
        "with_item : test [ \\"as\\" expr ]",
        "except_clause : \\"except\\" [ test [ ( \\"as\\" | \\",\\" ) test ] ]",
        "suite : simple_stmt | _NEWLINE _INDENT _NEWLINE ? stmt + _DEDENT _NEWLINE ?",
        "testlist_safe : old_test [ ( \\",\\" old_test ) + [ \\",\\" ] ]",
        "old_test : or_test | old_lambdef",
        "old_lambdef : \\"lambda\\" [ paramlist ] \\":\\" old_test",
        "?test : or_test [ \\"if\\" or_test \\"else\\" test ] | lambdef",
        "?or_test : and_test ( \\"or\\" and_test ) *",
        "?and_test : not_test ( \\"and\\" not_test ) *",
        "?not_test : \\"not\\" not_test | comparison",
        "?comparison : expr ( comp_op expr ) *",
        "comp_op : \\"<\\" | \\">\\" | \\"==\\" | \\">=\\" | \\"<=\\" | \\"<>\\" | \\"!=\\" | \\"in\\" | \\"not\\" \\"in\\" | \\"is\\" | \\"is\\" \\"not\\"",
        "?expr : xor_expr ( \\"|\\" xor_expr ) *",
        "?xor_expr : and_expr ( \\"^\\" and_expr ) *",
        "?and_expr : shift_expr ( \\"&\\" shift_expr ) *",
        "?shift_expr : arith_expr ( ( \\"<<\\" | \\">>\\" ) arith_expr ) *",
        "?arith_expr : term ( ( \\"+\\" | \\"-\\" ) term ) *",
        "?term : factor ( ( \\"*\\" | \\"/\\" | \\"%\\" | \\"//\\" ) factor ) *",
        "?factor : ( \\"+\\" | \\"-\\" | \\"~\\" ) factor | power",
        "?power : molecule [ \\"**\\" factor ]",
        "?molecule : molecule \\"(\\" [ arglist ] \\")\\" -> func_call \\n         | molecule \\"[\\" [ subscriptlist ] \\"]\\" -> getitem \\n         | molecule \\".\\" NAME -> getattr \\n         | atom",
        "?atom : \\"(\\" [ yield_expr | testlist_comp ] \\")\\" -> tuple \\n    | \\"[\\" [ listmaker ] \\"]\\" \\n    | \\"{\\" [ dictorsetmaker ] \\"}\\" \\n    | \\"`\\" testlist1 \\"`\\" \\n    | \\"(\\" test \\")\\" \\n    | NAME | number | string +",
        "listmaker : test ( list_for | ( \\",\\" test ) * [ \\",\\" ] )",
        "?testlist_comp : test ( comp_for | ( \\",\\" test ) + [ \\",\\" ] | \\",\\" )",
        "lambdef : \\"lambda\\" [ paramlist ] \\":\\" test",
        "?subscriptlist : subscript ( \\",\\" subscript ) * [ \\",\\" ]",
        "subscript : \\".\\" \\".\\" \\".\\" | test | [ test ] \\":\\" [ test ] [ sliceop ]",
        "sliceop : \\":\\" [ test ]",
        "?exprlist : expr ( \\",\\" expr ) * [ \\",\\" ]",
        "?testlist : test ( \\",\\" test ) * [ \\",\\" ]",
        "dictorsetmaker : ( ( test \\":\\" test ( comp_for | ( \\",\\" test \\":\\" test ) * [ \\",\\" ] ) ) | ( test ( comp_for | ( \\",\\" test ) * [ \\",\\" ] ) ) )",
        "classdef : \\"class\\" NAME [ \\"(\\" [ testlist ] \\")\\" ] \\":\\" suite",
        "arglist : ( argument \\",\\" ) * ( argument [ \\",\\" ] \\n                         | star_args [ \\",\\" kw_args ] \\n                         | kw_args )",
        "star_args : \\"*\\" test",
        "kw_args : \\"**\\" test",
        "argument : test [ comp_for ] | test \\"=\\" test",
        "list_iter : list_for | list_if",
        "list_for : \\"for\\" exprlist \\"in\\" testlist_safe [ list_iter ]",
        "list_if : \\"if\\" old_test [ list_iter ]",
        "comp_iter : comp_for | comp_if",
        "comp_for : \\"for\\" exprlist \\"in\\" or_test [ comp_iter ]",
        "comp_if : \\"if\\" old_test [ comp_iter ]",
        "testlist1 : test ( \\",\\" test ) *",
        "yield_expr : \\"yield\\" [ testlist ]",
        "number : DEC_NUMBER | HEX_NUMBER | OCT_NUMBER | FLOAT | IMAG_NUMBER",
        "string : STRING | LONG_STRING",
        "COMMENT : /#[^\\\\n]*/",
        "_NEWLINE : ( /\\\\r?\\\\n[\\\\t ]*/ | COMMENT ) +",
        "STRING : /[ubf]?r?(\\"(?!\\"\\").*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?\\"|'(?!'').*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?')/i",
        "LONG_STRING . 2 : /[ubf]?r?(\\"\\"\\".*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?\\"\\"\\"|'''.*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?''')/is",
        "HEX_NUMBER : /0x[\\\\da-f]*l?/i",
        "OCT_NUMBER : /0o?[0-7]*l?/i",
        "%import common . FLOAT -> FLOAT",
        "%import common . INT -> _INT",
        "%import common . CNAME -> NAME",
        "IMAG_NUMBER : ( _INT | FLOAT ) ( \\"j\\" | \\"J\\" )",
        "%ignore /[\\\\t \\\\f]+/",
        "%ignore /\\\\\\\\[\\\\t \\\\f]*\\\\r?\\\\n/",
        "%ignore COMMENT",
        "%declare _INDENT _DEDENT"
      ],
      "3.0.0": [
        "single_input : NEWLINE | simple_stmt | compound_stmt NEWLINE",
        "file_input : ( NEWLINE | stmt ) *",
        "eval_input : testlist NEWLINE *",
        "!decorator : \\"@\\" dotted_name [ \\"(\\" [ arguments ] \\")\\" ] NEWLINE",
        "decorators : decorator +",
        "decorated : decorators ( classdef | funcdef | async_funcdef )",
        "async_funcdef : \\"async\\" funcdef",
        "funcdef : \\"def\\" NAME \\"(\\" parameters ? \\")\\" [ \\"->\\" test ] \\":\\" suite",
        "!parameters : paramvalue ( \\",\\" paramvalue ) * [ \\",\\" [ starparams | kwparams ] ] \\n          | starparams \\n          | kwparams",
        "starparams : \\"*\\" typedparam ? ( \\",\\" paramvalue ) * [ \\",\\" kwparams ]",
        "kwparams : \\"**\\" typedparam",
        "?paramvalue : typedparam [ \\"=\\" test ]",
        "?typedparam : NAME [ \\":\\" test ]",
        "!varargslist : ( vfpdef [ \\"=\\" test ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"*\\" [ vfpdef ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"**\\" vfpdef [ \\",\\" ] ] ] | \\"**\\" vfpdef [ \\",\\" ] ] ] \\n  | \\"*\\" [ vfpdef ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"**\\" vfpdef [ \\",\\" ] ] ] \\n  | \\"**\\" vfpdef [ \\",\\" ] )",
        "vfpdef : NAME",
        "?stmt : simple_stmt | compound_stmt",
        "!?simple_stmt : small_stmt ( \\";\\" small_stmt ) * [ \\";\\" ] NEWLINE",
        "?small_stmt : ( expr_stmt | del_stmt | pass_stmt | flow_stmt | import_stmt | global_stmt | nonlocal_stmt | assert_stmt )",
        "?expr_stmt : testlist_star_expr ( annassign | augassign ( yield_expr | testlist ) \\n         | ( \\"=\\" ( yield_expr | testlist_star_expr ) ) * )",
        "annassign : \\":\\" test [ \\"=\\" test ]",
        "!?testlist_star_expr : ( test | star_expr ) ( \\",\\" ( test | star_expr ) ) * [ \\",\\" ]",
        "!augassign : ( \\"+=\\" | \\"-=\\" | \\"*=\\" | \\"@=\\" | \\"/=\\" | \\"%=\\" | \\"&=\\" | \\"|=\\" | \\"^=\\" | \\"<<=\\" | \\">>=\\" | \\"**=\\" | \\"//=\\" )",
        "del_stmt : \\"del\\" exprlist",
        "pass_stmt : \\"pass\\"",
        "flow_stmt : break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt",
        "break_stmt : \\"break\\"",
        "continue_stmt : \\"continue\\"",
        "return_stmt : \\"return\\" [ testlist ]",
        "yield_stmt : yield_expr",
        "raise_stmt : \\"raise\\" [ test [ \\"from\\" test ] ]",
        "import_stmt : import_name | import_from",
        "import_name : \\"import\\" dotted_as_names",
        "import_from : \\"from\\" ( dots ? dotted_name | dots ) \\"import\\" ( \\"*\\" | \\"(\\" import_as_names \\")\\" | import_as_names )",
        "!dots : \\".\\" +",
        "import_as_name : NAME [ \\"as\\" NAME ]",
        "dotted_as_name : dotted_name [ \\"as\\" NAME ]",
        "!import_as_names : import_as_name ( \\",\\" import_as_name ) * [ \\",\\" ]",
        "dotted_as_names : dotted_as_name ( \\",\\" dotted_as_name ) *",
        "dotted_name : NAME ( \\".\\" NAME ) *",
        "global_stmt : \\"global\\" NAME ( \\",\\" NAME ) *",
        "nonlocal_stmt : \\"nonlocal\\" NAME ( \\",\\" NAME ) *",
        "assert_stmt : \\"assert\\" test [ \\",\\" test ]",
        "compound_stmt : if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated | async_stmt",
        "async_stmt : \\"async\\" ( funcdef | with_stmt | for_stmt )",
        "if_stmt : \\"if\\" test \\":\\" suite ( \\"elif\\" test \\":\\" suite ) * [ \\"else\\" \\":\\" suite ]",
        "while_stmt : \\"while\\" test \\":\\" suite [ \\"else\\" \\":\\" suite ]",
        "for_stmt : \\"for\\" exprlist \\"in\\" testlist \\":\\" suite [ \\"else\\" \\":\\" suite ]",
        "try_stmt : ( \\"try\\" \\":\\" suite ( ( except_clause \\":\\" suite ) + [ \\"else\\" \\":\\" suite ] [ \\"finally\\" \\":\\" suite ] | \\"finally\\" \\":\\" suite ) )",
        "with_stmt : \\"with\\" with_item ( \\",\\" with_item ) * \\":\\" suite",
        "with_item : test [ \\"as\\" expr ]",
        "except_clause : \\"except\\" [ test [ \\"as\\" NAME ] ]",
        "suite : simple_stmt | NEWLINE INDENT stmt + DEDENT",
        "?test : or_test [ \\"if\\" or_test \\"else\\" test ] | lambdef",
        "?test_nocond : or_test | lambdef_nocond",
        "lambdef : \\"lambda\\" [ varargslist ] \\":\\" test",
        "lambdef_nocond : \\"lambda\\" [ varargslist ] \\":\\" test_nocond",
        "?or_test : and_test ( \\"or\\" and_test ) *",
        "?and_test : not_test ( \\"and\\" not_test ) *",
        "?not_test : \\"not\\" not_test -> not \\n         | comparison",
        "?comparison : expr ( _comp_op expr ) *",
        "star_expr : \\"*\\" expr",
        "?expr : xor_expr ( \\"|\\" xor_expr ) *",
        "?xor_expr : and_expr ( \\"^\\" and_expr ) *",
        "?and_expr : shift_expr ( \\"&\\" shift_expr ) *",
        "?shift_expr : arith_expr ( _shift_op arith_expr ) *",
        "?arith_expr : term ( _add_op term ) *",
        "?term : factor ( _mul_op factor ) *",
        "?factor : _factor_op factor | power",
        "!_factor_op : \\"+\\" | \\"-\\" | \\"~\\"",
        "!_add_op : \\"+\\" | \\"-\\"",
        "!_shift_op : \\"<<\\" | \\">>\\"",
        "!_mul_op : \\"*\\" | \\"@\\" | \\"/\\" | \\"%\\" | \\"//\\"",
        "!_comp_op : \\"<\\" | \\">\\" | \\"==\\" | \\">=\\" | \\"<=\\" | \\"<>\\" | \\"!=\\" | \\"in\\" | \\"not\\" \\"in\\" | \\"is\\" | \\"is\\" \\"not\\"",
        "?power : await_expr [ \\"**\\" factor ]",
        "?await_expr : [ \\"await\\" ] atom_expr",
        "?atom_expr : atom_expr \\"(\\" [ arguments ] \\")\\" -> funccall \\n          | atom_expr \\"[\\" subscriptlist \\"]\\" -> getitem \\n          | atom_expr \\".\\" NAME -> getattr \\n          | atom",
        "?atom : \\"(\\" [ yield_expr | testlist_comp ] \\")\\" -> tuple \\n     | \\"[\\" [ testlist_comp ] \\"]\\" -> list \\n     | \\"{\\" [ dictorsetmaker ] \\"}\\" -> dict \\n     | NAME -> var \\n     | number | string + \\n     | \\"(\\" test \\")\\" -> par_group \\n     | \\"...\\" -> ellipsis \\n     | \\"None\\" -> const_none \\n     | \\"True\\" -> const_true \\n     | \\"False\\" -> const_false",
        "!?testlist_comp : ( test | star_expr ) [ comp_for | ( \\",\\" ( test | star_expr ) ) + [ \\",\\" ] | \\",\\" ]",
        "!subscriptlist : subscript ( \\",\\" subscript ) * [ \\",\\" ]",
        "subscript : test | [ test ] \\":\\" [ test ] [ sliceop ]",
        "sliceop : \\":\\" [ test ]",
        "!exprlist : ( expr | star_expr ) ( \\",\\" ( expr | star_expr ) ) * [ \\",\\" ]",
        "!testlist : test ( \\",\\" test ) * [ \\",\\" ]",
        "!dictorsetmaker : ( ( ( test \\":\\" test | \\"**\\" expr ) ( comp_for | ( \\",\\" ( test \\":\\" test | \\"**\\" expr ) ) * [ \\",\\" ] ) ) | ( ( test | star_expr ) ( comp_for | ( \\",\\" ( test | star_expr ) ) * [ \\",\\" ] ) ) )",
        "classdef : \\"class\\" NAME [ \\"(\\" [ arguments ] \\")\\" ] \\":\\" suite",
        "!arguments : argvalue ( \\",\\" argvalue ) * [ \\",\\" [ starargs | kwargs ] ] \\n         | starargs \\n         | kwargs \\n         | test comp_for",
        "!starargs : \\"*\\" test ( \\",\\" \\"*\\" test ) * ( \\",\\" argvalue ) * [ \\",\\" kwargs ]",
        "kwargs : \\"**\\" test",
        "?argvalue : test [ \\"=\\" test ]",
        "comp_iter : comp_for | comp_if | async_for",
        "async_for : \\"async\\" \\"for\\" exprlist \\"in\\" or_test [ comp_iter ]",
        "comp_for : \\"for\\" exprlist \\"in\\" or_test [ comp_iter ]",
        "comp_if : \\"if\\" test_nocond [ comp_iter ]",
        "encoding_decl : NAME",
        "yield_expr : \\"yield\\" [ yield_arg ]",
        "yield_arg : \\"from\\" test | testlist",
        "number : DEC_NUMBER | HEX_NUMBER | OCT_NUMBER | FLOAT_NUMBER | IMAG_NUMBER",
        "string : STRING | LONG_STRING",
        "COMMENT : /#[^\\\\n]*/",
        "NEWLINE : ( /\\\\r?\\\\n[\\\\t ]*/ | COMMENT ) +",
        "STRING : /[ubf]?r?(\\"(?!\\"\\").*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?\\"|'(?!'').*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?')/i",
        "LONG_STRING : /[ubf]?r?(\\"\\"\\".*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?\\"\\"\\"|'''.*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?''')/is",
        "HEX_NUMBER . 2 : /0x[\\\\da-f]*/i",
        "OCT_NUMBER . 2 : /0o[0-7]*/i",
        "BIN_NUMBER . 2 : /0b[0-1]*/i",
        "FLOAT_NUMBER . 2 : /((\\\\d+\\\\.\\\\d*|\\\\.\\\\d+)(e[-+]?\\\\d+)?|\\\\d+(e[-+]?\\\\d+))/i",
        "IMAG_NUMBER . 2 : /\\\\d+j|${FLOAT_NUMBER}j/i",
        "%ignore /[\\\\t \\\\f]+/",
        "%ignore /\\\\\\\\[\\\\t \\\\f]*\\\\r?\\\\n/",
        "%ignore COMMENT",
        "%declare INDENT DEDENT"
      ]
    },
    "விதிகள்": {
      "single_input : _NEWLINE | simple_stmt | compound_stmt _NEWLINE": {
        "பெயர்ப்பு": {}
      },
      "?file_input : ( _NEWLINE | stmt ) *": {
        "பெயர்ப்பு": {}
      },
      "eval_input : testlist _NEWLINE ?": {
        "பெயர்ப்பு": {}
      },
      "decorator : \\"@\\" dotted_name [ \\"(\\" [ arglist ] \\")\\" ] _NEWLINE": {
        "பெயர்ப்பு": {}
      },
      "decorators : decorator +": {
        "பெயர்ப்பு": {}
      },
      "decorated : decorators ( classdef | funcdef )": {
        "பெயர்ப்பு": {}
      },
      "funcdef : \\"def\\" NAME \\"(\\" parameters \\")\\" \\":\\" suite": {
        "பெயர்ப்பு": {}
      },
      "parameters : [ paramlist ]": {
        "பெயர்ப்பு": {}
      },
      "paramlist : param ( \\",\\" param ) * [ \\",\\" [ star_params [ \\",\\" kw_params ] | kw_params ] ] \\n           | star_params [ \\",\\" kw_params ] \\n           | kw_params": {
        "பெயர்ப்பு": {}
      },
      "star_params : \\"*\\" NAME": {
        "பெயர்ப்பு": {}
      },
      "kw_params : \\"**\\" NAME": {
        "பெயர்ப்பு": {}
      },
      "param : fpdef [ \\"=\\" test ]": {
        "பெயர்ப்பு": {}
      },
      "fpdef : NAME | \\"(\\" fplist \\")\\"": {
        "பெயர்ப்பு": {}
      },
      "fplist : fpdef ( \\",\\" fpdef ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "?stmt : simple_stmt | compound_stmt": {
        "பெயர்ப்பு": {}
      },
      "?simple_stmt : small_stmt ( \\";\\" small_stmt ) * [ \\";\\" ] _NEWLINE": {
        "பெயர்ப்பு": {}
      },
      "?small_stmt : ( expr_stmt | print_stmt | del_stmt | pass_stmt | flow_stmt \\n          | import_stmt | global_stmt | exec_stmt | assert_stmt )": {
        "பெயர்ப்பு": {}
      },
      "expr_stmt : testlist augassign ( yield_expr | testlist ) -> augassign2 \\n         | testlist ( \\"=\\" ( yield_expr | testlist ) ) + -> assign \\n         | testlist": {
        "பெயர்ப்பு": {}
      },
      "augassign : ( \\"+=\\" | \\"-=\\" | \\"*=\\" | \\"/=\\" | \\"%=\\" | \\"&=\\" | \\"|=\\" | \\"^=\\" | \\"<<=\\" | \\">>=\\" | \\"**=\\" | \\"//=\\" )": {
        "பெயர்ப்பு": {}
      },
      "print_stmt : \\"print\\" ( [ test ( \\",\\" test ) * [ \\",\\" ] ] | \\">>\\" test [ ( \\",\\" test ) + [ \\",\\" ] ] )": {
        "பெயர்ப்பு": {
          "த": "print_stmt : \\"பதிப்பி\\" ( [ test ( \\",\\" test ) * [ \\",\\" ] ] | \\">>\\" test [ ( \\",\\" test ) + [ \\",\\" ] ] )",
          "fr": "print_stmt : \\"afficher\\" ( [ test ( \\",\\" test ) * [ \\",\\" ] ] | \\">>\\" test [ ( \\",\\" test ) + [ \\",\\" ] ] )"
        }
      },
      "del_stmt : \\"del\\" exprlist": {
        "பெயர்ப்பு": {}
      },
      "pass_stmt : \\"pass\\"": {
        "பெயர்ப்பு": {
          "த": "pass_stmt : \\"விடு\\"",
          "fr": "pass_stmt : \\"passer\\""
        }
      },
      "?flow_stmt : break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt": {
        "பெயர்ப்பு": {}
      },
      "break_stmt : \\"break\\"": {
        "பெயர்ப்பு": {}
      },
      "continue_stmt : \\"continue\\"": {
        "பெயர்ப்பு": {}
      },
      "return_stmt : \\"return\\" [ testlist ]": {
        "பெயர்ப்பு": {
          "த": "return_stmt : \\"பின்கொடு\\" [ testlist ]",
          "fr": "return_stmt : \\"renvoie\\" [ testlist ]"
        }
      },
      "yield_stmt : yield_expr": {
        "பெயர்ப்பு": {}
      },
      "raise_stmt : \\"raise\\" [ test [ \\",\\" test [ \\",\\" test ] ] ]": {
        "பெயர்ப்பு": {}
      },
      "import_stmt : import_name | import_from": {
        "பெயர்ப்பு": {}
      },
      "import_name : \\"import\\" dotted_as_names": {
        "பெயர்ப்பு": {
          "த": "import_name : \\"உள்ளீடு\\" dotted_as_names"
        }
      },
      "import_from : \\"from\\" ( \\".\\" * dotted_name | \\".\\" + ) \\"import\\" ( \\"*\\" | \\"(\\" import_as_names \\")\\" | import_as_names )": {
        "பெயர்ப்பு": {}
      },
      "?import_as_name : NAME [ \\"as\\" NAME ]": {
        "பெயர்ப்பு": {}
      },
      "?dotted_as_name : dotted_name [ \\"as\\" NAME ]": {
        "பெயர்ப்பு": {}
      },
      "import_as_names : import_as_name ( \\",\\" import_as_name ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "dotted_as_names : dotted_as_name ( \\",\\" dotted_as_name ) *": {
        "பெயர்ப்பு": {}
      },
      "dotted_name : NAME ( \\".\\" NAME ) *": {
        "பெயர்ப்பு": {}
      },
      "global_stmt : \\"global\\" NAME ( \\",\\" NAME ) *": {
        "பெயர்ப்பு": {}
      },
      "exec_stmt : \\"exec\\" expr [ \\"in\\" test [ \\",\\" test ] ]": {
        "பெயர்ப்பு": {}
      },
      "assert_stmt : \\"assert\\" test [ \\",\\" test ]": {
        "பெயர்ப்பு": {
          "த": "assert_stmt : \\"உறுதி\\" test [ \\",\\" test ]"
        }
      },
      "?compound_stmt : if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated": {
        "பெயர்ப்பு": {}
      },
      "if_stmt : \\"if\\" test \\":\\" suite ( \\"elif\\" test \\":\\" suite ) * [ \\"else\\" \\":\\" suite ]": {
        "பெயர்ப்பு": {
          "த": "if_stmt : test \\"ஆனால்\\" \\":\\" suite ( \\"இல்லை\\" test \\"ஆனால்\\" \\":\\" suite ) * [ \\"ஏதேனில்\\" \\":\\" suite ]",
          "fr": "if_stmt : \\"si\\" test \\":\\" suite ( \\"sinonsi\\" test \\":\\" suite ) * [ \\"sinon\\" \\":\\" suite ]"
        }
      },
      "while_stmt : \\"while\\" test \\":\\" suite [ \\"else\\" \\":\\" suite ]": {
        "பெயர்ப்பு": {
          "த": "while_stmt : test \\"வரை\\" \\":\\" suite [ \\"ஏதேனில்\\" \\":\\" suite ]",
          "fr": "while_stmt : \\"tant\\" \\"que\\" test \\":\\" suite [ \\"sinon\\" \\":\\" suite ]"
        }
      },
      "for_stmt : \\"for\\" exprlist \\"in\\" testlist \\":\\" suite [ \\"else\\" \\":\\" suite ]": {
        "பெயர்ப்பு": {
          "த": "for_stmt : \\"ஒவ்வொன்றாக\\" exprlist testlist \\"இல்\\" \\":\\" suite [ \\"ஏதேனில்\\" \\":\\" suite ]",
          "fr": "for_stmt : \\"pour\\" exprlist \\"dans\\" testlist \\":\\" suite [ \\"sinon\\" \\":\\" suite ]"
        }
      },
      "try_stmt : ( \\"try\\" \\":\\" suite ( ( except_clause \\":\\" suite ) + [ \\"else\\" \\":\\" suite ] [ \\"finally\\" \\":\\" suite ] | \\"finally\\" \\":\\" suite ) )": {
        "பெயர்ப்பு": {}
      },
      "with_stmt : \\"with\\" with_item ( \\",\\" with_item ) * \\":\\" suite": {
        "பெயர்ப்பு": {
          "fr": "with_stmt : \\"avec\\" with_item ( \\",\\" with_item ) * \\":\\" suite"
        }
      },
      "with_item : test [ \\"as\\" expr ]": {
        "பெயர்ப்பு": {}
      },
      "except_clause : \\"except\\" [ test [ ( \\"as\\" | \\",\\" ) test ] ]": {
        "பெயர்ப்பு": {}
      },
      "suite : simple_stmt | _NEWLINE _INDENT _NEWLINE ? stmt + _DEDENT _NEWLINE ?": {
        "பெயர்ப்பு": {}
      },
      "testlist_safe : old_test [ ( \\",\\" old_test ) + [ \\",\\" ] ]": {
        "பெயர்ப்பு": {}
      },
      "old_test : or_test | old_lambdef": {
        "பெயர்ப்பு": {}
      },
      "old_lambdef : \\"lambda\\" [ paramlist ] \\":\\" old_test": {
        "பெயர்ப்பு": {}
      },
      "?test : or_test [ \\"if\\" or_test \\"else\\" test ] | lambdef": {
        "பெயர்ப்பு": {}
      },
      "?or_test : and_test ( \\"or\\" and_test ) *": {
        "பெயர்ப்பு": {}
      },
      "?and_test : not_test ( \\"and\\" not_test ) *": {
        "பெயர்ப்பு": {}
      },
      "?not_test : \\"not\\" not_test | comparison": {
        "பெயர்ப்பு": {
          "த": "?not_test : not_test \\"இல்லை\\" | comparison",
          "fr": "?not_test : \\"pas\\" not_test | comparison"
        }
      },
      "?comparison : expr ( comp_op expr ) *": {
        "பெயர்ப்பு": {}
      },
      "comp_op : \\"<\\" | \\">\\" | \\"==\\" | \\">=\\" | \\"<=\\" | \\"<>\\" | \\"!=\\" | \\"in\\" | \\"not\\" \\"in\\" | \\"is\\" | \\"is\\" \\"not\\"": {
        "பெயர்ப்பு": {}
      },
      "?expr : xor_expr ( \\"|\\" xor_expr ) *": {
        "பெயர்ப்பு": {}
      },
      "?xor_expr : and_expr ( \\"^\\" and_expr ) *": {
        "பெயர்ப்பு": {}
      },
      "?and_expr : shift_expr ( \\"&\\" shift_expr ) *": {
        "பெயர்ப்பு": {}
      },
      "?shift_expr : arith_expr ( ( \\"<<\\" | \\">>\\" ) arith_expr ) *": {
        "பெயர்ப்பு": {}
      },
      "?arith_expr : term ( ( \\"+\\" | \\"-\\" ) term ) *": {
        "பெயர்ப்பு": {}
      },
      "?term : factor ( ( \\"*\\" | \\"/\\" | \\"%\\" | \\"//\\" ) factor ) *": {
        "பெயர்ப்பு": {}
      },
      "?factor : ( \\"+\\" | \\"-\\" | \\"~\\" ) factor | power": {
        "பெயர்ப்பு": {}
      },
      "?power : molecule [ \\"**\\" factor ]": {
        "பெயர்ப்பு": {}
      },
      "?molecule : molecule \\"(\\" [ arglist ] \\")\\" -> func_call \\n         | molecule \\"[\\" [ subscriptlist ] \\"]\\" -> getitem \\n         | molecule \\".\\" NAME -> getattr \\n         | atom": {
        "பெயர்ப்பு": {}
      },
      "?atom : \\"(\\" [ yield_expr | testlist_comp ] \\")\\" -> tuple \\n    | \\"[\\" [ listmaker ] \\"]\\" \\n    | \\"{\\" [ dictorsetmaker ] \\"}\\" \\n    | \\"`\\" testlist1 \\"`\\" \\n    | \\"(\\" test \\")\\" \\n    | NAME | number | string +": {
        "பெயர்ப்பு": {}
      },
      "listmaker : test ( list_for | ( \\",\\" test ) * [ \\",\\" ] )": {
        "பெயர்ப்பு": {}
      },
      "?testlist_comp : test ( comp_for | ( \\",\\" test ) + [ \\",\\" ] | \\",\\" )": {
        "பெயர்ப்பு": {}
      },
      "lambdef : \\"lambda\\" [ paramlist ] \\":\\" test": {
        "பெயர்ப்பு": {}
      },
      "?subscriptlist : subscript ( \\",\\" subscript ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "subscript : \\".\\" \\".\\" \\".\\" | test | [ test ] \\":\\" [ test ] [ sliceop ]": {
        "பெயர்ப்பு": {}
      },
      "sliceop : \\":\\" [ test ]": {
        "பெயர்ப்பு": {}
      },
      "?exprlist : expr ( \\",\\" expr ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "?testlist : test ( \\",\\" test ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "dictorsetmaker : ( ( test \\":\\" test ( comp_for | ( \\",\\" test \\":\\" test ) * [ \\",\\" ] ) ) | ( test ( comp_for | ( \\",\\" test ) * [ \\",\\" ] ) ) )": {
        "பெயர்ப்பு": {}
      },
      "classdef : \\"class\\" NAME [ \\"(\\" [ testlist ] \\")\\" ] \\":\\" suite": {
        "பெயர்ப்பு": {}
      },
      "arglist : ( argument \\",\\" ) * ( argument [ \\",\\" ] \\n                         | star_args [ \\",\\" kw_args ] \\n                         | kw_args )": {
        "பெயர்ப்பு": {}
      },
      "star_args : \\"*\\" test": {
        "பெயர்ப்பு": {}
      },
      "kw_args : \\"**\\" test": {
        "பெயர்ப்பு": {}
      },
      "argument : test [ comp_for ] | test \\"=\\" test": {
        "பெயர்ப்பு": {}
      },
      "list_iter : list_for | list_if": {
        "பெயர்ப்பு": {}
      },
      "list_for : \\"for\\" exprlist \\"in\\" testlist_safe [ list_iter ]": {
        "பெயர்ப்பு": {}
      },
      "list_if : \\"if\\" old_test [ list_iter ]": {
        "பெயர்ப்பு": {}
      },
      "comp_iter : comp_for | comp_if": {
        "பெயர்ப்பு": {}
      },
      "comp_for : \\"for\\" exprlist \\"in\\" or_test [ comp_iter ]": {
        "பெயர்ப்பு": {
          "த": "comp_for : \\"ஒவ்வொன்றாக\\" exprlist or_test \\"இல்\\" [ comp_iter ]",
          "fr": "comp_for : \\"pour\\" exprlist \\"de\\" or_test [ comp_iter ]"
        }
      },
      "comp_if : \\"if\\" old_test [ comp_iter ]": {
        "பெயர்ப்பு": {}
      },
      "testlist1 : test ( \\",\\" test ) *": {
        "பெயர்ப்பு": {}
      },
      "yield_expr : \\"yield\\" [ testlist ]": {
        "பெயர்ப்பு": {}
      },
      "number : DEC_NUMBER | HEX_NUMBER | OCT_NUMBER | FLOAT | IMAG_NUMBER": {
        "பெயர்ப்பு": {}
      },
      "string : STRING | LONG_STRING": {
        "பெயர்ப்பு": {}
      },
      "COMMENT : /#[^\\\\n]*/": {
        "பெயர்ப்பு": {}
      },
      "_NEWLINE : ( /\\\\r?\\\\n[\\\\t ]*/ | COMMENT ) +": {
        "பெயர்ப்பு": {}
      },
      "STRING : /[ubf]?r?(\\"(?!\\"\\").*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?\\"|'(?!'').*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?')/i": {
        "பெயர்ப்பு": {}
      },
      "LONG_STRING . 2 : /[ubf]?r?(\\"\\"\\".*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?\\"\\"\\"|'''.*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?''')/is": {
        "பெயர்ப்பு": {}
      },
      "HEX_NUMBER : /0x[\\\\da-f]*l?/i": {
        "பெயர்ப்பு": {}
      },
      "OCT_NUMBER : /0o?[0-7]*l?/i": {
        "பெயர்ப்பு": {}
      },
      "%import common . FLOAT -> FLOAT": {
        "பெயர்ப்பு": {}
      },
      "%import common . INT -> _INT": {
        "பெயர்ப்பு": {}
      },
      "%import common . CNAME -> NAME": {
        "பெயர்ப்பு": {}
      },
      "IMAG_NUMBER : ( _INT | FLOAT ) ( \\"j\\" | \\"J\\" )": {
        "பெயர்ப்பு": {}
      },
      "%ignore /[\\\\t \\\\f]+/": {
        "பெயர்ப்பு": {}
      },
      "%ignore /\\\\\\\\[\\\\t \\\\f]*\\\\r?\\\\n/": {
        "பெயர்ப்பு": {}
      },
      "%ignore COMMENT": {
        "பெயர்ப்பு": {}
      },
      "%declare _INDENT _DEDENT": {
        "பெயர்ப்பு": {}
      },
      "single_input : NEWLINE | simple_stmt | compound_stmt NEWLINE": {
        "பெயர்ப்பு": {}
      },
      "file_input : ( NEWLINE | stmt ) *": {
        "பெயர்ப்பு": {}
      },
      "eval_input : testlist NEWLINE *": {
        "பெயர்ப்பு": {}
      },
      "!decorator : \\"@\\" dotted_name [ \\"(\\" [ arguments ] \\")\\" ] NEWLINE": {
        "பெயர்ப்பு": {}
      },
      "decorated : decorators ( classdef | funcdef | async_funcdef )": {
        "பெயர்ப்பு": {}
      },
      "async_funcdef : \\"async\\" funcdef": {
        "பெயர்ப்பு": {}
      },
      "funcdef : \\"def\\" NAME \\"(\\" parameters ? \\")\\" [ \\"->\\" test ] \\":\\" suite": {
        "பெயர்ப்பு": {
          "த": "funcdef : \\"நிரல்பாகம்\\" NAME \\"(\\" parameters ? \\")\\" [ \\"->\\" test ] \\":\\" suite",
          "fr": "funcdef : \\"déf\\" NAME \\"(\\" parameters ? \\")\\" [ \\"->\\" test ] \\":\\" suite"
        }
      },
      "!parameters : paramvalue ( \\",\\" paramvalue ) * [ \\",\\" [ starparams | kwparams ] ] \\n          | starparams \\n          | kwparams": {
        "பெயர்ப்பு": {}
      },
      "starparams : \\"*\\" typedparam ? ( \\",\\" paramvalue ) * [ \\",\\" kwparams ]": {
        "பெயர்ப்பு": {}
      },
      "kwparams : \\"**\\" typedparam": {
        "பெயர்ப்பு": {}
      },
      "?paramvalue : typedparam [ \\"=\\" test ]": {
        "பெயர்ப்பு": {}
      },
      "?typedparam : NAME [ \\":\\" test ]": {
        "பெயர்ப்பு": {}
      },
      "!varargslist : ( vfpdef [ \\"=\\" test ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"*\\" [ vfpdef ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"**\\" vfpdef [ \\",\\" ] ] ] | \\"**\\" vfpdef [ \\",\\" ] ] ] \\n  | \\"*\\" [ vfpdef ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"**\\" vfpdef [ \\",\\" ] ] ] \\n  | \\"**\\" vfpdef [ \\",\\" ] )": {
        "பெயர்ப்பு": {}
      },
      "vfpdef : NAME": {
        "பெயர்ப்பு": {}
      },
      "!?simple_stmt : small_stmt ( \\";\\" small_stmt ) * [ \\";\\" ] NEWLINE": {
        "பெயர்ப்பு": {}
      },
      "?small_stmt : ( expr_stmt | del_stmt | pass_stmt | flow_stmt | import_stmt | global_stmt | nonlocal_stmt | assert_stmt )": {
        "பெயர்ப்பு": {}
      },
      "?expr_stmt : testlist_star_expr ( annassign | augassign ( yield_expr | testlist ) \\n         | ( \\"=\\" ( yield_expr | testlist_star_expr ) ) * )": {
        "பெயர்ப்பு": {}
      },
      "annassign : \\":\\" test [ \\"=\\" test ]": {
        "பெயர்ப்பு": {}
      },
      "!?testlist_star_expr : ( test | star_expr ) ( \\",\\" ( test | star_expr ) ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "!augassign : ( \\"+=\\" | \\"-=\\" | \\"*=\\" | \\"@=\\" | \\"/=\\" | \\"%=\\" | \\"&=\\" | \\"|=\\" | \\"^=\\" | \\"<<=\\" | \\">>=\\" | \\"**=\\" | \\"//=\\" )": {
        "பெயர்ப்பு": {}
      },
      "flow_stmt : break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt": {
        "பெயர்ப்பு": {}
      },
      "raise_stmt : \\"raise\\" [ test [ \\"from\\" test ] ]": {
        "பெயர்ப்பு": {}
      },
      "import_from : \\"from\\" ( dots ? dotted_name | dots ) \\"import\\" ( \\"*\\" | \\"(\\" import_as_names \\")\\" | import_as_names )": {
        "பெயர்ப்பு": {}
      },
      "!dots : \\".\\" +": {
        "பெயர்ப்பு": {}
      },
      "import_as_name : NAME [ \\"as\\" NAME ]": {
        "பெயர்ப்பு": {}
      },
      "dotted_as_name : dotted_name [ \\"as\\" NAME ]": {
        "பெயர்ப்பு": {}
      },
      "!import_as_names : import_as_name ( \\",\\" import_as_name ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "nonlocal_stmt : \\"nonlocal\\" NAME ( \\",\\" NAME ) *": {
        "பெயர்ப்பு": {}
      },
      "compound_stmt : if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated | async_stmt": {
        "பெயர்ப்பு": {}
      },
      "async_stmt : \\"async\\" ( funcdef | with_stmt | for_stmt )": {
        "பெயர்ப்பு": {}
      },
      "except_clause : \\"except\\" [ test [ \\"as\\" NAME ] ]": {
        "பெயர்ப்பு": {}
      },
      "suite : simple_stmt | NEWLINE INDENT stmt + DEDENT": {
        "பெயர்ப்பு": {}
      },
      "?test_nocond : or_test | lambdef_nocond": {
        "பெயர்ப்பு": {}
      },
      "lambdef : \\"lambda\\" [ varargslist ] \\":\\" test": {
        "பெயர்ப்பு": {}
      },
      "lambdef_nocond : \\"lambda\\" [ varargslist ] \\":\\" test_nocond": {
        "பெயர்ப்பு": {}
      },
      "?not_test : \\"not\\" not_test -> not \\n         | comparison": {
        "பெயர்ப்பு": {
          "த": "?not_test : not_test \\"இல்லை\\" -> not \\n         | comparison",
          "fr": "?not_test : \\"pas\\" not_test -> not \\n         | comparison"
        }
      },
      "?comparison : expr ( _comp_op expr ) *": {
        "பெயர்ப்பு": {}
      },
      "star_expr : \\"*\\" expr": {
        "பெயர்ப்பு": {}
      },
      "?shift_expr : arith_expr ( _shift_op arith_expr ) *": {
        "பெயர்ப்பு": {}
      },
      "?arith_expr : term ( _add_op term ) *": {
        "பெயர்ப்பு": {}
      },
      "?term : factor ( _mul_op factor ) *": {
        "பெயர்ப்பு": {}
      },
      "?factor : _factor_op factor | power": {
        "பெயர்ப்பு": {}
      },
      "!_factor_op : \\"+\\" | \\"-\\" | \\"~\\"": {
        "பெயர்ப்பு": {}
      },
      "!_add_op : \\"+\\" | \\"-\\"": {
        "பெயர்ப்பு": {}
      },
      "!_shift_op : \\"<<\\" | \\">>\\"": {
        "பெயர்ப்பு": {}
      },
      "!_mul_op : \\"*\\" | \\"@\\" | \\"/\\" | \\"%\\" | \\"//\\"": {
        "பெயர்ப்பு": {}
      },
      "!_comp_op : \\"<\\" | \\">\\" | \\"==\\" | \\">=\\" | \\"<=\\" | \\"<>\\" | \\"!=\\" | \\"in\\" | \\"not\\" \\"in\\" | \\"is\\" | \\"is\\" \\"not\\"": {
        "பெயர்ப்பு": {}
      },
      "?power : await_expr [ \\"**\\" factor ]": {
        "பெயர்ப்பு": {}
      },
      "?await_expr : [ \\"await\\" ] atom_expr": {
        "பெயர்ப்பு": {}
      },
      "?atom_expr : atom_expr \\"(\\" [ arguments ] \\")\\" -> funccall \\n          | atom_expr \\"[\\" subscriptlist \\"]\\" -> getitem \\n          | atom_expr \\".\\" NAME -> getattr \\n          | atom": {
        "பெயர்ப்பு": {}
      },
      "?atom : \\"(\\" [ yield_expr | testlist_comp ] \\")\\" -> tuple \\n     | \\"[\\" [ testlist_comp ] \\"]\\" -> list \\n     | \\"{\\" [ dictorsetmaker ] \\"}\\" -> dict \\n     | NAME -> var \\n     | number | string + \\n     | \\"(\\" test \\")\\" -> par_group \\n     | \\"...\\" -> ellipsis \\n     | \\"None\\" -> const_none \\n     | \\"True\\" -> const_true \\n     | \\"False\\" -> const_false": {
        "பெயர்ப்பு": {
          "த": "?atom : \\"(\\" [ yield_expr | testlist_comp ] \\")\\" -> tuple \\n     | \\"[\\" [ testlist_comp ] \\"]\\" -> list \\n     | \\"{\\" [ dictorsetmaker ] \\"}\\" -> dict \\n     | NAME -> var \\n     | number | string + \\n     | \\"(\\" test \\")\\" -> par_group \\n     | \\"...\\" -> ellipsis \\n     | \\"ஒன்றுமில்லை\\" -> const_none \\n     | \\"உண்மை\\" -> const_true \\n     | \\"தப்பு\\" -> const_false",
          "fr": "?atom : \\"(\\" [ yield_expr | testlist_comp ] \\")\\" -> tuple \\n     | \\"[\\" [ testlist_comp ] \\"]\\" -> list \\n     | \\"{\\" [ dictorsetmaker ] \\"}\\" -> dict \\n     | NAME -> var \\n     | number | string + \\n     | \\"(\\" test \\")\\" -> par_group \\n     | \\"...\\" -> ellipsis \\n     | \\"Nulle\\" -> const_none \\n     | \\"Vrai\\" -> const_true \\n     | \\"Faux\\" -> const_false"
        }
      },
      "!?testlist_comp : ( test | star_expr ) [ comp_for | ( \\",\\" ( test | star_expr ) ) + [ \\",\\" ] | \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "!subscriptlist : subscript ( \\",\\" subscript ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "subscript : test | [ test ] \\":\\" [ test ] [ sliceop ]": {
        "பெயர்ப்பு": {}
      },
      "!exprlist : ( expr | star_expr ) ( \\",\\" ( expr | star_expr ) ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "!testlist : test ( \\",\\" test ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "!dictorsetmaker : ( ( ( test \\":\\" test | \\"**\\" expr ) ( comp_for | ( \\",\\" ( test \\":\\" test | \\"**\\" expr ) ) * [ \\",\\" ] ) ) | ( ( test | star_expr ) ( comp_for | ( \\",\\" ( test | star_expr ) ) * [ \\",\\" ] ) ) )": {
        "பெயர்ப்பு": {}
      },
      "classdef : \\"class\\" NAME [ \\"(\\" [ arguments ] \\")\\" ] \\":\\" suite": {
        "பெயர்ப்பு": {
          "த": "classdef : \\"தொகுப்பு\\" NAME [ \\"(\\" [ arguments ] \\")\\" ] \\":\\" suite",
          "fr": "classdef : \\"classe\\" NAME [ \\"(\\" [ arguments ] \\")\\" ] \\":\\" suite"
        }
      },
      "!arguments : argvalue ( \\",\\" argvalue ) * [ \\",\\" [ starargs | kwargs ] ] \\n         | starargs \\n         | kwargs \\n         | test comp_for": {
        "பெயர்ப்பு": {}
      },
      "!starargs : \\"*\\" test ( \\",\\" \\"*\\" test ) * ( \\",\\" argvalue ) * [ \\",\\" kwargs ]": {
        "பெயர்ப்பு": {}
      },
      "kwargs : \\"**\\" test": {
        "பெயர்ப்பு": {}
      },
      "?argvalue : test [ \\"=\\" test ]": {
        "பெயர்ப்பு": {}
      },
      "comp_iter : comp_for | comp_if | async_for": {
        "பெயர்ப்பு": {}
      },
      "async_for : \\"async\\" \\"for\\" exprlist \\"in\\" or_test [ comp_iter ]": {
        "பெயர்ப்பு": {}
      },
      "comp_if : \\"if\\" test_nocond [ comp_iter ]": {
        "பெயர்ப்பு": {}
      },
      "encoding_decl : NAME": {
        "பெயர்ப்பு": {}
      },
      "yield_expr : \\"yield\\" [ yield_arg ]": {
        "பெயர்ப்பு": {}
      },
      "yield_arg : \\"from\\" test | testlist": {
        "பெயர்ப்பு": {}
      },
      "number : DEC_NUMBER | HEX_NUMBER | OCT_NUMBER | FLOAT_NUMBER | IMAG_NUMBER": {
        "பெயர்ப்பு": {}
      },
      "NEWLINE : ( /\\\\r?\\\\n[\\\\t ]*/ | COMMENT ) +": {
        "பெயர்ப்பு": {}
      },
      "LONG_STRING : /[ubf]?r?(\\"\\"\\".*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?\\"\\"\\"|'''.*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?''')/is": {
        "பெயர்ப்பு": {}
      },
      "HEX_NUMBER . 2 : /0x[\\\\da-f]*/i": {
        "பெயர்ப்பு": {}
      },
      "OCT_NUMBER . 2 : /0o[0-7]*/i": {
        "பெயர்ப்பு": {}
      },
      "BIN_NUMBER . 2 : /0b[0-1]*/i": {
        "பெயர்ப்பு": {}
      },
      "FLOAT_NUMBER . 2 : /((\\\\d+\\\\.\\\\d*|\\\\.\\\\d+)(e[-+]?\\\\d+)?|\\\\d+(e[-+]?\\\\d+))/i": {
        "பெயர்ப்பு": {}
      },
      "IMAG_NUMBER . 2 : /\\\\d+j|${FLOAT_NUMBER}j/i": {
        "பெயர்ப்பு": {}
      },
      "%declare INDENT DEDENT": {
        "பெயர்ப்பு": {}
      },
      "DEC_NUMBER : /0|[1-9]\\\\d*/i": {
        "பெயர்ப்பு": {}
      }
    },
    "மொழிபெயர்ப்பாளர்கள்": [
      "ம. ஜூலீஎன் (julien.malard@mail.mcgill.ca)"
    ]
  },
  "lark": {
    "நீட்சி": {},
    "பெயர்": {},
    "பதிப்புகள்": {
      "": [
        "start : ( _item | NL ) *",
        "_item : rule \\n     | token \\n     | statement",
        "rule : RULE priority ? \\":\\" expansions NL",
        "token : TOKEN priority ? \\":\\" expansions NL",
        "priority : \\".\\" NUMBER",
        "statement : \\"%ignore\\" expansions NL -> ignore \\n         | \\"%import\\" import_args [ \\"->\\" TOKEN ] NL -> import \\n         | \\"%declare\\" name + -> declare",
        "import_args : name ( \\".\\" name ) *",
        "expansions : alias ( VBAR alias ) *",
        "alias : expansion [ \\"->\\" RULE ]",
        "expansion : expr *",
        "expr : atom [ OP | \\"~\\" NUMBER [ \\"..\\" NUMBER ] ]",
        "atom : \\"(\\" expansions \\")\\" \\n     | \\"[\\" expansions \\"]\\" -> maybe \\n     | STRING \\"..\\" STRING -> literal_range \\n     | name \\n     | ( REGEXP | STRING ) -> literal",
        "name : RULE \\n    | TOKEN",
        "VBAR : NL ? \\"|\\"",
        "OP : /[+*][?]?|[?](?![a-z])/",
        "RULE : /!?[_?]?[a-z][_a-z0-9]*/",
        "TOKEN : /_?[A-Z][_A-Z0-9]*/",
        "STRING : _STRING \\"i\\" ?",
        "REGEXP : /\\\\/(?!\\\\/)(\\\\\\\\\\\\/|\\\\\\\\\\\\\\\\|[^\\\\/\\\\n])*?\\\\/[imslux]*/",
        "NL : /(\\\\r?\\\\n)+\\\\s*/",
        "%import common . ESCAPED_STRING -> _STRING",
        "%import common . INT -> NUMBER",
        "%import common . WS_INLINE",
        "COMMENT : \\"//\\" /[^\\\\n]/ *",
        "%ignore WS_INLINE",
        "%ignore COMMENT"
      ]
    },
    "விதிகள்": {
      "start : ( _item | NL ) *": {
        "பெயர்ப்பு": {}
      },
      "_item : rule \\n     | token \\n     | statement": {
        "பெயர்ப்பு": {}
      },
      "rule : RULE priority ? \\":\\" expansions NL": {
        "பெயர்ப்பு": {}
      },
      "token : TOKEN priority ? \\":\\" expansions NL": {
        "பெயர்ப்பு": {}
      },
      "priority : \\".\\" NUMBER": {
        "பெயர்ப்பு": {}
      },
      "statement : \\"%ignore\\" expansions NL -> ignore \\n         | \\"%import\\" import_args [ \\"->\\" TOKEN ] NL -> import \\n         | \\"%declare\\" name + -> declare": {
        "பெயர்ப்பு": {}
      },
      "import_args : name ( \\".\\" name ) *": {
        "பெயர்ப்பு": {}
      },
      "expansions : alias ( VBAR alias ) *": {
        "பெயர்ப்பு": {}
      },
      "alias : expansion [ \\"->\\" RULE ]": {
        "பெயர்ப்பு": {}
      },
      "expansion : expr *": {
        "பெயர்ப்பு": {}
      },
      "expr : atom [ OP | \\"~\\" NUMBER [ \\"..\\" NUMBER ] ]": {
        "பெயர்ப்பு": {}
      },
      "atom : \\"(\\" expansions \\")\\" \\n     | \\"[\\" expansions \\"]\\" -> maybe \\n     | STRING \\"..\\" STRING -> literal_range \\n     | name \\n     | ( REGEXP | STRING ) -> literal": {
        "பெயர்ப்பு": {}
      },
      "name : RULE \\n    | TOKEN": {
        "பெயர்ப்பு": {}
      },
      "VBAR : NL ? \\"|\\"": {
        "பெயர்ப்பு": {}
      },
      "OP : /[+*][?]?|[?](?![a-z])/": {
        "பெயர்ப்பு": {}
      },
      "RULE : /!?[_?]?[a-z][_a-z0-9]*/": {
        "பெயர்ப்பு": {}
      },
      "TOKEN : /_?[A-Z][_A-Z0-9]*/": {
        "பெயர்ப்பு": {}
      },
      "STRING : _STRING \\"i\\" ?": {
        "பெயர்ப்பு": {}
      },
      "REGEXP : /\\\\/(?!\\\\/)(\\\\\\\\\\\\/|\\\\\\\\\\\\\\\\|[^\\\\/\\\\n])*?\\\\/[imslux]*/": {
        "பெயர்ப்பு": {}
      },
      "NL : /(\\\\r?\\\\n)+\\\\s*/": {
        "பெயர்ப்பு": {}
      },
      "%import common . ESCAPED_STRING -> _STRING": {
        "பெயர்ப்பு": {}
      },
      "%import common . INT -> NUMBER": {
        "பெயர்ப்பு": {}
      },
      "%import common . WS_INLINE": {
        "பெயர்ப்பு": {}
      },
      "COMMENT : \\"//\\" /[^\\\\n]/ *": {
        "பெயர்ப்பு": {}
      },
      "%ignore WS_INLINE": {
        "பெயர்ப்பு": {}
      },
      "%ignore COMMENT": {
        "பெயர்ப்பு": {}
      }
    },
    "மொழிபெயர்ப்பாளர்கள்": []
  },
  "json": {
    "நீட்சி": {},
    "பெயர்": {},
    "பதிப்புகள்": {
      "": [
        "?start : value",
        "?value : object \\n      | array \\n      | string \\n      | SIGNED_NUMBER -> number \\n      | \\"true\\" -> true \\n      | \\"false\\" -> false \\n      | \\"null\\" -> null",
        "array : \\"[\\" [ value ( \\",\\" value ) * ] \\"]\\"",
        "object : \\"{\\" [ pair ( \\",\\" pair ) * ] \\"}\\"",
        "pair : string \\":\\" value",
        "string : ESCAPED_STRING",
        "%import common . ESCAPED_STRING",
        "%import common . SIGNED_NUMBER",
        "%import common . WS",
        "%ignore WS"
      ]
    },
    "விதிகள்": {
      "?start : value": {
        "பெயர்ப்பு": {}
      },
      "?value : object \\n      | array \\n      | string \\n      | DEC_NUMBER -> number \\n      | \\"true\\" -> true \\n      | \\"false\\" -> false \\n      | \\"null\\" -> null": {
        "பெயர்ப்பு": {}
      },
      "array : \\"[\\" [ value ( \\",\\" value ) * ] \\"]\\"": {
        "பெயர்ப்பு": {}
      },
      "object : \\"{\\" [ pair ( \\",\\" pair ) * ] \\"}\\"": {
        "பெயர்ப்பு": {}
      },
      "pair : string \\":\\" value": {
        "பெயர்ப்பு": {}
      },
      "string : ESCAPED_STRING": {
        "பெயர்ப்பு": {}
      },
      "%import common . ESCAPED_STRING": {
        "பெயர்ப்பு": {}
      },
      "%import common . WS": {
        "பெயர்ப்பு": {}
      },
      "%ignore WS": {
        "பெயர்ப்பு": {}
      },
      "?value : object \\n      | array \\n      | string \\n      | SIGNED_NUMBER -> number \\n      | \\"true\\" -> true \\n      | \\"false\\" -> false \\n      | \\"null\\" -> null": {
        "பெயர்ப்பு": {
          "fr": "?value : object \\n      | array \\n      | string \\n      | SIGNED_NUMBER -> number \\n      | \\"vrai\\" -> true \\n      | \\"faux\\" -> false \\n      | \\"nul\\" -> null",
          "த": "?value : object \\n      | array \\n      | string \\n      | SIGNED_NUMBER -> number \\n      | \\"உண்மை\\" -> true \\n      | \\"தப்பு\\" -> false \\n      | \\"எதுமில்லை\\" -> null",
          "es": "?value : object \\n      | array \\n      | string \\n      | SIGNED_NUMBER -> number \\n      | \\"verdadero\\" -> true \\n      | \\"falso\\" -> false \\n      | \\"nulo\\" -> null"
        }
      },
      "%import common . SIGNED_NUMBER": {
        "பெயர்ப்பு": {}
      }
    },
    "மொழிபெயர்ப்பாளர்கள்": []
  },
  "nearley": {
    "நீட்சி": {},
    "பெயர்": {},
    "பதிப்புகள்": {
      "": [
        "start : ( ruledef | directive ) +",
        "directive : \\"@\\" NAME ( STRING | NAME ) \\n         | \\"@\\" JS -> js_code",
        "ruledef : NAME \\"->\\" expansions \\n       | NAME REGEXP \\"->\\" expansions -> macro",
        "expansions : expansion ( \\"|\\" expansion ) *",
        "expansion : expr + js",
        "?expr : item ( \\":\\" /[+*?]/ ) ?",
        "?item : rule | string | regexp | null \\n     | \\"(\\" expansions \\")\\"",
        "rule : NAME",
        "string : STRING",
        "regexp : REGEXP",
        "null : \\"null\\"",
        "JS : /{%.*?%}/s",
        "js : JS ?",
        "COMMENT : /#[^\\\\n]*/",
        "REGEXP : /\\\\[.*?\\\\]/",
        "%import common . ESCAPED_STRING -> STRING",
        "%import common . WS",
        "%ignore WS",
        "%ignore COMMENT"
      ]
    },
    "விதிகள்": {
      "start : ( ruledef | directive ) +": {
        "பெயர்ப்பு": {}
      },
      "directive : \\"@\\" NAME ( STRING | NAME ) \\n         | \\"@\\" JS -> js_code": {
        "பெயர்ப்பு": {}
      },
      "ruledef : NAME \\"->\\" expansions \\n       | NAME REGEXP \\"->\\" expansions -> macro": {
        "பெயர்ப்பு": {}
      },
      "expansions : expansion ( \\"|\\" expansion ) *": {
        "பெயர்ப்பு": {}
      },
      "expansion : expr + js": {
        "பெயர்ப்பு": {}
      },
      "?expr : item ( \\":\\" /[+*?]/ ) ?": {
        "பெயர்ப்பு": {}
      },
      "?item : rule | string | regexp | null \\n     | \\"(\\" expansions \\")\\"": {
        "பெயர்ப்பு": {}
      },
      "rule : NAME": {
        "பெயர்ப்பு": {}
      },
      "string : STRING": {
        "பெயர்ப்பு": {}
      },
      "regexp : REGEXP": {
        "பெயர்ப்பு": {}
      },
      "null : \\"null\\"": {
        "பெயர்ப்பு": {}
      },
      "JS : /{%.*?%}/s": {
        "பெயர்ப்பு": {}
      },
      "js : JS ?": {
        "பெயர்ப்பு": {}
      },
      "COMMENT : /#[^\\\\n]*/": {
        "பெயர்ப்பு": {}
      },
      "REGEXP : /\\\\[.*?\\\\]/": {
        "பெயர்ப்பு": {}
      },
      "%import common . ESCAPED_STRING -> STRING": {
        "பெயர்ப்பு": {}
      },
      "%import common . WS": {
        "பெயர்ப்பு": {}
      },
      "%ignore WS": {
        "பெயர்ப்பு": {}
      },
      "%ignore COMMENT": {
        "பெயர்ப்பு": {}
      }
    },
    "மொழிபெயர்ப்பாளர்கள்": []
  },
  "எழில்": {
    "நீட்சி": {},
    "பெயர்": {},
    "பதிப்புகள்": {
      "": [
        "single_input : NEWLINE | simple_stmt | compound_stmt NEWLINE",
        "file_input : ( NEWLINE | stmt ) *",
        "eval_input : testlist NEWLINE *",
        "!decorator : \\"@\\" dotted_name [ \\"(\\" [ arguments ] \\")\\" ] NEWLINE",
        "decorators : decorator +",
        "decorated : decorators ( classdef | funcdef | async_funcdef )",
        "async_funcdef : \\"async\\" funcdef",
        "funcdef : \\"நிரல்பாகம்\\" NAME \\"(\\" parameters ? \\")\\" suite \\"முடி\\"",
        "!parameters : paramvalue ( \\",\\" paramvalue ) * [ \\",\\" [ starparams | kwparams ] ] \\n          | starparams \\n          | kwparams",
        "starparams : \\"*\\" typedparam ? ( \\",\\" paramvalue ) * [ \\",\\" kwparams ]",
        "kwparams : \\"**\\" typedparam",
        "?paramvalue : typedparam [ \\"=\\" test ]",
        "?typedparam : NAME [ \\":\\" test ]",
        "!varargslist : ( vfpdef [ \\"=\\" test ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"*\\" [ vfpdef ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"**\\" vfpdef [ \\",\\" ] ] ] | \\"**\\" vfpdef [ \\",\\" ] ] ] \\n  | \\"*\\" [ vfpdef ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"**\\" vfpdef [ \\",\\" ] ] ] \\n  | \\"**\\" vfpdef [ \\",\\" ] )",
        "vfpdef : NAME",
        "?stmt : simple_stmt | compound_stmt",
        "!?simple_stmt : small_stmt ( \\";\\" small_stmt ) * [ \\";\\" ] NEWLINE",
        "?small_stmt : ( expr_stmt | del_stmt | pass_stmt | print_stmt | flow_stmt | import_stmt | global_stmt | nonlocal_stmt | assert_stmt )",
        "?expr_stmt : testlist_star_expr ( annassign | augassign ( yield_expr | testlist ) \\n         | ( \\"=\\" ( yield_expr | testlist_star_expr ) ) * )",
        "annassign : \\":\\" test [ \\"=\\" test ]",
        "!?testlist_star_expr : ( test | star_expr ) ( \\",\\" ( test | star_expr ) ) * [ \\",\\" ]",
        "!augassign : ( \\"+=\\" | \\"-=\\" | \\"*=\\" | \\"@=\\" | \\"/=\\" | \\"%=\\" | \\"&=\\" | \\"|=\\" | \\"^=\\" | \\"<<=\\" | \\">>=\\" | \\"**=\\" | \\"//=\\" )",
        "print_stmt : \\"பதிப்பி\\" [ test ( \\",\\" test ) * [ \\",\\" ] ]",
        "del_stmt : \\"del\\" exprlist",
        "pass_stmt : \\"pass\\"",
        "flow_stmt : break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt",
        "break_stmt : \\"நிறுத்து\\"",
        "continue_stmt : \\"தொடர்\\"",
        "return_stmt : \\"நிரல்பாகம்\\" [ testlist ]",
        "yield_stmt : yield_expr",
        "raise_stmt : \\"raise\\" [ test [ \\"from\\" test ] ]",
        "import_stmt : import_name | import_from",
        "import_name : \\"import\\" dotted_as_names",
        "import_from : \\"from\\" ( dots ? dotted_name | dots ) \\"import\\" ( \\"*\\" | \\"(\\" import_as_names \\")\\" | import_as_names )",
        "!dots : \\".\\" +",
        "import_as_name : NAME [ \\"as\\" NAME ]",
        "dotted_as_name : dotted_name [ \\"as\\" NAME ]",
        "!import_as_names : import_as_name ( \\",\\" import_as_name ) * [ \\",\\" ]",
        "dotted_as_names : dotted_as_name ( \\",\\" dotted_as_name ) *",
        "dotted_name : NAME ( \\".\\" NAME ) *",
        "global_stmt : \\"global\\" NAME ( \\",\\" NAME ) *",
        "nonlocal_stmt : \\"nonlocal\\" NAME ( \\",\\" NAME ) *",
        "assert_stmt : \\"assert\\" test [ \\",\\" test ]",
        "compound_stmt : if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated | async_stmt",
        "async_stmt : \\"async\\" ( funcdef | with_stmt | for_stmt )",
        "if_stmt : \\"@\\" \\"(\\" test \\")\\" \\"ஆனால்\\" suite ( \\"@\\" \\"(\\" test \\")\\" \\"இல்லைஆனால்\\" suite ) * [ \\"இல்லை\\" suite ] \\"முடி\\"",
        "while_stmt : \\"while\\" test \\":\\" suite [ \\"else\\" \\":\\" suite ]",
        "for_stmt : \\"@\\" \\"(\\" exprlist \\")\\" \\"ஆக\\" testlist \\":\\" suite [ \\"else\\" \\":\\" suite ]",
        "try_stmt : ( \\"try\\" \\":\\" suite ( ( except_clause \\":\\" suite ) + [ \\"else\\" \\":\\" suite ] [ \\"finally\\" \\":\\" suite ] | \\"finally\\" \\":\\" suite ) )",
        "with_stmt : \\"with\\" with_item ( \\",\\" with_item ) * \\":\\" suite",
        "with_item : test [ \\"as\\" expr ]",
        "except_clause : \\"except\\" [ test [ \\"as\\" NAME ] ]",
        "suite : simple_stmt | NEWLINE INDENT stmt + DEDENT",
        "?test : or_test [ \\"if\\" or_test \\"else\\" test ] | lambdef",
        "?test_nocond : or_test | lambdef_nocond",
        "lambdef : \\"lambda\\" [ varargslist ] \\":\\" test",
        "lambdef_nocond : \\"lambda\\" [ varargslist ] \\":\\" test_nocond",
        "?or_test : and_test ( \\"or\\" and_test ) *",
        "?and_test : not_test ( \\"and\\" not_test ) *",
        "?not_test : \\"not\\" not_test -> not \\n         | comparison",
        "?comparison : expr ( _comp_op expr ) *",
        "star_expr : \\"*\\" expr",
        "?expr : xor_expr ( \\"|\\" xor_expr ) *",
        "?xor_expr : and_expr ( \\"^\\" and_expr ) *",
        "?and_expr : shift_expr ( \\"&\\" shift_expr ) *",
        "?shift_expr : arith_expr ( _shift_op arith_expr ) *",
        "?arith_expr : term ( _add_op term ) *",
        "?term : factor ( _mul_op factor ) *",
        "?factor : _factor_op factor | power",
        "!_factor_op : \\"+\\" | \\"-\\" | \\"~\\"",
        "!_add_op : \\"+\\" | \\"-\\"",
        "!_shift_op : \\"<<\\" | \\">>\\"",
        "!_mul_op : \\"*\\" | \\"@\\" | \\"/\\" | \\"%\\" | \\"//\\"",
        "!_comp_op : \\"<\\" | \\">\\" | \\"==\\" | \\">=\\" | \\"<=\\" | \\"<>\\" | \\"!=\\" | \\"in\\" | \\"not\\" \\"in\\" | \\"is\\" | \\"is\\" \\"not\\"",
        "?power : await_expr [ \\"**\\" factor ]",
        "?await_expr : [ \\"await\\" ] atom_expr",
        "?atom_expr : atom_expr \\"(\\" [ arguments ] \\")\\" -> funccall \\n          | atom_expr \\"[\\" subscriptlist \\"]\\" -> getitem \\n          | atom_expr \\".\\" NAME -> getattr \\n          | atom",
        "?atom : \\"(\\" [ yield_expr | testlist_comp ] \\")\\" -> tuple \\n     | \\"[\\" [ testlist_comp ] \\"]\\" -> list \\n     | \\"{\\" [ dictorsetmaker ] \\"}\\" -> dict \\n     | NAME -> var \\n     | number | string + \\n     | \\"(\\" test \\")\\" -> par_group \\n     | \\"...\\" -> ellipsis \\n     | \\"None\\" -> const_none \\n     | \\"True\\" -> const_true \\n     | \\"False\\" -> const_false",
        "!?testlist_comp : ( test | star_expr ) [ comp_for | ( \\",\\" ( test | star_expr ) ) + [ \\",\\" ] | \\",\\" ]",
        "!subscriptlist : subscript ( \\",\\" subscript ) * [ \\",\\" ]",
        "subscript : test | [ test ] \\":\\" [ test ] [ sliceop ]",
        "sliceop : \\":\\" [ test ]",
        "!exprlist : ( expr | star_expr ) ( \\",\\" ( expr | star_expr ) ) * [ \\",\\" ]",
        "!testlist : test ( \\",\\" test ) * [ \\",\\" ]",
        "!dictorsetmaker : ( ( ( test \\":\\" test | \\"**\\" expr ) ( comp_for | ( \\",\\" ( test \\":\\" test | \\"**\\" expr ) ) * [ \\",\\" ] ) ) | ( ( test | star_expr ) ( comp_for | ( \\",\\" ( test | star_expr ) ) * [ \\",\\" ] ) ) )",
        "classdef : \\"class\\" NAME [ \\"(\\" [ arguments ] \\")\\" ] \\":\\" suite",
        "!arguments : argvalue ( \\",\\" argvalue ) * [ \\",\\" [ starargs | kwargs ] ] \\n         | starargs \\n         | kwargs \\n         | test comp_for",
        "!starargs : \\"*\\" test ( \\",\\" \\"*\\" test ) * ( \\",\\" argvalue ) * [ \\",\\" kwargs ]",
        "kwargs : \\"**\\" test",
        "?argvalue : test [ \\"=\\" test ]",
        "comp_iter : comp_for | comp_if | async_for",
        "async_for : \\"async\\" \\"for\\" exprlist \\"in\\" or_test [ comp_iter ]",
        "comp_for : \\"for\\" exprlist \\"in\\" or_test [ comp_iter ]",
        "comp_if : \\"if\\" test_nocond [ comp_iter ]",
        "encoding_decl : NAME",
        "yield_expr : \\"yield\\" [ yield_arg ]",
        "yield_arg : \\"from\\" test | testlist",
        "number : DEC_NUMBER | HEX_NUMBER | OCT_NUMBER | FLOAT_NUMBER | IMAG_NUMBER",
        "string : STRING | LONG_STRING",
        "COMMENT : /#[^\\\\n]*/",
        "NEWLINE : ( /\\\\r?\\\\n[\\\\t ]*/ | COMMENT ) +",
        "STRING : /[ubf]?r?(\\"(?!\\"\\").*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?\\"|'(?!'').*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?')/i",
        "LONG_STRING : /[ubf]?r?(\\"\\"\\".*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?\\"\\"\\"|'''.*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?''')/is",
        "HEX_NUMBER . 2 : /0x[\\\\da-f]*/i",
        "OCT_NUMBER . 2 : /0o[0-7]*/i",
        "BIN_NUMBER . 2 : /0b[0-1]*/i",
        "FLOAT_NUMBER . 2 : /((\\\\d+\\\\.\\\\d*|\\\\.\\\\d+)(e[-+]?\\\\d+)?|\\\\d+(e[-+]?\\\\d+))/i",
        "IMAG_NUMBER . 2 : /\\\\d+j|${FLOAT_NUMBER}j/i",
        "%ignore /[\\\\t \\\\f]+/",
        "%ignore /\\\\\\\\[\\\\t \\\\f]*\\\\r?\\\\n/",
        "%ignore COMMENT",
        "%declare INDENT DEDENT"
      ]
    },
    "விதிகள்": {
      "single_input : NEWLINE | simple_stmt | compound_stmt NEWLINE": {
        "பெயர்ப்பு": {}
      },
      "file_input : ( NEWLINE | stmt ) *": {
        "பெயர்ப்பு": {}
      },
      "eval_input : testlist NEWLINE *": {
        "பெயர்ப்பு": {}
      },
      "!decorator : \\"@\\" dotted_name [ \\"(\\" [ arguments ] \\")\\" ] NEWLINE": {
        "பெயர்ப்பு": {}
      },
      "decorators : decorator +": {
        "பெயர்ப்பு": {}
      },
      "decorated : decorators ( classdef | funcdef | async_funcdef )": {
        "பெயர்ப்பு": {}
      },
      "async_funcdef : \\"async\\" funcdef": {
        "பெயர்ப்பு": {}
      },
      "funcdef : \\"நிரல்பாகம்\\" NAME \\"(\\" parameters ? \\")\\" suite \\"முடி\\"": {
        "பெயர்ப்பு": {}
      },
      "!parameters : paramvalue ( \\",\\" paramvalue ) * [ \\",\\" [ starparams | kwparams ] ] \\n          | starparams \\n          | kwparams": {
        "பெயர்ப்பு": {}
      },
      "starparams : \\"*\\" typedparam ? ( \\",\\" paramvalue ) * [ \\",\\" kwparams ]": {
        "பெயர்ப்பு": {}
      },
      "kwparams : \\"**\\" typedparam": {
        "பெயர்ப்பு": {}
      },
      "?paramvalue : typedparam [ \\"=\\" test ]": {
        "பெயர்ப்பு": {}
      },
      "?typedparam : NAME [ \\":\\" test ]": {
        "பெயர்ப்பு": {}
      },
      "!varargslist : ( vfpdef [ \\"=\\" test ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"*\\" [ vfpdef ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"**\\" vfpdef [ \\",\\" ] ] ] | \\"**\\" vfpdef [ \\",\\" ] ] ] \\n  | \\"*\\" [ vfpdef ] ( \\",\\" vfpdef [ \\"=\\" test ] ) * [ \\",\\" [ \\"**\\" vfpdef [ \\",\\" ] ] ] \\n  | \\"**\\" vfpdef [ \\",\\" ] )": {
        "பெயர்ப்பு": {}
      },
      "vfpdef : NAME": {
        "பெயர்ப்பு": {}
      },
      "?stmt : simple_stmt | compound_stmt": {
        "பெயர்ப்பு": {}
      },
      "!?simple_stmt : small_stmt ( \\";\\" small_stmt ) * [ \\";\\" ] NEWLINE": {
        "பெயர்ப்பு": {}
      },
      "?small_stmt : ( expr_stmt | del_stmt | pass_stmt | print_stmt | flow_stmt | import_stmt | global_stmt | nonlocal_stmt | assert_stmt )": {
        "பெயர்ப்பு": {}
      },
      "?expr_stmt : testlist_star_expr ( annassign | augassign ( yield_expr | testlist ) \\n         | ( \\"=\\" ( yield_expr | testlist_star_expr ) ) * )": {
        "பெயர்ப்பு": {}
      },
      "annassign : \\":\\" test [ \\"=\\" test ]": {
        "பெயர்ப்பு": {}
      },
      "!?testlist_star_expr : ( test | star_expr ) ( \\",\\" ( test | star_expr ) ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "!augassign : ( \\"+=\\" | \\"-=\\" | \\"*=\\" | \\"@=\\" | \\"/=\\" | \\"%=\\" | \\"&=\\" | \\"|=\\" | \\"^=\\" | \\"<<=\\" | \\">>=\\" | \\"**=\\" | \\"//=\\" )": {
        "பெயர்ப்பு": {}
      },
      "print_stmt : \\"பதிப்பி\\" [ test ( \\",\\" test ) * [ \\",\\" ] ]": {
        "பெயர்ப்பு": {}
      },
      "del_stmt : \\"del\\" exprlist": {
        "பெயர்ப்பு": {}
      },
      "pass_stmt : \\"pass\\"": {
        "பெயர்ப்பு": {}
      },
      "flow_stmt : break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt": {
        "பெயர்ப்பு": {}
      },
      "break_stmt : \\"நிறுத்து\\"": {
        "பெயர்ப்பு": {}
      },
      "continue_stmt : \\"தொடர்\\"": {
        "பெயர்ப்பு": {}
      },
      "return_stmt : \\"நிரல்பாகம்\\" [ testlist ]": {
        "பெயர்ப்பு": {}
      },
      "yield_stmt : yield_expr": {
        "பெயர்ப்பு": {}
      },
      "raise_stmt : \\"raise\\" [ test [ \\"from\\" test ] ]": {
        "பெயர்ப்பு": {}
      },
      "import_stmt : import_name | import_from": {
        "பெயர்ப்பு": {}
      },
      "import_name : \\"import\\" dotted_as_names": {
        "பெயர்ப்பு": {}
      },
      "import_from : \\"from\\" ( dots ? dotted_name | dots ) \\"import\\" ( \\"*\\" | \\"(\\" import_as_names \\")\\" | import_as_names )": {
        "பெயர்ப்பு": {}
      },
      "!dots : \\".\\" +": {
        "பெயர்ப்பு": {}
      },
      "import_as_name : NAME [ \\"as\\" NAME ]": {
        "பெயர்ப்பு": {}
      },
      "dotted_as_name : dotted_name [ \\"as\\" NAME ]": {
        "பெயர்ப்பு": {}
      },
      "!import_as_names : import_as_name ( \\",\\" import_as_name ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "dotted_as_names : dotted_as_name ( \\",\\" dotted_as_name ) *": {
        "பெயர்ப்பு": {}
      },
      "dotted_name : NAME ( \\".\\" NAME ) *": {
        "பெயர்ப்பு": {}
      },
      "global_stmt : \\"global\\" NAME ( \\",\\" NAME ) *": {
        "பெயர்ப்பு": {}
      },
      "nonlocal_stmt : \\"nonlocal\\" NAME ( \\",\\" NAME ) *": {
        "பெயர்ப்பு": {}
      },
      "assert_stmt : \\"assert\\" test [ \\",\\" test ]": {
        "பெயர்ப்பு": {}
      },
      "compound_stmt : if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef | decorated | async_stmt": {
        "பெயர்ப்பு": {}
      },
      "async_stmt : \\"async\\" ( funcdef | with_stmt | for_stmt )": {
        "பெயர்ப்பு": {}
      },
      "if_stmt : \\"@\\" \\"(\\" test \\")\\" \\"ஆனால்\\" suite ( \\"@\\" \\"(\\" test \\")\\" \\"இல்லைஆனால்\\" suite ) * [ \\"இல்லை\\" suite ] \\"முடி\\"": {
        "பெயர்ப்பு": {}
      },
      "while_stmt : \\"while\\" test \\":\\" suite [ \\"else\\" \\":\\" suite ]": {
        "பெயர்ப்பு": {}
      },
      "for_stmt : \\"@\\" \\"(\\" exprlist \\")\\" \\"ஆக\\" testlist \\":\\" suite [ \\"else\\" \\":\\" suite ]": {
        "பெயர்ப்பு": {}
      },
      "try_stmt : ( \\"try\\" \\":\\" suite ( ( except_clause \\":\\" suite ) + [ \\"else\\" \\":\\" suite ] [ \\"finally\\" \\":\\" suite ] | \\"finally\\" \\":\\" suite ) )": {
        "பெயர்ப்பு": {}
      },
      "with_stmt : \\"with\\" with_item ( \\",\\" with_item ) * \\":\\" suite": {
        "பெயர்ப்பு": {}
      },
      "with_item : test [ \\"as\\" expr ]": {
        "பெயர்ப்பு": {}
      },
      "except_clause : \\"except\\" [ test [ \\"as\\" NAME ] ]": {
        "பெயர்ப்பு": {}
      },
      "suite : simple_stmt | NEWLINE INDENT stmt + DEDENT": {
        "பெயர்ப்பு": {}
      },
      "?test : or_test [ \\"if\\" or_test \\"else\\" test ] | lambdef": {
        "பெயர்ப்பு": {}
      },
      "?test_nocond : or_test | lambdef_nocond": {
        "பெயர்ப்பு": {}
      },
      "lambdef : \\"lambda\\" [ varargslist ] \\":\\" test": {
        "பெயர்ப்பு": {}
      },
      "lambdef_nocond : \\"lambda\\" [ varargslist ] \\":\\" test_nocond": {
        "பெயர்ப்பு": {}
      },
      "?or_test : and_test ( \\"or\\" and_test ) *": {
        "பெயர்ப்பு": {}
      },
      "?and_test : not_test ( \\"and\\" not_test ) *": {
        "பெயர்ப்பு": {}
      },
      "?not_test : \\"not\\" not_test -> not \\n         | comparison": {
        "பெயர்ப்பு": {}
      },
      "?comparison : expr ( _comp_op expr ) *": {
        "பெயர்ப்பு": {}
      },
      "star_expr : \\"*\\" expr": {
        "பெயர்ப்பு": {}
      },
      "?expr : xor_expr ( \\"|\\" xor_expr ) *": {
        "பெயர்ப்பு": {}
      },
      "?xor_expr : and_expr ( \\"^\\" and_expr ) *": {
        "பெயர்ப்பு": {}
      },
      "?and_expr : shift_expr ( \\"&\\" shift_expr ) *": {
        "பெயர்ப்பு": {}
      },
      "?shift_expr : arith_expr ( _shift_op arith_expr ) *": {
        "பெயர்ப்பு": {}
      },
      "?arith_expr : term ( _add_op term ) *": {
        "பெயர்ப்பு": {}
      },
      "?term : factor ( _mul_op factor ) *": {
        "பெயர்ப்பு": {}
      },
      "?factor : _factor_op factor | power": {
        "பெயர்ப்பு": {}
      },
      "!_factor_op : \\"+\\" | \\"-\\" | \\"~\\"": {
        "பெயர்ப்பு": {}
      },
      "!_add_op : \\"+\\" | \\"-\\"": {
        "பெயர்ப்பு": {}
      },
      "!_shift_op : \\"<<\\" | \\">>\\"": {
        "பெயர்ப்பு": {}
      },
      "!_mul_op : \\"*\\" | \\"@\\" | \\"/\\" | \\"%\\" | \\"//\\"": {
        "பெயர்ப்பு": {}
      },
      "!_comp_op : \\"<\\" | \\">\\" | \\"==\\" | \\">=\\" | \\"<=\\" | \\"<>\\" | \\"!=\\" | \\"in\\" | \\"not\\" \\"in\\" | \\"is\\" | \\"is\\" \\"not\\"": {
        "பெயர்ப்பு": {}
      },
      "?power : await_expr [ \\"**\\" factor ]": {
        "பெயர்ப்பு": {}
      },
      "?await_expr : [ \\"await\\" ] atom_expr": {
        "பெயர்ப்பு": {}
      },
      "?atom_expr : atom_expr \\"(\\" [ arguments ] \\")\\" -> funccall \\n          | atom_expr \\"[\\" subscriptlist \\"]\\" -> getitem \\n          | atom_expr \\".\\" NAME -> getattr \\n          | atom": {
        "பெயர்ப்பு": {}
      },
      "?atom : \\"(\\" [ yield_expr | testlist_comp ] \\")\\" -> tuple \\n     | \\"[\\" [ testlist_comp ] \\"]\\" -> list \\n     | \\"{\\" [ dictorsetmaker ] \\"}\\" -> dict \\n     | NAME -> var \\n     | number | string + \\n     | \\"(\\" test \\")\\" -> par_group \\n     | \\"...\\" -> ellipsis \\n     | \\"None\\" -> const_none \\n     | \\"True\\" -> const_true \\n     | \\"False\\" -> const_false": {
        "பெயர்ப்பு": {}
      },
      "!?testlist_comp : ( test | star_expr ) [ comp_for | ( \\",\\" ( test | star_expr ) ) + [ \\",\\" ] | \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "!subscriptlist : subscript ( \\",\\" subscript ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "subscript : test | [ test ] \\":\\" [ test ] [ sliceop ]": {
        "பெயர்ப்பு": {}
      },
      "sliceop : \\":\\" [ test ]": {
        "பெயர்ப்பு": {}
      },
      "!exprlist : ( expr | star_expr ) ( \\",\\" ( expr | star_expr ) ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "!testlist : test ( \\",\\" test ) * [ \\",\\" ]": {
        "பெயர்ப்பு": {}
      },
      "!dictorsetmaker : ( ( ( test \\":\\" test | \\"**\\" expr ) ( comp_for | ( \\",\\" ( test \\":\\" test | \\"**\\" expr ) ) * [ \\",\\" ] ) ) | ( ( test | star_expr ) ( comp_for | ( \\",\\" ( test | star_expr ) ) * [ \\",\\" ] ) ) )": {
        "பெயர்ப்பு": {}
      },
      "classdef : \\"class\\" NAME [ \\"(\\" [ arguments ] \\")\\" ] \\":\\" suite": {
        "பெயர்ப்பு": {}
      },
      "!arguments : argvalue ( \\",\\" argvalue ) * [ \\",\\" [ starargs | kwargs ] ] \\n         | starargs \\n         | kwargs \\n         | test comp_for": {
        "பெயர்ப்பு": {}
      },
      "!starargs : \\"*\\" test ( \\",\\" \\"*\\" test ) * ( \\",\\" argvalue ) * [ \\",\\" kwargs ]": {
        "பெயர்ப்பு": {}
      },
      "kwargs : \\"**\\" test": {
        "பெயர்ப்பு": {}
      },
      "?argvalue : test [ \\"=\\" test ]": {
        "பெயர்ப்பு": {}
      },
      "comp_iter : comp_for | comp_if | async_for": {
        "பெயர்ப்பு": {}
      },
      "async_for : \\"async\\" \\"for\\" exprlist \\"in\\" or_test [ comp_iter ]": {
        "பெயர்ப்பு": {}
      },
      "comp_for : \\"for\\" exprlist \\"in\\" or_test [ comp_iter ]": {
        "பெயர்ப்பு": {}
      },
      "comp_if : \\"if\\" test_nocond [ comp_iter ]": {
        "பெயர்ப்பு": {}
      },
      "encoding_decl : NAME": {
        "பெயர்ப்பு": {}
      },
      "yield_expr : \\"yield\\" [ yield_arg ]": {
        "பெயர்ப்பு": {}
      },
      "yield_arg : \\"from\\" test | testlist": {
        "பெயர்ப்பு": {}
      },
      "number : DEC_NUMBER | HEX_NUMBER | OCT_NUMBER | FLOAT_NUMBER | IMAG_NUMBER": {
        "பெயர்ப்பு": {}
      },
      "string : STRING | LONG_STRING": {
        "பெயர்ப்பு": {}
      },
      "COMMENT : /#[^\\\\n]*/": {
        "பெயர்ப்பு": {}
      },
      "NEWLINE : ( /\\\\r?\\\\n[\\\\t ]*/ | COMMENT ) +": {
        "பெயர்ப்பு": {}
      },
      "STRING : /[ubf]?r?(\\"(?!\\"\\").*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?\\"|'(?!'').*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?')/i": {
        "பெயர்ப்பு": {}
      },
      "LONG_STRING : /[ubf]?r?(\\"\\"\\".*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?\\"\\"\\"|'''.*?(?<!\\\\\\\\)(\\\\\\\\\\\\\\\\)*?''')/is": {
        "பெயர்ப்பு": {}
      },
      "HEX_NUMBER . 2 : /0x[\\\\da-f]*/i": {
        "பெயர்ப்பு": {}
      },
      "OCT_NUMBER . 2 : /0o[0-7]*/i": {
        "பெயர்ப்பு": {}
      },
      "BIN_NUMBER . 2 : /0b[0-1]*/i": {
        "பெயர்ப்பு": {}
      },
      "FLOAT_NUMBER . 2 : /((\\\\d+\\\\.\\\\d*|\\\\.\\\\d+)(e[-+]?\\\\d+)?|\\\\d+(e[-+]?\\\\d+))/i": {
        "பெயர்ப்பு": {}
      },
      "IMAG_NUMBER . 2 : /\\\\d+j|${FLOAT_NUMBER}j/i": {
        "பெயர்ப்பு": {}
      },
      "%ignore /[\\\\t \\\\f]+/": {
        "பெயர்ப்பு": {}
      },
      "%ignore /\\\\\\\\[\\\\t \\\\f]*\\\\r?\\\\n/": {
        "பெயர்ப்பு": {}
      },
      "%ignore COMMENT": {
        "பெயர்ப்பு": {}
      },
      "%declare INDENT DEDENT": {
        "பெயர்ப்பு": {}
      }
    },
    "மொழிபெயர்ப்பாளர்கள்": []
  }
}"""