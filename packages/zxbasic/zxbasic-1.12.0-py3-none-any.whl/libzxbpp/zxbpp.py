#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4:et:

# ----------------------------------------------------------------------
# Copyleft (K), Jose M. Rodriguez-Rosa (a.k.a. Boriel)
#
# This program is Free Software and is released under the terms of
#                    the GNU General License
#
# This is the Parser for the ZXBpp (ZXBasic Preprocessor)
# ----------------------------------------------------------------------

import sys
import os
import re
import argparse
from typing import NamedTuple, List

from .zxbpplex import tokens  # noqa
from . import zxbpplex, zxbasmpplex
from ply import yacc

import api
from api.config import OPTIONS
from api import global_
import api.utils
from .prepro.output import warning, error, CURRENT_FILE
from .prepro import DefinesTable, ID, MacroCall, Arg, ArgList
from .prepro.exceptions import PreprocError


OUTPUT = ''
INCLUDED = {}  # Already included files (with lines)
SPACES = re.compile(r'[ \t]+')

# Set to BASIC or ASM depending on the Lexer context
# e.g. for .ASM files should be set to zxbasmpplex.Lexer()
# Use setMode('ASM' or 'BASIC') to change this FLAG
LEXER = zxbpplex.Lexer()

# CURRENT working directory for this cpp
CURRENT_DIR = None

# Default include path
INCLUDEPATH = ('library', 'library-asm')

# Enabled to FALSE if IFDEF failed
ENABLED: bool = True


class IfDef(NamedTuple):
    enabled: bool
    line: int


# IFDEFS array
IFDEFS: List[IfDef] = []  # Push (Line, state here)


precedence = (
    ('left', 'DUMMY'),
    ('left', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('right', 'LLP'),
)


def init():
    """ Initializes the preprocessor
    """
    global OUTPUT
    global INCLUDED
    global CURRENT_DIR
    global ENABLED
    global INCLUDEPATH
    global IFDEFS
    global ID_TABLE
    global CURRENT_FILE

    OPTIONS.add_option_if_not_defined('debug_zxbpp', bool, False)
    global_.FILENAME = '(stdin)'
    OUTPUT = ''
    INCLUDED = {}
    CURRENT_DIR = ''
    pwd = get_include_path()
    INCLUDEPATH = [os.path.join(pwd, 'library'), os.path.join(pwd, 'library-asm')]
    ENABLED = True
    IFDEFS = []
    global_.has_errors = 0
    global_.error_msg_cache.clear()
    parser.defaulted_states = {}
    ID_TABLE = DefinesTable()
    del CURRENT_FILE[:]


def get_include_path():
    """ Default include path using a tricky sys calls.
    """
    return os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir))


def setMode(mode):
    global LEXER

    mode = mode.upper()
    if mode not in ('ASM', 'BASIC'):
        raise PreprocError('Invalid mode "%s"' % mode)

    if mode == 'ASM':
        LEXER = zxbasmpplex.Lexer()
    else:
        LEXER = zxbpplex.Lexer()


def search_filename(fname, lineno, local_first):
    """ Search a filename into the list of the include path.
    If local_first is true, it will try first in the current directory of
    the file being analyzed.
    """
    fname = api.utils.sanitize_filename(fname)
    i_path = [CURRENT_DIR] + INCLUDEPATH if local_first else list(INCLUDEPATH)
    i_path.extend(OPTIONS.include_path.value.split(':') if OPTIONS.include_path.value else [])
    if os.path.isabs(fname):
        if os.path.isfile(fname):
            return fname
    else:
        for dir_ in i_path:
            path = api.utils.sanitize_filename(os.path.join(dir_, fname))
            if os.path.exists(path):
                return path

    error(lineno, "file '%s' not found" % fname)
    return ''


def include_file(filename, lineno, local_first):
    """ Performs a file inclusion (#include) in the preprocessor.
    Writes down that "filename" was included at the current file,
    at line <lineno>.

    If local_first is True, then it will first search the file in the
    local path before looking for it in the include path chain.
    This is used when doing a #include "filename".
    """
    global CURRENT_DIR
    filename = search_filename(filename, lineno, local_first)
    if filename not in INCLUDED.keys():
        INCLUDED[filename] = []

    if len(CURRENT_FILE) > 0:  # Added from which file, line
        INCLUDED[filename].append((CURRENT_FILE[-1], lineno))

    CURRENT_FILE.append(filename)
    CURRENT_DIR = os.path.dirname(filename)
    return LEXER.include(filename)


def include_once(filename, lineno, local_first):
    """ Performs a file inclusion (#include) in the preprocessor.
    Writes down that "filename" was included at the current file,
    at line <lineno>.

    The file is ignored if it was previuosly included (a warning will
    be emitted though).

    If local_first is True, then it will first search the file in the
    local path before looking for it in the include path chain.
    This is used when doing a #include "filename".
    """
    filename = search_filename(filename, lineno, local_first)
    if filename not in INCLUDED.keys():  # If not already included
        return include_file(filename, lineno, local_first)  # include it and return

    # Now checks if the file has been included more than once
    if len(INCLUDED[filename]) > 1:
        warning(lineno, "file '%s' already included more than once, in file "
                        "'%s' at line %i" %
                (filename, INCLUDED[filename][0][0], INCLUDED[filename][0][1]))

    # Empty file (already included)
    LEXER.next_token = '_ENDFILE_'
    return ''


# -------- GRAMMAR RULES for the preprocessor ---------
def p_start(p):
    """ start : program
    """
    global OUTPUT

    OUTPUT += ''.join(p[1])


def p_program(p):
    """ program : include_file
                | line
                | init
                | undef
                | ifdef
                | require
                | pragma
                | errormsg
                | warningmsg
    """
    p[0] = p[1]


def p_program_tokenstring(p):
    """ program : defs NEWLINE
    """
    try:
        tmp = [str(x()) if isinstance(x, MacroCall) else x for x in p[1]]
    except PreprocError as v:
        error(v.lineno, v.message)

    tmp.append(p[2])
    p[0] = tmp


def p_program_tokenstring_2(p):
    """ program : define NEWLINE
    """
    p[0] = p[1] + [p[2]]


def p_program_char(p):
    """ program : program include_file
                | program line
                | program init
                | program undef
                | program ifdef
                | program require
                | program pragma
                | program errormsg
                | program warningmsg
    """
    p[0] = p[1] + p[2]


def p_program_newline(p):
    """ program : program defs NEWLINE
    """
    try:
        tmp = [str(x()) if isinstance(x, MacroCall) else x for x in p[2]]
    except PreprocError as v:
        error(v.lineno, v.message)
        p[0] = []
        return

    p[0] = p[1]
    p[0].extend(tmp)
    p[0].append(p[3])


def p_program_newline_2(p):
    """ program : program define NEWLINE
    """
    p[0] = p[1] + p[2] + [p[3]]


def p_token(p):
    """ token : STRING
              | TOKEN
              | CONTINUE
              | SEPARATOR
              | NUMBER
    """
    p[0] = p[1]


def p_include_file(p):
    """ include_file : include NEWLINE program _ENDFILE_
    """
    global CURRENT_DIR
    p[0] = [p[1] + p[2]] + p[3] + [p[4]]
    CURRENT_FILE.pop()  # Remove top of the stack
    CURRENT_DIR = os.path.dirname(CURRENT_FILE[-1])


def p_include_file_empty(p):
    """ include_file : include NEWLINE _ENDFILE_
    """  # This happens when an IFDEF is FALSE
    p[0] = [p[2]]


def p_include_once_empty(p):
    """ include_file : include_once NEWLINE _ENDFILE_
    """
    p[0] = [p[2]]  # Include once already included. Nothing done.


def p_include_once_ok(p):
    """ include_file : include_once NEWLINE program _ENDFILE_
    """
    global CURRENT_DIR
    p[0] = [p[1] + p[2]] + p[3] + [p[4]]
    CURRENT_FILE.pop()  # Remove top of the stack
    CURRENT_DIR = os.path.dirname(CURRENT_FILE[-1])


def p_include(p):
    """ include : INCLUDE STRING
    """
    if ENABLED:
        p[0] = include_file(p[2], p.lineno(2), local_first=True)
    else:
        p[0] = []
        p.lexer.next_token = '_ENDFILE_'


def p_include_fname(p):
    """ include : INCLUDE FILENAME
    """
    if ENABLED:
        p[0] = include_file(p[2], p.lineno(2), local_first=False)
    else:
        p[0] = []
        p.lexer.next_token = '_ENDFILE_'


def p_include_once(p):
    """ include_once : INCLUDE ONCE STRING
    """
    if ENABLED:
        p[0] = include_once(p[3], p.lineno(3), local_first=True)
    else:
        p[0] = []

    if not p[0]:
        p.lexer.next_token = '_ENDFILE_'


def p_include_once_fname(p):
    """ include_once : INCLUDE ONCE FILENAME
    """
    p[0] = []

    if ENABLED:
        p[0] = include_once(p[3], p.lineno(3), local_first=False)
    else:
        p[0] = []

    if not p[0]:
        p.lexer.next_token = '_ENDFILE_'


def p_line(p):
    """ line : LINE INTEGER NEWLINE
    """
    if ENABLED:
        p[0] = ['#%s %s%s' % (p[1], p[2], p[3])]
    else:
        p[0] = []


def p_line_file(p):
    """ line : LINE INTEGER STRING NEWLINE
    """
    if ENABLED:
        p[0] = ['#%s %s "%s"%s' % (p[1], p[2], p[3], p[4])]
    else:
        p[0] = []


def p_require_file(p):
    """ require : REQUIRE STRING NEWLINE
    """
    p[0] = ['#%s "%s"\n' % (p[1], api.utils.sanitize_filename(p[2]))]


def p_init(p):
    """ init : INIT ID NEWLINE
             | INIT STRING NEWLINE
    """
    p[0] = ['#%s %s\n' % (p[1], p[2])]


def p_undef(p):
    """ undef : UNDEF ID
    """
    if ENABLED:
        ID_TABLE.undef(p[2])

    p[0] = []


def p_errormsg(p):
    """ errormsg : ERROR STRING
    """
    if ENABLED:
        error(p.lineno(1), p[2])
    p[0] = []


def p_warningmsg(p):
    """ warningmsg : WARNING STRING
    """
    if ENABLED:
        warning(p.lineno(1), p[2])
    p[0] = []


def p_define(p):
    """ define : DEFINE ID params defs
    """
    if ENABLED:
        if p[4]:
            if SPACES.match(p[4][0]):
                p[4][0] = p[4][0][1:]
            else:
                warning(p.lineno(1), "missing whitespace after the macro name")

        ID_TABLE.define(p[2], args=p[3], value=p[4], lineno=p.lineno(2),
                        fname=CURRENT_FILE[-1])
    p[0] = []


def p_define_params_epsilon(p):
    """ params :
    """
    p[0] = None


def p_define_params_empty(p):
    """ params : LP RP
    """
    # Defines the 'epsilon' parameter
    p[0] = [ID('', value='', args=None, lineno=p.lineno(1),
               fname=CURRENT_FILE[-1])]


def p_define_params_paramlist(p):
    """ params : LP paramlist RP
    """
    for i in p[2]:
        if not isinstance(i, ID):
            error(p.lineno(3),
                  '"%s" might not appear in a macro parameter list' % str(i))
            p[0] = None
            return

    names = [x.name for x in p[2]]
    for i in range(len(names)):
        if names[i] in names[i + 1:]:
            error(p.lineno(3), 'Duplicated name parameter "%s"' % (names[i]))
            p[0] = None
            return

    p[0] = p[2]


def p_paramlist_single(p):
    """ paramlist : ID
    """
    p[0] = [ID(p[1], value='', args=None, lineno=p.lineno(1),
               fname=CURRENT_FILE[-1])]


def p_paramlist_paramlist(p):
    """ paramlist : paramlist COMMA ID
    """
    p[0] = p[1] + [ID(p[3], value='', args=None, lineno=p.lineno(1),
                      fname=CURRENT_FILE[-1])]


def p_pragma_id(p):
    """ pragma : PRAGMA ID
    """
    p[0] = ['#%s %s' % (p[1], p[2])]


def p_pragma_id_expr(p):
    """ pragma : PRAGMA ID EQ ID
               | PRAGMA ID EQ STRING
               | PRAGMA ID EQ INTEGER
    """
    p[0] = ['#%s %s %s %s' % (p[1], p[2], p[3], p[4])]


def p_pragma_push(p):
    """ pragma : PRAGMA PUSH LP ID RP
               | PRAGMA POP LP ID RP
    """
    p[0] = ['#%s %s%s%s%s' % (p[1], p[2], p[3], p[4], p[5])]


def p_ifdef(p):
    """ ifdef : if_header NEWLINE program ENDIF
    """
    global ENABLED

    if ENABLED:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

    p[0] += ['#line %i "%s"' % (p.lineno(4) + 1, CURRENT_FILE[-1])]
    ENABLED = IFDEFS.pop().enabled


def p_ifdef_else(p):
    """ ifdef : ifdefelsea ifdefelseb ENDIF
    """
    global ENABLED

    ENABLED = IFDEFS.pop().enabled
    if ENABLED:
        p[0] = p[1] + p[2]
    else:
        p[0] = []

    p[0] += ['#line %i "%s"' % (p.lineno(3) + 1, CURRENT_FILE[-1])]


def p_ifdef_else_a(p):
    """ ifdefelsea : if_header NEWLINE program
    """
    global ENABLED

    p[0] = []
    if IFDEFS[-1].enabled:
        if p[1]:
            p[0] = [p[2]] + p[3]
        ENABLED = not p[1]


def p_ifdef_else_b(p):
    """ ifdefelseb : ELSE NEWLINE program
    """
    global ENABLED

    if ENABLED:
        p[0] = ['#line %i "%s"%s' % (p.lineno(1) + 1, CURRENT_FILE[-1], p[2])]
        p[0] += p[3]
    else:
        p[0] = []


def p_if_header(p):
    """ if_header : IFDEF ID
    """
    global ENABLED

    IFDEFS.append(IfDef(ENABLED, p.lineno(2)))
    if ENABLED:
        ENABLED = ID_TABLE.defined(p[2])

    p[0] = ENABLED


def p_ifn_header(p):
    """ if_header : IFNDEF ID
    """
    global ENABLED

    IFDEFS.append(IfDef(ENABLED, p.lineno(2)))
    if ENABLED:
        ENABLED = not ID_TABLE.defined(p[2])

    p[0] = ENABLED


def p_if_expr_header(p):
    """ if_header : IF expr
    """
    global ENABLED

    IFDEFS.append(IfDef(ENABLED, p.lineno(2)))
    if ENABLED:
        ENABLED = bool(int(p[2])) if p[2].isdigit() else ID_TABLE.defined(p[2])

    p[0] = ENABLED


def p_expr(p):
    """ expr : macrocall
    """
    p[0] = str(p[1]()).strip()


def p_exprne(p):
    """ expr : expr NE expr
    """
    p[0] = '1' if p[1] != p[3] else '0'


def p_expreq(p):
    """ expr : expr EQ expr
    """
    p[0] = '1' if p[1] == p[3] else '0'


def p_exprlt(p):
    """ expr : expr LT expr
    """
    a = int(p[1]) if p[1].isdigit() else 0
    b = int(p[3]) if p[3].isdigit() else 0

    p[0] = '1' if a < b else '0'


def p_exprle(p):
    """ expr : expr LE expr
    """
    a = int(p[1]) if p[1].isdigit() else 0
    b = int(p[3]) if p[3].isdigit() else 0

    p[0] = '1' if a <= b else '0'


def p_exprgt(p):
    """ expr : expr GT expr
    """
    a = int(p[1]) if p[1].isdigit() else 0
    b = int(p[3]) if p[3].isdigit() else 0

    p[0] = '1' if a > b else '0'


def p_exprge(p):
    """ expr : expr GE expr
    """
    a = int(p[1]) if p[1].isdigit() else 0
    b = int(p[3]) if p[3].isdigit() else 0

    p[0] = '1' if a >= b else '0'


def p_defs_list_eps(p):
    """ defs :
    """
    p[0] = []


def p_defs_list(p):
    """ defs : defs def
    """
    p[0] = p[1] + [p[2]]


def p_def(p):
    """ def : token
            | COMMA
            | RRP
            | LLP
    """
    p[0] = p[1]


def p_def_macrocall(p):
    """ def : macrocall
    """
    p[0] = p[1]


def p_macrocall(p):
    """ macrocall : ID args
    """
    p[0] = MacroCall(p.lineno(1), ID_TABLE, p[1], p[2])


def p_args_eps(p):
    """ args : %prec DUMMY
    """
    p[0] = None


def p_args(p):
    """ args : LLP arglist RRP
    """
    p[0] = p[2]


def p_arglist(p):
    """ arglist : arglist COMMA arg
    """
    p[1].addNewArg(p[3])
    p[0] = p[1]


def p_arglist_arg(p):
    """ arglist : arg
    """
    p[0] = ArgList(ID_TABLE)
    p[0].addNewArg(p[1])


def p_arg_eps(p):
    """ arg :
    """
    p[0] = Arg()


def p_arg_argstring(p):
    """ arg : argstring
    """
    p[0] = p[1]


def p_argstring(p):
    """ argstring : token
                  | macrocall
    """
    p[0] = Arg(p[1])


def p_argstring_argslist(p):
    """ argstring : LLP arglist RRP
    """
    p[0] = Arg(p[2])


def p_argstring_token(p):
    """ argstring : argstring token
                  | argstring macrocall
    """
    p[0] = p[1]
    p[0].addToken(p[2])


def p_argstring_argstring(p):
    """ argstring : argstring LLP arglist RRP
    """
    p[0] = p[1]
    p[0].addToken(p[3])


# --- YYERROR

def p_error(p):
    if p is not None:
        value = p.value
        value = ''.join(['|%s|' % hex(ord(x)) if x < ' ' else x for x in value])
        error(p.lineno, "syntax error. Unexpected token '%s' [%s]" %
              (value, p.type))
    else:
        OPTIONS.stderr.value.write("General syntax error at preprocessor "
                                   "(unexpected End of File?)")
    global_.has_errors += 1


def filter_(input_, filename='<internal>', state='INITIAL'):
    """ Filter the input string thought the preprocessor.
    result is appended to OUTPUT global str
    """
    global CURRENT_DIR

    prev_dir = CURRENT_DIR
    CURRENT_FILE.append(filename)
    CURRENT_DIR = os.path.dirname(CURRENT_FILE[-1])
    LEXER.input(input_, filename)
    LEXER.lex.begin(state)
    parser.parse(lexer=LEXER, debug=OPTIONS.debug_zxbpp.value)
    CURRENT_FILE.pop()
    CURRENT_DIR = prev_dir


def main(argv):
    global OUTPUT, ID_TABLE, ENABLED, CURRENT_DIR

    ENABLED = True
    OUTPUT = ''

    if argv:
        CURRENT_FILE.append(argv[0])
    else:
        CURRENT_FILE.append(global_.FILENAME)
    CURRENT_DIR = os.path.dirname(CURRENT_FILE[-1])

    if OPTIONS.Sinclair.value:
        included_file = search_filename('sinclair.bas', 0, local_first=False)
        if not included_file:
            return

        OUTPUT += include_once(included_file, 0, local_first=False)
        if len(OUTPUT) and OUTPUT[-1] != '\n':
            OUTPUT += '\n'

        parser.parse(lexer=LEXER, debug=OPTIONS.debug_zxbpp.value)
        CURRENT_FILE.pop()
        CURRENT_DIR = os.path.dirname(CURRENT_FILE[-1])

    prev_file = global_.FILENAME
    global_.FILENAME = CURRENT_FILE[-1]
    OUTPUT += LEXER.include(CURRENT_FILE[-1])
    if len(OUTPUT) and OUTPUT[-1] != '\n':
        OUTPUT += '\n'

    parser.parse(lexer=LEXER, debug=OPTIONS.debug_zxbpp.value)
    CURRENT_FILE.pop()
    global_.FILENAME = prev_file
    return global_.has_errors


parser = api.utils.get_or_create('zxbppparse', lambda: yacc.yacc())
parser.defaulted_states = {}
ID_TABLE = DefinesTable()


# ------- ERROR And Warning messages ----------------

def entry_point(args=None):
    if args is None:
        args = sys.argv[1:]

    api.config.init()
    init()
    setMode('BASIC')

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', type=str, dest='output_file', default=None,
                        help='Sets output file. Default is to output to console (STDOUT)')
    parser.add_argument('-d', '--debug', dest='debug', default=OPTIONS.Debug.value, action='count',
                        help='Enable verbosity/debugging output. Additional -d increases verbosity/debug level')
    parser.add_argument('-e', '--errmsg', type=str, dest='stderr', default=None,
                        help='Error messages file. Standard error console by default (STDERR)')
    parser.add_argument('input_file', type=str, default=None, nargs='?',
                        help="File to parse. If not specified, console input will be used (STDIN)")

    options = parser.parse_args(args=args)
    OPTIONS.Debug.value = options.debug
    OPTIONS.debug_zxbpp.value = OPTIONS.Debug.value > 0

    if options.stderr:
        OPTIONS.StdErrFileName.value = options.stderr
        OPTIONS.stderr.value = api.utils.open_file(OPTIONS.StdErrFileName.value, 'wt', 'utf-8')

    result = main([options.input_file] if options.input_file else [])
    if not global_.has_errors:  # ok?
        if options.output_file:
            with api.utils.open_file(options.output_file, 'wt', 'utf-8') as output_file:
                output_file.write(OUTPUT)
        else:
            OPTIONS.stdout.value.write(OUTPUT)
    return result


if __name__ == '__main__':
    sys.exit(entry_point())
