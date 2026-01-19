# Script Name: GF_PY3_FUNCTION_CTypes.py
# Environment: Python 3.8.0
# Create By GF 2024-01-22 18:16

# ##################################################

import ctypes

# ##################################################

_LIST_SYMBOL_HEAD:str      = str('[')
_LIST_SYMBOL_TAIL:str      = str(']')
_LIST_SYMBOL_BLANK:str     = str(' ')
_LIST_SYMBOL_DELIMITER:str = str(',')

# ##################################################

def PY3_STR_TO_C_CHAR_P(INPUT:str) -> str:
    PY3_BYTES = INPUT.encode("utf-8")
    C_CHAR_P  = ctypes.create_string_buffer(PY3_BYTES)
    return C_CHAR_P

def C_CHAR_P_TO_PY3_STR(INPUT:str) -> object:
    if INPUT:
        PY3_STRING = INPUT.decode("utf-8")
        # CLIB.free(INPUT) # -> Release "Char Pointer" Memory Allocated by C Function Call.
        return PY3_STRING
    else:
        return None

# ##################################################

def COPY_STRING_DELETE_GIVEN_CHAR_AT_FIRST(STRING:str, GIVEN_CHAR:str) -> str:

    STRING_LENGTH:int  = len(STRING)
    STRING_CHARAC:list = []
    # ----------------------------------------------
    LEFT:int = 0
    RIGH:int = STRING_LENGTH - 1
    while LEFT <= RIGH:
        """ Within The Loop Statement. """
        if (LEFT == 0 and STRING[LEFT] == GIVEN_CHAR):
            LEFT = LEFT + 1
        else:
            STRING_CHARAC.append(STRING[LEFT])
            LEFT = LEFT + 1
    # ----------------------------------------------
    return str('').join(STRING_CHARAC)

def COPY_STRING_DELETE_GIVEN_CHAR_AT_FINAL(STRING:str, GIVEN_CHAR:str) -> str:

    STRING_LENGTH:int  = len(STRING)
    STRING_CHARAC:list = []
    # ----------------------------------------------
    LEFT:int = 0
    RIGH:int = STRING_LENGTH - 1
    while LEFT <= RIGH:
        """ Within The Loop Statement. """
        if (LEFT == RIGH and STRING[LEFT] == GIVEN_CHAR):
            LEFT = LEFT + 1
        else:
            STRING_CHARAC.append(STRING[LEFT])
            LEFT = LEFT + 1
    # ----------------------------------------------
    return str('').join(STRING_CHARAC)

def COPY_STRING_DELETE_ALL_GIVEN_CHAR_AT_HEAD(STRING:str, GIVEN_CHAR:str) -> str:

    STRING_LABORS:str = STRING
    # ----------------------------------------------
    IDX:int = 0
    while STRING_LABORS[IDX] == GIVEN_CHAR:
        """ Within The Loop Statement. """
        STRING_LABORS = COPY_STRING_DELETE_GIVEN_CHAR_AT_FIRST(STRING_LABORS, GIVEN_CHAR)
    # ----------------------------------------------
    return STRING_LABORS

def COPY_STRING_DELETE_ALL_GIVEN_CHAR_AT_TAIL(STRING:str, GIVEN_CHAR:str) -> str:

    STRING_LENGTH:int  = len(STRING)
    STRING_LABORS:str = STRING
    # ----------------------------------------------
    IDX:int = STRING_LENGTH - 1
    while STRING_LABORS[IDX] == GIVEN_CHAR:
        """ Within The Loop Statement. """
        STRING_LABORS = COPY_STRING_DELETE_GIVEN_CHAR_AT_FINAL(STRING_LABORS, GIVEN_CHAR)
        IDX = IDX - 1
    # ----------------------------------------------
    return STRING_LABORS

def COPY_STRING_LIKE_LIST_EXTRACT_ELEMENT_BY_INDEX(STRING_LIKE_LIST:str, INDEX:int):

    """
    Need Functions:
    len(string:str) -> int
    
    Illustration:
    >>>> List:str = '[1, 2, 3, 4, 5]'
    >>>> Result:str = STRING_LIKE_LIST_EXTRACT_ELEMENT_BY_INDEX(List, 3)
    >>>> print(Result)
    OUT: '4'
    """
    
    LABOR_STRING_LIKE_LIST = STRING_LIKE_LIST
    # ----------------------------------------------
    # Convert: '[A, B, C]' ===> 'A, B, C'
    LABOR_STRING_LIKE_LIST = LABOR_STRING_LIKE_LIST[ 1:]
    LABOR_STRING_LIKE_LIST = LABOR_STRING_LIKE_LIST[:-1] # -> Python 3 List Slice with Head But Without Tail.
    # ----------------------------------------------
    STRLIST_CONTENT_LENGTH = len(LABOR_STRING_LIKE_LIST)
    # ----------------------------------------------
    if (STRLIST_CONTENT_LENGTH == 0):
        """ Within The Conditional Statement. """
        print("[Caution] \"COPY_STRING_LIKE_LIST_EXTRACT_ELEMENT_BY_INDEX\": String Form List is Empty.\n")
        # ..........................................
        return None
    elif (INDEX < 0):
        """ Within The Conditional Statement. """
        """ This Step is Redundant in Python 3 and is Only Used to Preserve The Implementation Logic """
        FRUIT:list = LABOR_STRING_LIKE_LIST.split(_LIST_SYMBOL_DELIMITER)
        FRUIT = [COPY_STRING_DELETE_ALL_GIVEN_CHAR_AT_HEAD(X, str(' ')) for X in FRUIT]
        return FRUIT[INDEX]
    else:
        """ Within The Conditional Statement. """
        FRUIT:list = LABOR_STRING_LIKE_LIST.split(_LIST_SYMBOL_DELIMITER)
        FRUIT = [COPY_STRING_DELETE_ALL_GIVEN_CHAR_AT_HEAD(X, str(' ')) for X in FRUIT]
        return FRUIT[INDEX]

def COPY_STRING_LIKE_LIST_REPLACE_VALUE_BY_INDEX(STRING_LIKE_LIST:str, INDEX:int, VALUE:str):
    
    """
    Need Functions:
    len(string:str) -> int
    
    Illustration:
    >>>> List:str = '[1, 2, 3, 4, 5]'
    >>>> Result:str = COPY_STRING_LIKE_LIST_REPLACE_VALUE_BY_INDEX(List, 3, "B")
    >>>> print(Result);
    OUT: '[1, 2, 3, B, 5]'
    """

    LABOR_STRING_LIKE_LIST = STRING_LIKE_LIST
    # ----------------------------------------------
    # Convert: '[A, B, C]' ===> 'A, B, C'
    LABOR_STRING_LIKE_LIST = LABOR_STRING_LIKE_LIST[ 1:]
    LABOR_STRING_LIKE_LIST = LABOR_STRING_LIKE_LIST[:-1] # -> Python 3 List Slice with Head But Without Tail.
    # ----------------------------------------------
    STRLIST_CONTENT_LENGTH = len(LABOR_STRING_LIKE_LIST)
    # ----------------------------------------------
    # Convert: 'A, B, C' ===> ['A', ' B', ' C']
    LABOR_STRING_LIKE_LIST = LABOR_STRING_LIKE_LIST.split(_LIST_SYMBOL_DELIMITER)
    # ----------------------------------------------
    STRLIST_ELEMENT_NUMBER = len(LABOR_STRING_LIKE_LIST)
    # ----------------------------------------------
    if (STRLIST_CONTENT_LENGTH == 0):
        """ Within The Conditional Statement. """
        print("[Caution] \"COPY_STRING_LIKE_LIST_REPLACE_VALUE_BY_INDEX\": String Form List is Empty.\n")
        # ..........................................
        return None
    elif (INDEX == 0):
        """ Within The Conditional Statement. """
        FRUIT:list = LABOR_STRING_LIKE_LIST
        ALTER:str  = VALUE
        # ..........................................
        ALTER = COPY_STRING_DELETE_ALL_GIVEN_CHAR_AT_HEAD(ALTER, _LIST_SYMBOL_BLANK)
        ALTER = COPY_STRING_DELETE_ALL_GIVEN_CHAR_AT_TAIL(ALTER, _LIST_SYMBOL_BLANK)
        # ..........................................
        FRUIT[INDEX] = (_LIST_SYMBOL_HEAD + ALTER)
        FRUIT[-1]    = (FRUIT[-1] + _LIST_SYMBOL_TAIL)
        # ..........................................
        return str(',').join(FRUIT)
    elif (INDEX == (STRLIST_ELEMENT_NUMBER - 1)):
        """ Within The Conditional Statement. """
        FRUIT:list = LABOR_STRING_LIKE_LIST
        ALTER:str  = VALUE
        # ..........................................
        ALTER = COPY_STRING_DELETE_ALL_GIVEN_CHAR_AT_HEAD(ALTER, _LIST_SYMBOL_BLANK)
        ALTER = COPY_STRING_DELETE_ALL_GIVEN_CHAR_AT_TAIL(ALTER, _LIST_SYMBOL_BLANK)
        # ..........................................
        FRUIT[0]     = (_LIST_SYMBOL_HEAD + FRUIT[0])
        FRUIT[INDEX] = (_LIST_SYMBOL_BLANK + ALTER + _LIST_SYMBOL_TAIL)
        # ..........................................
        return str(',').join(FRUIT)
    else:
        """ Within The Conditional Statement. """
        FRUIT:list = LABOR_STRING_LIKE_LIST
        ALTER:str  = VALUE
        # ..........................................
        ALTER = COPY_STRING_DELETE_ALL_GIVEN_CHAR_AT_HEAD(ALTER, _LIST_SYMBOL_BLANK)
        ALTER = COPY_STRING_DELETE_ALL_GIVEN_CHAR_AT_TAIL(ALTER, _LIST_SYMBOL_BLANK)
        # ..........................................
        FRUIT[0]     = (_LIST_SYMBOL_HEAD + FRUIT[0])
        FRUIT[INDEX] = (_LIST_SYMBOL_BLANK + ALTER)
        FRUIT[-1]    = (FRUIT[-1] + _LIST_SYMBOL_TAIL)
        # ..........................................
        return str(',').join(FRUIT)
