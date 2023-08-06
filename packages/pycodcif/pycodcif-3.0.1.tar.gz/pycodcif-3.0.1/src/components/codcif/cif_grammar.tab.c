/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison implementation for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "3.0.4"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1


/* Substitute the variable and function names.  */
#define yyparse         cifparse
#define yylex           ciflex
#define yyerror         ciferror
#define yydebug         cifdebug
#define yynerrs         cifnerrs

#define yylval          ciflval
#define yychar          cifchar

/* Copy the first part of user declarations.  */
#line 8 "cif_grammar.y" /* yacc.c:339  */

/* exports: */
#include <cif_grammar_y.h>

/* uses: */
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <cexceptions.h>
#include <cxprintf.h>
#include <allocx.h>
#include <stringx.h>
#include <stdiox.h>
#include <cif_grammar_flex.h>
#include <yy.h>
#include <cif_lexer.h>
#include <cif_compiler.h>
#include <cif_lex_buffer.h>
#include <assert.h>
#include <common.h>

static CIF_COMPILER * volatile cif_cc; /* CIF current compiler */

static cexception_t *px; /* parser exception */

static typed_value *typed_value_from_value( CIFVALUE *v, cexception_t *ex );

#line 102 "cif_grammar.tab.c" /* yacc.c:339  */

# ifndef YY_NULLPTR
#  if defined __cplusplus && 201103L <= __cplusplus
#   define YY_NULLPTR nullptr
#  else
#   define YY_NULLPTR 0
#  endif
# endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 0
#endif

/* In a future release of Bison, this section will be replaced
   by #include "cif_grammar.tab.h".  */
#ifndef YY_CIF_CIF_GRAMMAR_TAB_H_INCLUDED
# define YY_CIF_CIF_GRAMMAR_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int cifdebug;
#endif
/* "%code requires" blocks.  */
#line 36 "cif_grammar.y" /* yacc.c:355  */

    #include <cif_compiler.h>

#line 136 "cif_grammar.tab.c" /* yacc.c:355  */

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    _DATA_ = 258,
    _SAVE_HEAD = 259,
    _SAVE_FOOT = 260,
    _TAG = 261,
    _LOOP_ = 262,
    _DQSTRING = 263,
    _SQSTRING = 264,
    _UQSTRING = 265,
    _TEXT_FIELD = 266,
    _INTEGER_CONST = 267,
    _REAL_CONST = 268
  };
#endif
/* Tokens.  */
#define _DATA_ 258
#define _SAVE_HEAD 259
#define _SAVE_FOOT 260
#define _TAG 261
#define _LOOP_ 262
#define _DQSTRING 263
#define _SQSTRING 264
#define _UQSTRING 265
#define _TEXT_FIELD 266
#define _INTEGER_CONST 267
#define _REAL_CONST 268

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED

union YYSTYPE
{
#line 40 "cif_grammar.y" /* yacc.c:355  */

    char *s;
    typed_value *typed_value;

#line 179 "cif_grammar.tab.c" /* yacc.c:355  */
};

typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE ciflval;

int cifparse (void);

#endif /* !YY_CIF_CIF_GRAMMAR_TAB_H_INCLUDED  */

/* Copy the second part of user declarations.  */

#line 196 "cif_grammar.tab.c" /* yacc.c:358  */

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif

#ifndef YY_ATTRIBUTE
# if (defined __GNUC__                                               \
      && (2 < __GNUC__ || (__GNUC__ == 2 && 96 <= __GNUC_MINOR__)))  \
     || defined __SUNPRO_C && 0x5110 <= __SUNPRO_C
#  define YY_ATTRIBUTE(Spec) __attribute__(Spec)
# else
#  define YY_ATTRIBUTE(Spec) /* empty */
# endif
#endif

#ifndef YY_ATTRIBUTE_PURE
# define YY_ATTRIBUTE_PURE   YY_ATTRIBUTE ((__pure__))
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# define YY_ATTRIBUTE_UNUSED YY_ATTRIBUTE ((__unused__))
#endif

#if !defined _Noreturn \
     && (!defined __STDC_VERSION__ || __STDC_VERSION__ < 201112)
# if defined _MSC_VER && 1200 <= _MSC_VER
#  define _Noreturn __declspec (noreturn)
# else
#  define _Noreturn YY_ATTRIBUTE ((__noreturn__))
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(E) ((void) (E))
#else
# define YYUSE(E) /* empty */
#endif

#if defined __GNUC__ && 407 <= __GNUC__ * 100 + __GNUC_MINOR__
/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN \
    _Pragma ("GCC diagnostic push") \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")\
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# define YY_IGNORE_MAYBE_UNINITIALIZED_END \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif


#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYSIZE_T yynewbytes;                                            \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / sizeof (*yyptr);                          \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, (Count) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYSIZE_T yyi;                         \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  31
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   58

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  14
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  24
/* YYNRULES -- Number of rules.  */
#define YYNRULES  47
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  53

/* YYTRANSLATE[YYX] -- Symbol number corresponding to YYX as returned
   by yylex, with out-of-bounds checking.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   268

#define YYTRANSLATE(YYX)                                                \
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, without out-of-bounds checking.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13
};

#if YYDEBUG
  /* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,    66,    66,    68,    69,    70,    71,    72,    76,    91,
     115,   116,   120,   137,   136,   156,   157,   161,   162,   166,
     171,   208,   209,   214,   215,   219,   220,   224,   232,   273,
     274,   308,   307,   336,   347,   361,   369,   381,   380,   394,
     395,   396,   400,   404,   408,   415,   468,   470
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || 0
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "_DATA_", "_SAVE_HEAD", "_SAVE_FOOT",
  "_TAG", "_LOOP_", "_DQSTRING", "_SQSTRING", "_UQSTRING", "_TEXT_FIELD",
  "_INTEGER_CONST", "_REAL_CONST", "$accept", "cif_file",
  "stray_cif_value_list", "data_block_list", "headerless_data_block",
  "$@1", "data_block", "data_item_list", "data_block_head", "data_item",
  "save_item_list", "save_item", "cif_entry", "cif_value_list", "loop",
  "$@2", "loop_tags", "loop_values", "save_block", "$@3", "cif_value",
  "string", "textfield", "number", YY_NULLPTR
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[NUM] -- (External) token number corresponding to the
   (internal) symbol number NUM (which must be that of a token).  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268
};
# endif

#define YYPACT_NINF -25

#define yypact_value_is_default(Yystate) \
  (!!((Yystate) == (-25)))

#define YYTABLE_NINF -13

#define yytable_value_is_error(Yytable_value) \
  0

  /* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
     STATE-NUM.  */
static const yytype_int8 yypact[] =
{
       2,    43,   -25,    43,   -25,   -25,   -25,   -25,   -25,   -25,
     -25,     7,    31,    31,    31,   -25,    33,    45,   -25,   -25,
     -25,   -25,    43,   -25,   -25,   -25,    43,   -25,    51,    43,
      16,   -25,    31,   -25,    31,    33,   -25,    33,    43,   -25,
      13,   -25,    43,   -25,    19,   -25,    33,   -25,   -25,   -25,
      43,   -25,   -25
};

  /* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
     Performed when YYTABLE does not specify something else to do.  Zero
     means the default is an error.  */
static const yytype_uint8 yydefact[] =
{
       2,    19,    37,     0,    31,    43,    42,    44,    45,    47,
      46,     0,     6,     3,     4,    11,    16,    13,    21,    25,
      26,    22,     8,    39,    41,    40,    20,    29,     0,    27,
       0,     1,     7,    10,     5,    15,    18,     0,     9,    30,
       0,    24,    28,    34,     0,    17,    14,    38,    23,    33,
      32,    36,    35
};

  /* YYPGOTO[NTERM-NUM].  */
static const yytype_int8 yypgoto[] =
{
     -25,   -25,   -25,    21,   -25,   -25,   -11,     4,   -25,     1,
     -25,   -24,   -25,    -5,   -25,   -25,   -25,   -25,   -25,   -25,
       0,   -25,   -25,   -25
};

  /* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int8 yydefgoto[] =
{
      -1,    11,    12,    13,    14,    37,    15,    35,    16,    36,
      40,    18,    19,    26,    20,    30,    44,    50,    21,    28,
      27,    23,    24,    25
};

  /* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
     positive, shift that token.  If negative, reduce the rule whose
     number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int8 yytable[] =
{
      22,    17,    33,    29,    41,     1,     2,    31,     3,     4,
       5,     6,     7,     8,     9,    10,    48,    38,    47,     3,
       4,    33,    43,    33,    42,    49,    39,     5,     6,     7,
       8,     9,    10,    32,     1,    34,    45,     2,    39,     3,
       4,    46,    39,     0,    51,   -12,     0,    45,   -12,     0,
      52,     5,     6,     7,     8,     9,    10,     3,     4
};

static const yytype_int8 yycheck[] =
{
       0,     0,    13,     3,    28,     3,     4,     0,     6,     7,
       8,     9,    10,    11,    12,    13,    40,    22,     5,     6,
       7,    32,     6,    34,    29,     6,    26,     8,     9,    10,
      11,    12,    13,    12,     3,    14,    35,     4,    38,     6,
       7,    37,    42,    -1,    44,     0,    -1,    46,     3,    -1,
      50,     8,     9,    10,    11,    12,    13,     6,     7
};

  /* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
     symbol of state STATE-NUM.  */
static const yytype_uint8 yystos[] =
{
       0,     3,     4,     6,     7,     8,     9,    10,    11,    12,
      13,    15,    16,    17,    18,    20,    22,    23,    25,    26,
      28,    32,    34,    35,    36,    37,    27,    34,    33,    34,
      29,     0,    17,    20,    17,    21,    23,    19,    27,    34,
      24,    25,    27,     6,    30,    23,    21,     5,    25,     6,
      31,    34,    34
};

  /* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint8 yyr1[] =
{
       0,    14,    15,    15,    15,    15,    15,    15,    16,    16,
      17,    17,    18,    19,    18,    20,    20,    21,    21,    22,
      22,    23,    23,    24,    24,    25,    25,    26,    26,    27,
      27,    29,    28,    30,    30,    31,    31,    33,    32,    34,
      34,    34,    35,    35,    35,    36,    37,    37
};

  /* YYR2[YYN] -- Number of symbols on the right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     0,     1,     1,     2,     1,     2,     1,     2,
       2,     1,     1,     0,     3,     2,     1,     2,     1,     1,
       2,     1,     1,     2,     1,     1,     1,     2,     3,     1,
       2,     0,     4,     2,     1,     2,     1,     0,     4,     1,
       1,     1,     1,     1,     1,     1,     1,     1
};


#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)
#define YYEMPTY         (-2)
#define YYEOF           0

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                  \
do                                                              \
  if (yychar == YYEMPTY)                                        \
    {                                                           \
      yychar = (Token);                                         \
      yylval = (Value);                                         \
      YYPOPSTACK (yylen);                                       \
      yystate = *yyssp;                                         \
      goto yybackup;                                            \
    }                                                           \
  else                                                          \
    {                                                           \
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;                                                  \
    }                                                           \
while (0)

/* Error token number */
#define YYTERROR        1
#define YYERRCODE       256



/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)

/* This macro is provided for backward compatibility. */
#ifndef YY_LOCATION_PRINT
# define YY_LOCATION_PRINT(File, Loc) ((void) 0)
#endif


# define YY_SYMBOL_PRINT(Title, Type, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Type, Value); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*----------------------------------------.
| Print this symbol's value on YYOUTPUT.  |
`----------------------------------------*/

static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
{
  FILE *yyo = yyoutput;
  YYUSE (yyo);
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# endif
  YYUSE (yytype);
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
{
  YYFPRINTF (yyoutput, "%s %s (",
             yytype < YYNTOKENS ? "token" : "nterm", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yytype_int16 *yybottom, yytype_int16 *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yytype_int16 *yyssp, YYSTYPE *yyvsp, int yyrule)
{
  unsigned long int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       yystos[yyssp[yyi + 1 - yynrhs]],
                       &(yyvsp[(yyi + 1) - (yynrhs)])
                                              );
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif


#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
static YYSIZE_T
yystrlen (const char *yystr)
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
static char *
yystpcpy (char *yydest, const char *yysrc)
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
        switch (*++yyp)
          {
          case '\'':
          case ',':
            goto do_not_strip_quotes;

          case '\\':
            if (*++yyp != '\\')
              goto do_not_strip_quotes;
            /* Fall through.  */
          default:
            if (yyres)
              yyres[yyn] = *yyp;
            yyn++;
            break;

          case '"':
            if (yyres)
              yyres[yyn] = '\0';
            return yyn;
          }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into *YYMSG, which is of size *YYMSG_ALLOC, an error message
   about the unexpected token YYTOKEN for the state stack whose top is
   YYSSP.

   Return 0 if *YYMSG was successfully written.  Return 1 if *YYMSG is
   not large enough to hold the message.  In that case, also set
   *YYMSG_ALLOC to the required number of bytes.  Return 2 if the
   required number of bytes is too large to store.  */
static int
yysyntax_error (YYSIZE_T *yymsg_alloc, char **yymsg,
                yytype_int16 *yyssp, int yytoken)
{
  YYSIZE_T yysize0 = yytnamerr (YY_NULLPTR, yytname[yytoken]);
  YYSIZE_T yysize = yysize0;
  enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
  /* Internationalized format string. */
  const char *yyformat = YY_NULLPTR;
  /* Arguments of yyformat. */
  char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
  /* Number of reported tokens (one for the "unexpected", one per
     "expected"). */
  int yycount = 0;

  /* There are many possibilities here to consider:
     - If this state is a consistent state with a default action, then
       the only way this function was invoked is if the default action
       is an error action.  In that case, don't check for expected
       tokens because there are none.
     - The only way there can be no lookahead present (in yychar) is if
       this state is a consistent state with a default action.  Thus,
       detecting the absence of a lookahead is sufficient to determine
       that there is no unexpected or expected token to report.  In that
       case, just report a simple "syntax error".
     - Don't assume there isn't a lookahead just because this state is a
       consistent state with a default action.  There might have been a
       previous inconsistent state, consistent state with a non-default
       action, or user semantic action that manipulated yychar.
     - Of course, the expected token list depends on states to have
       correct lookahead information, and it depends on the parser not
       to perform extra reductions after fetching a lookahead from the
       scanner and before detecting a syntax error.  Thus, state merging
       (from LALR or IELR) and default reductions corrupt the expected
       token list.  However, the list is correct for canonical LR with
       one exception: it will still contain any token that will not be
       accepted due to an error action in a later state.
  */
  if (yytoken != YYEMPTY)
    {
      int yyn = yypact[*yyssp];
      yyarg[yycount++] = yytname[yytoken];
      if (!yypact_value_is_default (yyn))
        {
          /* Start YYX at -YYN if negative to avoid negative indexes in
             YYCHECK.  In other words, skip the first -YYN actions for
             this state because they are default actions.  */
          int yyxbegin = yyn < 0 ? -yyn : 0;
          /* Stay within bounds of both yycheck and yytname.  */
          int yychecklim = YYLAST - yyn + 1;
          int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
          int yyx;

          for (yyx = yyxbegin; yyx < yyxend; ++yyx)
            if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR
                && !yytable_value_is_error (yytable[yyx + yyn]))
              {
                if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                  {
                    yycount = 1;
                    yysize = yysize0;
                    break;
                  }
                yyarg[yycount++] = yytname[yyx];
                {
                  YYSIZE_T yysize1 = yysize + yytnamerr (YY_NULLPTR, yytname[yyx]);
                  if (! (yysize <= yysize1
                         && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
                    return 2;
                  yysize = yysize1;
                }
              }
        }
    }

  switch (yycount)
    {
# define YYCASE_(N, S)                      \
      case N:                               \
        yyformat = S;                       \
      break
      YYCASE_(0, YY_("syntax error"));
      YYCASE_(1, YY_("syntax error, unexpected %s"));
      YYCASE_(2, YY_("syntax error, unexpected %s, expecting %s"));
      YYCASE_(3, YY_("syntax error, unexpected %s, expecting %s or %s"));
      YYCASE_(4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
      YYCASE_(5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
# undef YYCASE_
    }

  {
    YYSIZE_T yysize1 = yysize + yystrlen (yyformat);
    if (! (yysize <= yysize1 && yysize1 <= YYSTACK_ALLOC_MAXIMUM))
      return 2;
    yysize = yysize1;
  }

  if (*yymsg_alloc < yysize)
    {
      *yymsg_alloc = 2 * yysize;
      if (! (yysize <= *yymsg_alloc
             && *yymsg_alloc <= YYSTACK_ALLOC_MAXIMUM))
        *yymsg_alloc = YYSTACK_ALLOC_MAXIMUM;
      return 1;
    }

  /* Avoid sprintf, as that infringes on the user's name space.
     Don't have undefined behavior even if the translation
     produced a string with the wrong number of "%s"s.  */
  {
    char *yyp = *yymsg;
    int yyi = 0;
    while ((*yyp = *yyformat) != '\0')
      if (*yyp == '%' && yyformat[1] == 's' && yyi < yycount)
        {
          yyp += yytnamerr (yyp, yyarg[yyi++]);
          yyformat += 2;
        }
      else
        {
          yyp++;
          yyformat++;
        }
  }
  return 0;
}
#endif /* YYERROR_VERBOSE */

/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
{
  YYUSE (yyvaluep);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YYUSE (yytype);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}




/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;


/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       'yyss': related to states.
       'yyvs': related to semantic values.

       Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yytype_int16 yyssa[YYINITDEPTH];
    yytype_int16 *yyss;
    yytype_int16 *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken = 0;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yyssp = yyss = yyssa;
  yyvsp = yyvs = yyvsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */
  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        YYSTYPE *yyvs1 = yyvs;
        yytype_int16 *yyss1 = yyss;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * sizeof (*yyssp),
                    &yyvs1, yysize * sizeof (*yyvsp),
                    &yystacksize);

        yyss = yyss1;
        yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yytype_int16 *yyss1 = yyss;
        union yyalloc *yyptr =
          (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
        if (! yyptr)
          goto yyexhaustedlab;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
                  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token.  */
  yychar = YYEMPTY;

  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 8:
#line 77 "cif_grammar.y" /* yacc.c:1646  */
    {
            if( isset_fix_errors( cif_cc ) ||
                isset_fix_data_header( cif_cc ) ) {
                    print_message( cif_cc, "WARNING", "stray CIF values at the "
                                   "beginning of the input file", "",
                                   typed_value_line( (yyvsp[0].typed_value) ), -1, px );
            } else {
                    print_message( cif_cc, "ERROR", "stray CIF values at the "
                                   "beginning of the input file", "",
                                   typed_value_line( (yyvsp[0].typed_value) ), -1, px );
                    cif_compiler_increase_nerrors( cif_cc );
            }
            delete_typed_value( (yyvsp[0].typed_value) );
        }
#line 1323 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 9:
#line 92 "cif_grammar.y" /* yacc.c:1646  */
    {
            if( isset_fix_errors( cif_cc ) ||
                isset_fix_data_header( cif_cc ) ) {
                    print_message( cif_cc, "WARNING", "stray CIF values at the "
                                   "beginning of the input file", "",
                                   typed_value_line( (yyvsp[-1].typed_value) ), -1, px );
            } else {
                    print_message( cif_cc, "ERROR", "stray CIF values at the "
                                   "beginning of the input file", "",
                                   typed_value_line( (yyvsp[-1].typed_value) ), -1, px );
                    cif_compiler_increase_nerrors( cif_cc );
            }
            delete_typed_value( (yyvsp[-1].typed_value) );
            delete_typed_value( (yyvsp[0].typed_value) );
        }
#line 1343 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 12:
#line 121 "cif_grammar.y" /* yacc.c:1646  */
    {
            if( isset_fix_errors( cif_cc ) ||
                isset_fix_data_header( cif_cc ) ) {
                    print_message( cif_cc, 
                              "WARNING", "no data block heading " 
                              "(i.e. data_somecif) found", "",
                              cif_flex_previous_line_number(), -1, px );
            } else {
                    print_message( cif_cc, 
                              "ERROR", "no data block heading "
                              "(i.e. data_somecif) found", "",
                              cif_flex_previous_line_number(), -1, px );
                    cif_compiler_increase_nerrors( cif_cc );
            }
        }
#line 1363 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 13:
#line 137 "cif_grammar.y" /* yacc.c:1646  */
    {
            if( isset_fix_errors( cif_cc ) ||
                isset_fix_data_header( cif_cc ) ) {
                    print_message( cif_cc, 
                              "WARNING", "no data block heading " 
                              "(i.e. data_somecif) found", "",
                              cif_flex_previous_line_number(), -1, px );
            } else {
                    print_message( cif_cc, 
                              "ERROR", "no data block heading "
                              "(i.e. data_somecif) found", "",
                              cif_flex_previous_line_number(), -1, px );
                    cif_compiler_increase_nerrors( cif_cc );
            }
        }
#line 1383 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 19:
#line 167 "cif_grammar.y" /* yacc.c:1646  */
    {
            cif_start_datablock( cif_compiler_cif( cif_cc ), (yyvsp[0].s), px );
            freex( (yyvsp[0].s) );
        }
#line 1392 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 20:
#line 172 "cif_grammar.y" /* yacc.c:1646  */
    {
            if( isset_fix_errors( cif_cc ) ||
                isset_fix_string_quotes( cif_cc ) ||
                isset_fix_datablock_names( cif_cc ) ) {
                char buf[strlen((yyvsp[-1].s))+strlen(value_scalar(typed_value_value( (yyvsp[0].typed_value) )))+2];
                strcpy( buf, (yyvsp[-1].s) );
                buf[strlen((yyvsp[-1].s))] = '_';
                size_t i;
                for( i = 0; i < strlen(value_scalar(typed_value_value( (yyvsp[0].typed_value) ))); i++ ) {
                    if( value_scalar(typed_value_value( (yyvsp[0].typed_value) ))[i] != ' ' ) {
                        buf[strlen((yyvsp[-1].s))+1+i] = value_scalar(typed_value_value( (yyvsp[0].typed_value) ))[i];
                    } else {
                        buf[strlen((yyvsp[-1].s))+1+i] = '_';
                    } 
                }
                buf[strlen((yyvsp[-1].s))+strlen(value_scalar(typed_value_value( (yyvsp[0].typed_value) )))+1] = '\0';
                cif_start_datablock( cif_compiler_cif( cif_cc ), buf, px );
                if( isset_fix_errors( cif_cc ) ||
                    isset_fix_string_quotes( cif_cc ) ) {
                    yywarning_token( cif_cc, "the dataname apparently had spaces "
                                     "in it -- replaced spaces with underscores",
                                     typed_value_line( (yyvsp[0].typed_value) ), -1, px );
                }
            } else {
                cif_start_datablock( cif_compiler_cif( cif_cc ), (yyvsp[-1].s), px );
                yyerror_token( cif_cc, "incorrect CIF syntax",
                               typed_value_line( (yyvsp[0].typed_value) ),
                               typed_value_pos( (yyvsp[0].typed_value) )+1,
                               typed_value_content( (yyvsp[0].typed_value) ), px );
            }
            freex( (yyvsp[-1].s) );
            delete_typed_value( (yyvsp[0].typed_value) );
        }
#line 1430 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 27:
#line 225 "cif_grammar.y" /* yacc.c:1646  */
    {
            assert_datablock_exists( cif_cc, px );
            add_tag_value( cif_cc, (yyvsp[-1].s), (yyvsp[0].typed_value), px );
            freex( (yyvsp[-1].s) );
            typed_value_detach_value( (yyvsp[0].typed_value) ); // protecting v from free()ing
            delete_typed_value( (yyvsp[0].typed_value) );
        }
#line 1442 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 28:
#line 233 "cif_grammar.y" /* yacc.c:1646  */
    {
                assert_datablock_exists( cif_cc, px );
                if( isset_fix_errors( cif_cc ) ||
                    isset_fix_string_quotes( cif_cc ) ) {
                    yywarning_token( cif_cc, "string with spaces without quotes -- fixed",
                                     typed_value_line( (yyvsp[-1].typed_value) ), -1, px );
                    char *buf = mallocx(strlen(value_scalar(typed_value_value( (yyvsp[-1].typed_value) )))+
                                        strlen(value_scalar(typed_value_value( (yyvsp[0].typed_value) )))+2,px);
                    buf = strcpy( buf, value_scalar(typed_value_value( (yyvsp[-1].typed_value) )) );
                    buf = strcat( buf, " \0" );
                    buf = strcat( buf, value_scalar(typed_value_value( (yyvsp[0].typed_value) )) );
                    cif_value_type_t tag_type = CIF_SQSTRING;
                    if( index( buf, '\n' ) != NULL ||
                        index( buf, '\r' ) != NULL ||
                        index( buf, '\'' ) != NULL ||
                        index( buf, '\"' ) != NULL ) {
                        tag_type = CIF_TEXT;
                    }
                    typed_value *tv = new_typed_value( typed_value_line( (yyvsp[0].typed_value) ),
                                                       typed_value_pos( (yyvsp[0].typed_value) ),
                                                       typed_value_content( (yyvsp[0].typed_value) ),
                                                       new_value_from_scalar( buf, tag_type, px ) );
                    add_tag_value( cif_cc, (yyvsp[-2].s), tv, px );
                    typed_value_detach_value( tv );
                    delete_typed_value( tv );
                    typed_value_detach_content( (yyvsp[0].typed_value) ); /* preventing from free()ing
                                                         repeatedly */
                } else {
                    yyerror_token( cif_cc, "incorrect CIF syntax",
                                   typed_value_line( (yyvsp[0].typed_value) ),
                                   typed_value_pos( (yyvsp[0].typed_value) ) + 1,
                                   typed_value_content( (yyvsp[0].typed_value) ), px );
                }
                freex( (yyvsp[-2].s) );
                delete_typed_value( (yyvsp[-1].typed_value) );
                delete_typed_value( (yyvsp[0].typed_value) );
            }
#line 1484 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 30:
#line 275 "cif_grammar.y" /* yacc.c:1646  */
    {
            // Copying the whole $1 value each time a new value is
            // appended results in quadratic performance. Since the
            // code below works anyway only for broken CIFs where the
            // leading stray values will be discarded, we can afford
            // not to store the whole set of the non-CIF values before
            // the actual CIF after some threshold max_length. Such
            // limitation increases performance dramatically for large
            // files such as 'HETCOR_Ampicillin_1.25ms.txt' (4196446
            // words, 4194828 lines). All regression tests pass after
            // this change, demonstrating that the accumulated values
            // were not used in any tests and apparently there is no
            // pressing need to have them.
            const size_t max_length = 100;
            size_t len1 = strlen(value_scalar(typed_value_value( (yyvsp[-1].typed_value) )));
            size_t len2 = strlen(value_scalar(typed_value_value( (yyvsp[0].typed_value) )));
            size_t len = len1 < max_length ? len1 : max_length;
            char *buf = mallocx( len + len2 + 2, px );
            buf = strncpy( buf, value_scalar( typed_value_value( (yyvsp[-1].typed_value) ) ), len );
            buf[len] = '\0';
            buf = strcat( buf, " \0" );
            buf = strcat( buf, value_scalar( typed_value_value( (yyvsp[0].typed_value) ) ) );
            (yyval.typed_value) = new_typed_value( typed_value_line( (yyvsp[-1].typed_value) ),
                                  typed_value_pos( (yyvsp[-1].typed_value) ),
                                  strdupx( typed_value_content((yyvsp[-1].typed_value)), px ),
                                  new_value_from_scalar( buf, CIF_SQSTRING, px ) );
            delete_typed_value( (yyvsp[-1].typed_value) );
            delete_typed_value( (yyvsp[0].typed_value) );
        }
#line 1518 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 31:
#line 308 "cif_grammar.y" /* yacc.c:1646  */
    {
           assert_datablock_exists( cif_cc, px );
           cif_compiler_start_loop( cif_cc, cif_flex_current_line_number() );
           cif_start_loop( cif_compiler_cif( cif_cc ), px );
           freex( (yyvsp[0].s) );
       }
#line 1529 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 32:
#line 315 "cif_grammar.y" /* yacc.c:1646  */
    {
           if( cif_compiler_loop_value_count( cif_cc ) %
               cif_compiler_loop_tag_count( cif_cc ) != 0 ) {
               ciferror( cxprintf( "wrong number of elements in the "
                                  "loop starting at line %d",
                                   cif_compiler_loop_start_line( cif_cc ) ) );
#if 0
               if( cif_compiler_cif( cif_cc ) ) {
                   cif_set_yyretval( cif_compiler_cif( cif_cc ), -1 );
               }
               cexception_raise( px, CIF_UNRECOVERABLE_ERROR,
                   cxprintf( "wrong number of elements in the "
                             "loop starting at line %d",
                              cif_compiler_loop_start_line( cif_cc ) ) );
#endif
           }
           cif_finish_loop( cif_compiler_cif( cif_cc ), px );
       }
#line 1552 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 33:
#line 337 "cif_grammar.y" /* yacc.c:1646  */
    {
            ssize_t tag_nr = cif_tag_index( cif_compiler_cif( cif_cc ), (yyvsp[0].s) );
            if( tag_nr != -1 ) {
                yyerror_token( cif_cc, cxprintf( "tag %s appears more than once", (yyvsp[0].s) ),
                               cif_flex_current_line_number(), -1, NULL, px );
            }
            cif_compiler_increase_loop_tags( cif_cc );
            cif_insert_cifvalue( cif_compiler_cif( cif_cc ), (yyvsp[0].s), NULL, px );
            freex( (yyvsp[0].s) );
        }
#line 1567 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 34:
#line 348 "cif_grammar.y" /* yacc.c:1646  */
    {
            ssize_t tag_nr = cif_tag_index( cif_compiler_cif( cif_cc ), (yyvsp[0].s) );
            if( tag_nr != -1 ) {
                yyerror_token( cif_cc, cxprintf( "tag %s appears more than once", (yyvsp[0].s) ),
                               cif_flex_current_line_number(), -1, NULL, px );
            }
            cif_compiler_increase_loop_tags( cif_cc );
            cif_insert_cifvalue( cif_compiler_cif( cif_cc ), (yyvsp[0].s), NULL, px );
            freex( (yyvsp[0].s) );
        }
#line 1582 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 35:
#line 362 "cif_grammar.y" /* yacc.c:1646  */
    {
            cif_compiler_increase_loop_values( cif_cc );
            cif_push_loop_cifvalue( cif_compiler_cif( cif_cc ),
                                    typed_value_value( (yyvsp[0].typed_value) ), px );
            typed_value_detach_value( (yyvsp[0].typed_value) ); /* protecting v from free'ing */
            delete_typed_value( (yyvsp[0].typed_value) );
        }
#line 1594 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 36:
#line 370 "cif_grammar.y" /* yacc.c:1646  */
    {
            cif_compiler_increase_loop_values( cif_cc );
            cif_push_loop_cifvalue( cif_compiler_cif( cif_cc ),
                                    typed_value_value( (yyvsp[0].typed_value) ), px );
            typed_value_detach_value( (yyvsp[0].typed_value) ); /* protecting v from free'ing */
            delete_typed_value( (yyvsp[0].typed_value) );
        }
#line 1606 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 37:
#line 381 "cif_grammar.y" /* yacc.c:1646  */
    {
            assert_datablock_exists( cif_cc, px );
            cif_start_save_frame( cif_compiler_cif( cif_cc ), /* name = */ (yyvsp[0].s), px );
            freex( (yyvsp[0].s) );
        }
#line 1616 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 38:
#line 388 "cif_grammar.y" /* yacc.c:1646  */
    {
            cif_finish_save_frame( cif_compiler_cif( cif_cc ) );
        }
#line 1624 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 42:
#line 401 "cif_grammar.y" /* yacc.c:1646  */
    {
            (yyval.typed_value) = typed_value_from_value( new_value_from_scalar( (yyvsp[0].s), CIF_SQSTRING, px ), px );
        }
#line 1632 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 43:
#line 405 "cif_grammar.y" /* yacc.c:1646  */
    {
            (yyval.typed_value) = typed_value_from_value( new_value_from_scalar( (yyvsp[0].s), CIF_DQSTRING, px ), px );
        }
#line 1640 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 44:
#line 409 "cif_grammar.y" /* yacc.c:1646  */
    {
            (yyval.typed_value) = typed_value_from_value( new_value_from_scalar( (yyvsp[0].s), CIF_UQSTRING, px ), px );
        }
#line 1648 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 45:
#line 416 "cif_grammar.y" /* yacc.c:1646  */
    {
          char *text = (yyvsp[0].s);

          int unprefixed = 0;
          if( isset_do_not_unprefix_text( cif_cc ) == 0 ) {
              size_t str_len = strlen( text );
              char *unprefixed_text =
                    cif_unprefix_textfield( text );
              freex( text );
              text = unprefixed_text;
              if( str_len != strlen( unprefixed_text ) ) {
                  unprefixed = 1;
              }
          }
          int unfolded = 0;
          if( isset_do_not_unfold_text( cif_cc ) == 0 &&
              text[0] == '\\' ) {
              size_t str_len = strlen( text );
              char *unfolded_text =
                    cif_unfold_textfield( text );
              freex( text );
              text = unfolded_text;
              if( str_len != strlen( unfolded_text ) ) {
                  unfolded = 1;
              }
          }

        /*
         * Unprefixing transforms the first line to either "/\n" or "\n".
         * These symbols signal whether the processed text should be
         * unfolded or not (if the unfolding option is also set).
         * As a result, if the text was unprefixed, but not unfolded
         * an unnescessary empty line might occur at the begining of
         * the text field. This empty line should be removed.
         */
          if( unprefixed == 1 && unfolded == 0 ) {
              char *str = text;
              if( str[0] == '\n' ) {
                  size_t i = 0;
                  while( str[i] != '\0' ) {
                      str[i] = str[i+1];
                      i++;
                  }
                  str[i] = '\0';
              }
          }

          (yyval.typed_value) = typed_value_from_value( new_value_from_scalar( text, CIF_TEXT, px ), px );
        }
#line 1702 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 46:
#line 469 "cif_grammar.y" /* yacc.c:1646  */
    { (yyval.typed_value) = typed_value_from_value( new_value_from_scalar( (yyvsp[0].s), CIF_FLOAT, px ), px ); }
#line 1708 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;

  case 47:
#line 471 "cif_grammar.y" /* yacc.c:1646  */
    { (yyval.typed_value) = typed_value_from_value( new_value_from_scalar( (yyvsp[0].s), CIF_INT, px ), px ); }
#line 1714 "cif_grammar.tab.c" /* yacc.c:1646  */
    break;


#line 1718 "cif_grammar.tab.c" /* yacc.c:1646  */
      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYEMPTY : YYTRANSLATE (yychar);

  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
# define YYSYNTAX_ERROR yysyntax_error (&yymsg_alloc, &yymsg, \
                                        yyssp, yytoken)
      {
        char const *yymsgp = YY_("syntax error");
        int yysyntax_error_status;
        yysyntax_error_status = YYSYNTAX_ERROR;
        if (yysyntax_error_status == 0)
          yymsgp = yymsg;
        else if (yysyntax_error_status == 1)
          {
            if (yymsg != yymsgbuf)
              YYSTACK_FREE (yymsg);
            yymsg = (char *) YYSTACK_ALLOC (yymsg_alloc);
            if (!yymsg)
              {
                yymsg = yymsgbuf;
                yymsg_alloc = sizeof yymsgbuf;
                yysyntax_error_status = 2;
              }
            else
              {
                yysyntax_error_status = YYSYNTAX_ERROR;
                yymsgp = yymsg;
              }
          }
        yyerror (yymsgp);
        if (yysyntax_error_status == 2)
          goto yyexhaustedlab;
      }
# undef YYSYNTAX_ERROR
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYTERROR;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#if !defined yyoverflow || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  yystos[*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  return yyresult;
}
#line 474 "cif_grammar.y" /* yacc.c:1906  */


static void cif_compile_file( FILE *in, char *filename, cexception_t *ex )
{
    cexception_t inner;
    int yyretval = 0;

    cexception_guard( inner ) {
        cif_compiler_set_file( cif_cc, in );
        px = &inner; /* catch all parser-generated exceptions */
        if( (yyretval = cifparse()) != 0 ) {
            if( cif_compiler_cif( cif_cc ) ) {
                int errcount = cif_compiler_nerrors( cif_cc );
                cif_set_yyretval( cif_compiler_cif( cif_cc ), yyretval );
                cif_set_nerrors( cif_compiler_cif( cif_cc ), errcount );
                cexception_raise( &inner, CIF_UNRECOVERABLE_ERROR,
                    cxprintf( "compiler could not recover "
                        "from errors, quitting now -- "
                        "%d error(s) detected",
                        errcount ));
            }
        }
    }
    cexception_catch {
        if( cif_compiler_file( cif_cc ) ) {
            cif_compiler_set_file( cif_cc, NULL );
        }
        cexception_reraise( inner, ex );
    }
}

CIF *new_cif_from_cif1_file( FILE *in, char *filename, cif_option_t co, cexception_t *ex )
{
    volatile int nerrors;
    cexception_t inner;
    CIF * volatile cif = NULL;
    extern void cifrestart( void );

    assert( !cif_cc );
    cif_cc = new_cif_compiler( filename, co, ex );
    cif_flex_reset_counters();
    cif_lexer_set_compiler( cif_cc );

    if( co & CO_COUNT_LINES_FROM_2 ) {
        cif_flex_set_current_line_number( 2 );
    }

    cexception_guard( inner ) {
        cif_compile_file( in, filename, &inner );
    }
    cexception_catch {
        cifrestart();
        if( !isset_suppress_messages( cif_cc ) ) {
            delete_cif_compiler( cif_cc );
            cif_cc = NULL;
            cexception_reraise( inner, ex );
        } else {
            cexception_t inner2;
            cexception_try( inner2 ) {
                if( cif_yyretval( cif_compiler_cif( cif_cc ) ) == 0 ) {
                    cif_set_yyretval( cif_compiler_cif( cif_cc ), -1 );
                }
                cif_set_nerrors( cif_compiler_cif( cif_cc ),
                                 cif_nerrors( cif_compiler_cif( cif_cc ) ) + 1 );
                cif_set_message( cif_compiler_cif( cif_cc ),
                                 filename, "ERROR",
                                 cexception_message( &inner ),
                                 cexception_syserror( &inner ),
                                 &inner2 );
            }
            cexception_catch {
                cexception_raise
                    ( ex, CIF_OUT_OF_MEMORY_ERROR, "not enough memory to "
                      "record CIF error message" );
            }
        }
    }

    cif = cif_compiler_cif( cif_cc );
    nerrors = cif_compiler_nerrors( cif_cc );
    if( cif && nerrors > 0 ) {
        cif_set_nerrors( cif, nerrors );
    }

    cif_lexer_cleanup();
    cif_compiler_detach_cif( cif_cc );
    delete_cif_compiler( cif_cc );
    cif_cc = NULL;

    cif_revert_message_list( cif );
    return cif;
}

int ciferror( const char *message )
{
    if( strcmp( message, "syntax error" ) == 0 ) {
        message = "incorrect CIF syntax";
    }
    print_message( cif_cc, "ERROR", message, ":",
                   cif_flex_current_line_number(),
                   cif_flex_current_position()+1, px );
    print_trace( cif_cc, (char*)cif_flex_current_line(),
                 cif_flex_current_position()+1, px );
    cif_compiler_increase_nerrors( cif_cc );
    return 0;
}

static typed_value *typed_value_from_value( CIFVALUE *v, cexception_t *ex )
{
    return new_typed_value( cif_flex_current_line_number(),
                             cif_flex_current_position(),
                             strdupx( cif_flex_current_line(), px ), v );
}

/*
int yywrap()
{
#if 0
    if( cif_cc->include_files ) {
	compiler_close_include_file( cif_cc, px );
	return 0;
    } else {
	return 1;
    }
#else
    return 1;
#endif
}
*/

void cif_yy_debug_on( void )
{
#ifdef YYDEBUG
    cifdebug = 1;
#endif
}

void cif_yy_debug_off( void )
{
#ifdef YYDEBUG
    cifdebug = 0;
#endif
}
