import sys
import re
import os

################################

tokens = []
expr_stack = []
symbols = {}

#################################
# CONSTANTS
#################################

DIGITS = '0123456789'
LOGIC_OPERATOR = '><!='
OPERATOR = '+-*/%'
PAREN = '()'

#######################################
# TOKENS
#######################################

TT_PRINT    = 'PRINT'
TT_INPUT    = 'INPUT'
TT_INT      = 'INT'
TT_FLOAT    = 'FLOAT'
TT_CHAR     = 'CHAR'
TT_STRING   = 'STRING'
TT_BOOL     = 'BOOL'
TT_TRUE     = 'True'
TT_FALSE    = 'False'
TT_START    = 'START'
TT_STOP     = 'STOP'

#################################

def open_file(filename):
    os.chdir(r'D:\______PERSONALFOLDERS______\joyang\codes\python\InterpreterbyHowCode')
    data = open(filename, "r").read()
    data += "\n<EOF>"
    return(data)

def checkProgram(tokens):
    checkSTART = tokens.count("START")
    checkSTOP = tokens.count("STOP")

    if checkSTART !=1:
        sys.exit("\t\tINVALID SYNTAX!\n")
    elif checkSTOP != 1:
        sys.exit("\t\tINVALID SYNTAX!\n")
    elif  tokens[0] != TT_START:
        sys.exit("\t\tINVALID SYNTAX!\n")
    elif tokens[len(tokens)-1] != TT_STOP:
        sys.exit("\t\tINVALID SYNTAX!\n")

    # won't freaking work, don't know why 
    # if checkSTART != 1 and checkSTOP != 1 and tokens[0] != TT_START and tokens[len(tokens)-1] != TT_STOP:
    #     sys.exit("\t\tINVALID SYNTAX!")


def lex(filecontents):

    isInt = 0
    isFloat = 0
    isChar = 0
    isString = 0
    isBool = 0
    
    isLogicOp = 0
    isInput = 0
    isInt2 = 0
    isFloat2 = 0
    isBool2 = 0
    isString2 = 0
    isString3 = 0 # a string was declared >>> string a
    isChar2 = 0
    isChar3 = 0 # a char was declared >>> char a
    isComment = 0

    tok = ""
    logicOp = ""
    ch = ""
    string = ""
    expr = ""
    var = ""

    state = 0
    isExpr = 0
    varStarted = 0
    # checkVarBool = 0
    charDone = 0
    declareCon = 0
    isAssign = 0 # indicator nga naay DECLARED variable na detect
    
    test = ""

    filecontents = list(filecontents)

    for char in filecontents:
        tok += char
        
        if isComment == 1: #if line is a 'comment'
            if tok == "\n":
                isComment = 0 # 'comment' ends
            tok = ""
            continue
        else:
            if tok == " ":
                if isString == 0:
                    tok = ""
                else:
                    tok = " "
            elif tok == "*" and isInt == 0 and isFloat == 0: #looks for comment start indicator '*'
                isComment = 1
            elif tok == "\n" or tok == "<EOF>": 
                if expr != "" and isInt == 1 and isExpr == 1: # --- start --------------------------------------------------
                    tokens.append("INT:" + expr)
                    expr = ""                                               # para ni sa print na function
                    isInt = 0                                               # para sa print diriso 
                elif expr != "" and isFloat == 1 and isExpr == 1:           # >>> print 1234
                    tokens.append("FLOAT:" + expr)                          # >>> print 1+3
                    expr = ""
                    isFloat = 0                                             # para ma append ang expression na e print without variables
                elif expr != "" and isInt == 1 and isExpr == 0:
                    tokens.append("INT:" + expr)
                    expr = ""
                    isInt = 0
                elif expr != "" and isFloat == 1 and isExpr == 0:
                    tokens.append("FLOAT:" + expr)
                    expr = ""
                    isFloat = 0 
                elif logicOp != "": 
                    if var != "": # if naay variable name, append sa daan ang variable name
                        tokens.append("VAR:" + var)
                        var = ""
                        varStarted = 0
                    tokens.append("BOOL:" + logicOp)
                    logicOp = ""
                    isLogicOp = 0 # -------------------------------end------------------------------------------------------------
                elif var!= "" and expr == "" and isInt == 1 and isExpr == 0 and isInt2 == 0: # --- start --------------------------------------------------
                    tokens.append("VAR:" + var)
                    var = ""                                                               # para ma append ang 'd' with its datatype
                    if isAssign == 0:                                                      # >>> int a, b = 1+2+3, c, d
                        tokens.append("INT:")
                    expr = ""
                    isInt = 0                                                              # 'isAssign' is indicator nga naay DECLARED variable na detect
                    varStarted = 0
                elif var!= "" and expr == "" and isFloat == 1 and isExpr == 0 and isFloat2 == 0:
                    tokens.append("VAR:" + var)
                    var = ""
                    if isAssign == 0:
                        tokens.append("FLOAT:")
                    isFloat = 0
                    varStarted = 0 # -------------------------------end------------------------------------------------------------
                elif var != "" and isBool == 1 and isLogicOp == 0 and isInput == 0: # --- start --------------------------------------------------
                    tokens.append("VAR:" + var)
                    var = ""                                # para ma append ang last na variable name with its datatype in multiple declaration in single line
                    tokens.append("BOOL:")                                                      # para ma append ang 'c' with its datatype
                    isBool = 0                                                                  # char a, b = 'x', e = '8', c
                    varStarted = 0
                elif var != "" and isString == 0 and isChar == 0 and isInput == 0:
                    tokens.append("VAR:" + var)
                    var = ""
                    varStarted = 0
                    if isChar3 == 1 and isAssign == 0:
                        tokens.append("CHAR:")
                        isChar3 = 0
                    elif isString3 == 1 and isAssign == 0:
                        tokens.append("STRING:")
                        isString3 = 0 # -------------------------------end------------------------------------------------------------
                elif var != "" and isInput == 1: # to indicate datatype of input needed
                    if isInt2 == 1:
                        tokens.append("INT")
                        isInt2 = 0
                    elif isFloat2 == 1:
                        tokens.append("FLOAT")
                        isFloat2 = 0
                    elif isChar2 == 1:
                        tokens.append("CHAR")
                        isChar2 = 0
                    elif isString2 == 1:
                        tokens.append("STRING")
                        isString2 = 0
                    elif isBool2 == 1:
                        tokens.append("BOOL")
                        isBool2 = 0
                    tokens.append("VAR:" + var)
                    var = ""
                    varStarted = 0
                    isInput = 0
                tok = ""
                isExpr = 0
                isInt = 0
                isBool = 0
                isChar = 0
                isString = 0
                isAssign = 0
            elif tok == ",": # for multiple declarations in one line
                tok = ""
                if var != "" and expr == "": # if the a data wasn't assigned to the last variable 
                    tokens.append("VAR:" + var)     # >>> int a=c, b, c >> for c, to know what it's datatype
                    var = ""
                    if isAssign == 0:
                        if isInt == 1:
                            tokens.append("INT:")
                            expr = ""
                        elif isFloat == 1:
                            tokens.append("FLOAT:" )
                            expr = ""
                        elif isBool == 1:
                            tokens.append("BOOL:")
                            logicOp = ""
                        elif isChar3 == 1:
                            tokens.append("CHAR:")
                        elif isString3 == 1:
                            tokens.append("STRING:")
                elif tokens[len(tokens)-1][0:6] == "STRING": # >>> string a = "hello", b, c = "itlog"
                    var = ""                                    # para ma store ang succeding token 
                    varStarted = 1                              # after maka read ug string
                    continue
                elif tokens[len(tokens)-1][0:4] == "CHAR":      # same idea sa CHAR ug BOOL
                    var = ""
                    varStarted = 1
                    continue
                elif tokens[len(tokens)-1][0:4] == "BOOL":
                    var = ""
                    varStarted = 1
                    continue
                elif expr != "" or isLogicOp == 1: # para dili ma concatinate ang next token with its next token
                    if isInt == 1 and isExpr == 1:     # int a = 1+2+3, b, c >>> dili maread as one ang 'b' and 'c'
                        tokens.append("INT:" + expr)      
                        expr = ""                           #same para sa float
                    if isFloat == 1 and isExpr == 1:
                        tokens.append("FLOAT:" + expr)
                        expr = ""
                    elif isInt == 1 and isExpr == 0:        # same ra gehapon, pero dili sa expressions 
                        tokens.append("INT:" + expr)                # >>> int a = 1, b, c 
                        expr = ""
                    elif isFloat == 1 and isExpr == 0:
                        tokens.append("FLOAT:" + expr)
                        expr = ""
                    elif logicOp != "":
                        tokens.append("BOOL:" + logicOp)
                    isExpr = 0
                    varStarted = 1 
                logicOp = "" 
                isLogicOp = 0
                isAssign = 0
            elif tok == TT_START and isString == 0 and varStarted == 0: # mu append ra sa 'START' if wala inside sa string ug variable
                tokens.append(TT_START)
                tok = ""
            elif tok == TT_STOP and isString == 0 and varStarted == 0: # mu append ra sa 'STOP' if wala inside sa string ug variable
                tokens.append(TT_STOP)   
                tok = ""                           
            elif tok == TT_INT: # if ka detect ug 'int'
                if isInput == 1:        # if na activate and 'isInput', e active pud ang 'isInt2'
                    isInt2 = 1          # para ni sa variable na storan sa input
                varStarted = 1
                isInt = 1
                tok = ""
            elif tok == TT_FLOAT: # if ka detect ug 'float'
                if isInput == 1:    
                    isFloat2 = 1    
                varStarted = 1
                isFloat = 1                                         #SAME RA SA 'char', 'float', 'string', 'bool'
                tok = ""
            elif tok == TT_CHAR: # if ka detect ug 'char'
                isChar3 = 1
                if isInput == 1:
                    isChar2 = 1
                varStarted = 1
                tok = ""
            elif tok == TT_STRING: # if ka detect ug 'string'
                isString3 = 1
                if isInput == 1:
                    isString2 = 1
                varStarted = 1
                tok = ""
            elif tok == TT_BOOL: # if ka detect ug 'bool'
                if isInput == 1:
                    isBool2 = 1
                varStarted = 1
                isBool = 1
                tok = ""
            elif tok == "and" or tok == "or" or tok == "not" and isString == 0: # para logical operations
                isLogicOp = 1        
                logicOp += " "
                logicOp += tok
                logicOp += " "
                tok = ""
            elif tok == "=" and isLogicOp == 0 and isString == 0 and isChar == 0: 
                if var != "":                           # tokenizing variables and then 'EQUALS'                
                    tokens.append("VAR:" + var)         # that is not inside a string or char
                    var = ""
                    varStarted = 0
                # elif var != "" and isBool:
                #     tokens.append("VAR:" + var)
                #     var = ""
                #     varStarted = 0
                #     checkVarBool = 1
                tokens.append("EQUALS")
                tok = ""
            elif tok == "$" and isString == 0 and isChar == 0: #para ni maka store/access sa data sa already declared na nga variable
                if tokens[len(tokens)-1] == "EQUALS": # para mu work ni >>> int a = $var >>> $a = $b
                    var = ""                          
                    varStarted = 1
                varStarted = 1
                tok = ""
                isAssign = 1 # indicator nga naay DECLARED variable na detect
            elif varStarted == 1: #nag start na ug tokenize sa variable name
                var += tok
                tok = ""
            elif tok == TT_PRINT:
                tokens.append(TT_PRINT)
                tok = "" #reset everytime we find a token
            elif tok == TT_INPUT:
                isInput = 1
                tokens.append(TT_INPUT)
                tok = ""
            elif tok == TT_TRUE:
                tokens.append("BOOL:" + TT_TRUE)
                tok = ""
            elif tok == TT_FALSE:
                tokens.append("BOOL:" + TT_FALSE)
                tok = ""
            elif tok in DIGITS and isChar == 0 and isString == 0: # digit detected is not on string or char
                if isInt == 1:              #if int or float, adto sa expr e concatenate ang tok
                    expr += tok
                    tok = ""
                elif isFloat == 1:
                    expr += tok
                    tok = ""
                elif isBool == 1 or isLogicOp == 1:       #if bool or logicOp, adto sa logicOp e concatenate ang tok
                    logicOp += tok
                    tok = ""
                else:                   # else are considered as int
                    isInt = 1
                    expr += tok
                    tok = ""
            elif tok == "."  and isString == 0: # if mka detect ug '.' na wala sa string
                isFloat = 1             # set isFloat to 1
                expr += tok 
                if isBool == 1:         # if active ang isBool, set is float to 0
                    isFloat = 0         # haron ang succedding digits or operators or ...  
                    logicOp += expr     # kay sa logicOp na ma store
                    expr = ""
                tok = ""
            elif tok in OPERATOR or tok in PAREN  and isString == 0: # if mka detect ug \operators or paren na wala sa string
                isExpr = 1
                expr += tok
                if isLogicOp == 1 or isBool == 1: # if active ang isBool or isLogicOp, store sa logicOp
                    logicOp += expr
                    expr = ""
                tok = ""
            elif tok in LOGIC_OPERATOR  and isString == 0: # if ka detect ug logic Ops
                if isBool == 1:
                    isLogicOp = 1
                    isInt = 0
                    isFloat = 0
                    expr += tok
                    logicOp += expr
                    expr = ""
                else:
                    logicOp += expr
                    logicOp += tok
                    expr = ""
                    isLogicOp = 1
                    isInt = 0
                tok = ""
            elif tok == "\"" or tok == " \"": # para kuha sa string
                if isString == 0: 
                    isString = 1
                elif isString == 1: 
                    tokens.append("STRING:" + string + "\"")
                    string = ""
                    isString = 0
                    tok = ""
            elif isString == 1:
                string += tok
                tok = ""
            elif tok == "'" or charDone == 1  and isString == 0: # para kuha sa char
                if isChar == 0: 
                    isChar = 1
                    charDone = 0
                elif isChar == 1 and charDone == 1:
                    tokens.append("CHAR:" + ch)
                    ch = ""
                    isChar = 0
                    charDone = 0
                tok = ""
            elif isChar == 1 and charDone == 0:
                ch += tok
                tok = ""
                charDone = 1
    print(tokens)
    print("\n---------------------------------- CODE RESULTS--------------------------------------------\n")
    return tokens

def evalExpression(expr):

    # regex = r'[-]?\d+|[+/*-]'
    # expr_stack = re.findall(regex, expr)

    return eval(expr)

def doPRINT(toPRINT):
    if(toPRINT[0:6] == "STRING"):
        toPRINT = toPRINT[8:]
        toPRINT = toPRINT[:-1]
    elif(toPRINT[0:3] == "INT"):
        toPRINT = evalExpression(toPRINT[4:])
    elif(toPRINT[0:5] == "FLOAT"):
        toPRINT = evalExpression(toPRINT[6:])
    elif(toPRINT[0:4] == "CHAR"):
        toPRINT = toPRINT[5:]
    elif(toPRINT[0:4] == "BOOL"):
        toPRINT = evalExpression(toPRINT[5:])
    elif(toPRINT[0:3] == "VAR"):
        if(toPRINT[0:6] == "STRING"):
            toPRINT = toPRINT[8:]
            toPRINT = toPRINT[:-1]
        elif(toPRINT[0:3] == "INT"):
            toPRINT = evalExpression(toPRINT[4:])
        elif(toPRINT[0:5] == "FLOAT"):
            toPRINT = evalExpression(toPRINT[6:])
        elif(toPRINT[0:4] == "CHAR"):
            toPRINT = toPRINT[5:]
        elif(toPRINT[0:4] == "BOOL"):
            toPRINT = evalExpression(toPRINT[5:])
    print(toPRINT)

def doASSIGNvar(varName, varValue):
    temp_value = ""
    if varValue[0:4] == "BOOL":
        if varValue[5:] == "True" or varValue[5:] == "False":
            symbols[varName[4:]] = varValue
        elif len(varValue) == 5:
            symbols[varName[4:]] = varValue
        else:
            symbols[varName[4:]] = "BOOL:" + str(evalExpression(varValue[5:]))
    else:
        symbols[varName[4:]] = varValue

def getVar(varName):
    if varName in symbols:
        return symbols[varName]
    else:
        return ("Undefined Variable")
        exit

def getInput(string, dataType, varName):
    i = input(string)
    datatype = ""
    if(dataType == "STRING"):
        symbols[varName] = "STRING:\"" + i + "\""
    elif(dataType == "INT"):
        symbols[varName] = "INT:" + i
    elif(dataType == "FLOAT"):
        symbols[varName] = "FLOAT:" + i
    elif(dataType == "CHAR"):
        symbols[varName] = "CHAR:" + i
    elif(dataType == "BOOL"):
        symbols[varName] = "BOOL:" + str(evalExpression(i))

def parse(tokens):
    i = 0
    size = len(tokens)
    while( i < size):
        if tokens[i] == TT_START or tokens[i] == TT_STOP:
            i+=1
            continue
        if tokens[i] + " " + tokens[i+1][0:6] == "print STRING" or tokens[i] + " " + tokens[i+1][0:3] == "print INT" or tokens[i] + " " + tokens[i+1][0:5] == "print FLOAT" or tokens[i] + " " + tokens[i+1][0:4] == "print CHAR" or tokens[i] + " " + tokens[i+1][0:4] == "print BOOL" or tokens[i] + " " + tokens[i+1][0:3] == "print VAR":
            if tokens[i+1][0:6] == "STRING":
                doPRINT(tokens[i+1])
            elif tokens[i+1][0:3] == "INT":
                doPRINT(tokens[i+1])
            elif tokens[i+1][0:5] == "FLOAT":
                doPRINT(tokens[i+1])
            elif tokens[i+1][0:4] == "CHAR":
                doPRINT(tokens[i+1])
            elif tokens[i+1][0:4] == "BOOL":
                doPRINT(tokens[i+1])
            elif tokens[i+1][0:3] == "VAR":
                doPRINT(getVar(tokens[i+1][4:]))
            i+=2
        elif tokens[i][0:3] + " " + tokens[i+1][0:3] == "VAR INT" or tokens[i][0:3] + " " + tokens[i+1][0:5] == "VAR FLOAT" or tokens[i][0:3] + " " + tokens[i+1][0:4] == "VAR CHAR" or tokens[i][0:3] + " " + tokens[i+1][0:6] == "VAR STRING" or tokens[i][0:3] + " " + tokens[i+1][0:4] == "VAR BOOL":
            if tokens[i+1][0:3] == "INT":
                doASSIGNvar(tokens[i], "INT:")
            elif tokens[i+1][0:5] == "FLOAT":
                doASSIGNvar(tokens[i], "FLOAT:")
            elif tokens[i+1][0:4] == "CHAR":
                doASSIGNvar(tokens[i], "CHAR:")
            elif tokens[i+1][0:6] == "STRING":
                doASSIGNvar(tokens[i], "STRING:")
            elif tokens[i+1][0:4] == "BOOL":
                doASSIGNvar(tokens[i], "BOOL:")
            i += 2
        # execute input function without string instructions
        elif tokens[i] + " " + tokens[i+2][0:3] == "input VAR":
            getInput("", tokens[i+1], tokens[i+2][4:])
            i+=3
        elif tokens[i][0:3] + " " + tokens[i+1] + " " + tokens[i+2][0:6] == "VAR EQUALS STRING" or tokens[i][0:3] + " " + tokens[i+1] + " " + tokens[i+2][0:3] == "VAR EQUALS INT" or tokens[i][0:3] + " " + tokens[i+1] + " " + tokens[i+2][0:5] == "VAR EQUALS FLOAT" or tokens[i][0:3] + " " + tokens[i+1] + " " + tokens[i+2][0:4] == "VAR EQUALS CHAR" or tokens[i][0:3] + " " + tokens[i+1] + " " + tokens[i+2][0:4] == "VAR EQUALS BOOL" or tokens[i][0:3] + " " + tokens[i+1] + " " + tokens[i+2][0:3] == "VAR EQUALS VAR":
            if tokens[i+2][0:6] == "STRING":
                doASSIGNvar(tokens[i], tokens[i+2])
            elif tokens[i+2][0:3] == "INT":
                doASSIGNvar(tokens[i], "INT:" + str(evalExpression(tokens[i+2][4:])))
                #doASSIGNvar(tokens[i], tokens[i+2])
            elif tokens[i+2][0:5] == "FLOAT":
                doASSIGNvar(tokens[i], "FLOAT:" + str(evalExpression(tokens[i+2][6:])))
                #doASSIGNvar(tokens[i], tokens[i+2])
            elif tokens[i+2][0:4] == "CHAR":
                doASSIGNvar(tokens[i], tokens[i+2])
            elif tokens[i+2][0:4] == "BOOL":
                doASSIGNvar(tokens[i], tokens[i+2])
            elif tokens[i+2][0:3] == "VAR":
                doASSIGNvar(tokens[i], getVar(tokens[i+2][4:]))
            i+=3
         # execute input function with string instructions
        elif tokens[i] + " " + tokens[i+1][0:6] + " " + tokens[i+3][0:3] == "input STRING VAR":
            getInput(tokens[i+1][7:], tokens[i+2], tokens[i+3][4:])
            i+=4

    print("\n----------------------------------END OF CODE --------------------------------------------\n")
    print("\n** TOKENS **")
    print(tokens)
    print("\n\n** SYMBOLS **")
    print(symbols)
    print("\n")

def run():
    data = open_file('test.lang')
    tokens = lex(data)
    checkProgram(tokens)
    parse(tokens)

run()