######
# https://craftinginterpreters.com/representing-code.html
#
#Code representation key:
#a,b,c,d = nonterminal
#'a','b','c','d' = terminal
#
#statement -> a 'a' a = statement will be of form nonterminal, terminal, nonterminal
#statement -> a | b = statement has options a or b
#statement -> ( a | 'c' ) b = statement is of form (options a or 'c'), b
#statement -> a * = statement will have a appear 0 or more times
#statement -> b a * = statement will be of form b, a appearing 0 or more times
#statement -> a + = satement will have a appear at least 1 time
#statement -> c 'a' ( a | b ) ? statement is c, 'a', ( a | b ) appearing 0-1 times
#
#####################
#@Jonathan Ke (jak2)
#@9/25/2019
#
#
#
#https://craftinginterpreters.com/representing-code.html
'''
expression -> literal | unary | binary | grouping ;

literal    -> NUMBER | STRING | "true" | "false" | "nil" ;
grouping   -> "(" expression ")" ;
unary      -> ( "-" | "!" ) expression ;
binary     -> expression operator expression ;
operator   -> "==" | "!=" | "<" | "<=" | ">" | ">="
           | "+"  | "-"  | "*" | "/" ;
'''

from Token import *
import JavaLang

def defineNodes(grammarRules):
    allTerms = grammarRules.split()
    nodeList = []
    curState = []
    for term in allTerms:
        if term == ';':
            nodeList.append(createNode(curState))
            curState.clear()
        else: curState.append(term)
    return nodeList
        
def assignNodes(grammarRules):
    nodeList = defineNodes(grammarRules)
    for node in nodeList:
        node.body = findChildren(node,nodeList)
    return nodeList
        
def createNode(expr):
    #list of children in string form
    head = expr[0]
    expr = expr[2:]
    childrenList = exprToList(expr)
    return Expr(head,childrenList)
    
def exprToList(expr): 
    #reads expressions and turns them into interpretable lists
    out = []
    i = 0
    while  i < len(expr):
        arg = expr[i]
        if arg == '(':
            subExpr = findSubExpression(expr[i:])
            print(subExpr)
            subList = exprToList(subExpr)
            i += len(subExpr) + 1
            print(expr[i])
            if expr[i][-1] in '*+?': 
                print("HERE")
                #check if the entire argument is of type '*','+','?'
                if '*' in arg:
                    out.append(Star(subList))
                elif '+' in arg:
                    out.append(Plus(subList))
                else: 
                    out.append(Question(subList))
            else:
                out.extend(subList)
        elif arg == '|': #'or' conditions
            return [evaluateBarStatement(expr)]        
        elif '*' == arg[-1]:
            out.append(Star(arg[:-1]))
        elif '+' == arg[-1]:
            out.append(Plus(arg[:-1]))
        elif '?' == arg[-1]:
            out.append(Question(arg[:-1]))
        else:
            out.append(arg)      
        i += 1
    return out 

def evaluateBarStatement(L):
    outTerms = []
    sub = []
    i = 0
    while i < len(L):
        if L[i] == '(': #ignore stuff in parenthesis for now
            skip = len(findSubExpression(L[i:]))
            sub.extend(L[i:i+skip+2])
            i += skip+1
        elif L[i] == '|':
            result = exprToList(sub)
            if len(result) == 1:
                outTerms.append(result[0])
            else: outTerms.append(result)
            sub = []
        else:
            sub.append(L[i])
        i+=1
    result = exprToList(sub)
    if len(result) == 1:
        outTerms.append(result[0])
    else: outTerms.append(result)    
    return Bar(outTerms)    
             
#returns expression in most left parenthesis set
#first value in exp is '('
def findSubExpression(exp):
    out = []
    ct = 0
    for i in exp:
        if i == '(':
            ct += 1
        elif ')' in i:
            ct -= 1
        out.append(i)
        if ct == 0:
            return out[1:-1]
           
def peek(expr,i):
    if i < len(expr):
        return expr[i]
    
def findListBetweenBars(L,i):
    out = []
    for val in L[i+1:]:
        if val == '|':
            return out
        out.append(val)
    return out

def findChildren(node, L):
    out = []
    for opt in node.bodyList:
        if isinstance(opt,Grammar):
            if isinstance(opt,Bar):
                subExpr = findChildren(Expr('temp',opt.val),L)
                out.append(Bar(subExpr))
            elif isinstance(opt,Star):
                subExpr = findChildren(Expr('temp',opt.val),L)
                out.append(Star(subExpr))
            elif isinstance(opt, Question):
                subExpr = findChildren(Expr('temp',opt.val),L)
                out.append(Question(subExpr))
            elif isinstance(opt,Plus): #is plus
                subExpr = findChildren(Expr('temp',opt.val),L)
                out.append(Plus(subExpr))
        elif isinstance(opt,list):
            subExpr = findChildren(Expr("temp",opt),L)
            out.append(subExpr)
        else: #single instance
            if "'" in opt or '"' in opt: #terminal
                out.append(opt)
            else:
                out.append(findNode(L,opt))
    return out

def findNode(L,name):
    for node in L:
        if node.head == name:
            return node
    return None
    
                        

########################################
#Objects used to break down node body
########################################
class Grammar(object):
    def __init__(self,val):
        self.val = val

class Bar(Grammar): #mutiple stored values can replace inside part
    def __init__(self,val):
        self.val = val
        
    def addElement(self,e):
        self.val.append(e)
        
    def __str__(self):
        return 'BAR-> '+str(self.val)
        
class Star(Grammar): #stored value appears atleast 0 times
    def __init__(self,val):
        self.val = val
        
    def __str__(self):
        return 'STAR-> '+self.val
        
class Plus(Grammar): #stored value appears atleast 1 times
    def __init__(self,val):
        self.val = val
        
    def __str__(self):
        return 'PLUS-> '+self.val
        
class Question(Grammar): #statement appears 0 or 1 time
    def __init__(self,val):
        self.val = val
        
    def __str__(self):
        return 'QUEST-> '+self.val


########################################
#Actual parse tree nodes
########################################
class Expr(object):

    def __init__(self, head, bodyList):
        self.head = head
        self.bodyList = bodyList
        self.body = []
        
                     
    def __str__(self):
        L = [str(x) for x in self.bodyList]
        return self.head + ': ' + str(L)
        

########################################
#Testers
########################################

def testExprToList():
    print("\nTesting exprToList:")
    s0 = '''
expression -> literal | unary | binary | grouping ;

literal    -> NUMBER | STRING | "true" | "false" | "nil" ;
grouping   -> "(" expression ")" ;
unary      -> ( "-" | "!" ) expression ;
binary     -> expression operator expression ;
operator   -> "==" | "!=" | "<" | "<=" | ">" | ">="
           | "+"  | "-"  | "*" | "/" ;
'''
    s1 = '''"==" | "!=" | "<" | "<=" | ">" | ">="
           | "+"  | "-"  | "*" | "/" '''.split()
    s2 = '''
    "really" + "crispy" "bacon"
          | "sausage"
          | ( "scrambled" | "poached" | "fried" ) "eggs" 
    '''.split()
    print('########START########')
    out = exprToList(s2)
    print('########END########')
    for i in out:
        print(i)
        
def testCreateNode():
    print("\nTesting createNode:")
    s1 = '''
    binary  -> ( expression ( operator | expression ) ( expression | operator ) )
    '''.split()
    
    s2 = '''
    protein   ->  "really"+ "crispy" "bacon" 
          | "sausage"
          |  ( "scrambled" | "poached" | "fried" ) "eggs" 
    '''.split()
    print('########START########')
    node = createNode(s2)
    print('########END########')
    print(node)
    
def testDefineNodes():
    print("\nTesting defineNodes:")
    s1 = '''
expression -> literal | unary | binary | grouping ;

literal    -> NUMBER | STRING | "true" | "false" | "nil" ;
grouping   -> "(" expression ")" ;
unary      -> ( "-" | "!" ) expression ;
binary     -> expression operator expression ;
operator   -> "==" | "!=" | "<" | "<=" | ">" | ">="
           | "+"  | "-"  | "*" | "/" ;
''' 
    print('########START########')
    nodes = defineNodes(s1)
    print('########END########')
    for node in nodes:
        print(node)
    return

def testAssignNodes():
    print("\nTesting assignNodes:")
    s1 = '''
expression -> literal | unary | binary | grouping ;

literal    -> NUMBER | STRING | "true" | "false" | "nil" ;
grouping   -> "(" expression ")" ;
unary      -> ( "-" | "!" ) expression ;
binary     -> expression operator expression ;
operator   -> "==" | "!=" | "<" | "<=" | ">" | ">="
           | "+"  | "-"  | "*" | "/" ;
''' 
    s2 = '''
    breakfast -> protein ( "with" breakfast "on the side" )?
          | bread ;

protein   -> "really"+ "crispy" "bacon"
          | "sausage"
          | ( "scrambled" | "poached" | "fried" ) "eggs" ;

bread     -> "toast" | "biscuits" | "EnglishMuffin" ;
    '''
    javaLang = JavaLang.JavaLang.JavaGrammar
    print('########START########')
    nodes = assignNodes(javaLang)
    print('########END########')
    for node in nodes:
        print(node.head)
        print('  ',node)
        for obj in node.body:
            print('\t',obj)
    return
    

testExprToList()
testCreateNode()
testDefineNodes()
testAssignNodes()