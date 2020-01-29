#@Jonathan Ke
#@9/26/2019
#parses Java code into a parse tree

from JavaLang import JavaLang as Java
import JavaTokenizer
from Token import *
from TreeNode import *
import copy

#Break down Java grammar string
def breakDownBNF(grammarFull):
    out = []
    sub = []
    prevLine = grammarFull.splitlines()[0]
    for line in grammarFull.splitlines():
        if line != '':
            if line[0].isspace():
                if line.strip() != '':
                    sub.append(rejoinBrackParaBrace(line.strip().split()))
            else:
                out.append((prevLine.strip()[:-1], sub))
                sub = []
                prevLine = line
    out.append((prevLine.strip()[:-1], sub))
    out.pop(0) #first term is a dud
    outDict = dict()
    for block in out:
        outDict[block[0]] = block
    return outDict

#each grammar child must have last element removed(it is the occurence value)
def breakDownBNFComplex(grammarFull):
    out = []
    sub = []
    prevLine = grammarFull.splitlines()[0]
    for line in grammarFull.splitlines():
        if line != '':
            if line[0].isspace() and line.strip() != '':
                #ignore the last element because it is occurence value(only different part)
                sub.append(rejoinBrackParaBrace(line.strip().split()[:-1]))
            else:
                out.append((prevLine.strip()[:-1], sub))
                sub = []
                prevLine = line
    out.append((prevLine.strip()[:-1], sub))
    out.pop(0) #first term is a dud
    outDict = dict()
    for block in out:
        outDict[block[0]] = block
    return outDict

#reorganizes special syntax definitions of grammar before 
#creating parsing dictionary
def rejoinBrackParaBrace(L):
    out = []
    i = 0
    while i < len(L):
        if L[i] != '[' and '[' in L[i]:
            s = []
            for val in L[i:]:
                if val != ']' and ']' in val:
                    s.append(val)
                    break
                s.append(val)
            i+= len(s)
            out.append(" ".join(s))
        elif L[i] != '(' and '(' in L[i]:
            s = []
            for val in L[i:]:
                if val != ')' and ')' in val:
                    s.append(val)
                    break
                elif val != '|':
                    s.append(val)
                i += 1
            i += 1
            out.append(" ".join(s))
        elif '{' in L[i] and '{' != L[i]:
            out.append(L[i])
            i += 1
        elif '{' == L[i]:
            s = []
            ct = 0
            for val in L[i:]:
                s.append(val)
                if '}' == val:
                    ct -= 1
                    if  ct == 0:
                        break
                    else: ct -= 1
                elif '{' in val:
                    ct += 1
            i += len(s)
            if len(s) == 3: # only one element between braces
                out.extend(s)
            else:
                s.pop(0)
                s[0] = '{'+s[0]
                x = s.pop()
                s[-1] = s[-1]+'}'
                out.append(" ".join(s))
        else:
            out.append(L[i])
            i+=1
    return out

#gets all java tokens from JavaLang
def getAllJavaTokens():
    out = set()
    for keyword in Java.keywords:
        out.add(keyword)
    for prim in Java.primitives:
        out.add(prim)
    for sep in Java.separators:
        out.add(sep)
    for op in Java.operators:
        out.add(op)
    return out

#create processable java grammar
class GrammarData(object):
    
    #data = breakDownBNF(Java.JavaGrammar2)
    data = breakDownBNFComplex(open('JavaGrammar', 'r').read())  
    
    @staticmethod
    def refresh():
        grammar = open('JavaGrammar', 'r')
        GrammarData.data = breakDownBNFComplex(grammar.read())  
        grammar.close()
        
#tracks the furthest the parsing function recursed into the token list      
class TokenDepth(object):
    
    def __init__(self, tokenList):
        self.depth = len(tokenList)
        self.initialLength = self.depth
        
    def checkDepth(self, tokenList):
        if len(tokenList) < self.depth:
            self.depth = len(tokenList)
        
#Parsing Object/function
class Node(object):
    def __init__(self, parent, grammarBlock, compareCode, tokenDepth = None):
        self.head = grammarBlock[0]
        #print("\tHead:", self.head)
        self.body = grammarBlock[1]
        self.code = compareCode
        self.parent = parent
        self.tempBool = None #used for tracking variables from children
        self.temp = None #used for tracking variables from children
        self.parseCode = TreeNode(self.head) #returned value
        if tokenDepth == None: #tracks maximum number of tokens the parse completed
            self.tokenDepth = TokenDepth(self.code)
        else: 
            self.tokenDepth = tokenDepth
            self.tokenDepth.checkDepth(self.code)
            
        #check if tokens fit to grammar
        if self.checkBody():
            #print("Return True to",self.parent.head)
            self.passed = True
            self.tokenDepth.checkDepth(self.code)
        else:
            #print("Return False to",self.parent.head)
            self.passed = False
    
    #build child node 
    def visit(self, child, code):
        #initiates a child node
        if child in GrammarData.data:
            return Node(self,GrammarData.data[child], code, 
                        tokenDepth = self.tokenDepth)
                
    #check each listed grammar
    def checkBody(self):
        for sub in self.body:
            if self.checkSub([sub]):     
                return True
        return False
    
    #intermediate checking function
    def checkSub(self, sub):
        #print("\tSUB-> ",sub)
        i = 0
        while i < len(sub):
            response = self.checkSubSub(sub[i], sub)
            if response == self.CONTINUE or response == self.FAILED:
                i +=1
            elif response == self.FAILED:
                #print('FAILED????')
                return False
            else: #grammar passed! 
                return True
        #all subsubs failed, return to body
        return False
    
    CONTINUE = 0
    FAILED = 1
    PASSED = 2
    
    #updates with potential new subs based on current sub input
    def checkExpansions(self, sub, subParent):
        for unit in sub:
            if unit[0] in '(' and len(unit) > 1: #special syntax
                if '(' == unit[0]:
                    subParent.extend(self.createBonusParenthesisStatements(unit,sub))
                    return self.CONTINUE #don't actually evaluate this statement
        return self.PASSED
    
    #checks if current statement aligns with grammar
    def evaluateStatement(self, sub, subParent, code):
        #parse statement
        parseCode = TreeNode(self.head)
        outSignal = self.FAILED #short circuit eval
        for unit in sub:
            if unit == '~': #continue after this statement
                outSignal = self.CONTINUE #can continue checking subParent
                #pass this extra symbol
            elif unit[0] == '{' and unit != '{':
                code = self.evaluateBraces(unit,code,parseCode)
            elif unit[0] == '[' and unit != '[':
                #print("INTO THE BRACKETS WE GO BECAUSE OF",unit)
                code = self.evaluateBrackets(unit,code,parseCode)
            elif (unit[0].isupper() and unit[1].islower() 
                and unit != "Literal" and unit != 'Identifier'): #nonterminal
                child = self.visit(unit, code)
                if child.passed:
                   parseCode.addChild(child.parseCode) 
                   code = child.code 
                else:
                    return outSignal, parseCode, code
            else: #terminal
                outcome, code = self.evaluateTerminal(unit, code, parseCode)
                #destructively alters parseCode and code
                if not outcome:
                    return outSignal, parseCode, code
        return self.PASSED, parseCode, code
    
    allJavaTokens = getAllJavaTokens()
    
    #check if tokens leftover match tokens used by grammar
    @staticmethod
    def checkTokensExist(sub, code):
        tokens = []
        for unit in sub:
            if unit in Node.allJavaTokens:
                tokens.append(unit)
            elif unit == 'Literal' or unit == 'Identifier':
                tokens.append(unit)
        for unit in tokens:
            if not Node.checkTokensExistHelper(unit, code):
                return False
        return True
         
    @staticmethod       
    def checkTokensExistHelper(unit, code):
        for tok in code:
            if unit == 'Literal' and isinstance(tok, Literal):
                return True
            elif unit == 'Identifier' and isinstance(tok, Identifier):
                return True
            elif tok.string == unit:
                return True
        return False
                    
    #Three return types:
    #0 = continue, only the subsub failed
    #1 = subsub failed, essential component of sub failed
    #2 = passed, return pass to body!
    #evaluates a subsub statement for expansions, then checks if subsub passes grammar
    def checkSubSub(self, sub, subParent):
        #print("\t\tSubSub->",sub) 
        if self.isEmpty(sub):
            return self.CONTINUE
        out = self.checkExpansions(sub, subParent)
        if out == self.CONTINUE:
            return out
        #quick check to see if the code has enough tokens to be in statement
        if not self.checkTokensExist(sub, self.code):
            return self.CONTINUE
        #parse statement
        code = copy.deepcopy(self.code)
        out, parseCode, code = self.evaluateStatement(sub, subParent, code)
        if out == self.CONTINUE or out == self.FAILED:
            return out
        elif len(code) == len(self.code):
            return self.CONTINUE
        #succesfully parsed function, update this node's data     
        self.parseCode = parseCode
        self.code = code
        #print("\t\t\tWE HAVE A WINNER")
        return self.PASSED
    
    #just in case the sub statement is empty
    def isEmpty(self,sub):
        for e in sub:
            if e != '~':
                return False
        return True
        
    #terminal evaluation method
    def evaluateTerminal(self, unit, code, parseCode):
        if unit == "Identifier": 
            #print("Identifier vs:",code[0],end=" ")
            if isinstance(code[0],Identifier):
                #print("PASSED")
                out = code.pop(0)
                parseCode.addChild(out)
            else:
                #print("FAILED")
                return False, code
        elif unit == "Literal":
            #print("Literal vs:",code[0],end=" ")
            if isinstance(code[0],Literal):
                #print("PASSED")
                out = code.pop(0)
                parseCode.addChild(out)
            else:
                #print("FAILED")
                return False,code
        else: 
            #print("Keyword: "+unit+' vs:',code[0],end=" ")
            if code[0].string == unit:
                #print("PASSED")
                parseCode.addChild(code.pop(0))
            else:
                #print("FAILED")
                return False, code
        return True, code
    
    #parses grammar rule with reusable subgrammar components
    def evaluateBraces(self, unit, code, parseCode):
        ct = 1
        unit = unit[1:-1].split()
        subParent = [unit]
        outCode = code
        currParseCodeCopy = None
        while True:
            subUnit = subParent[-1] #sub unit to loop
            #print("BRACE SUB->", subUnit)
            out = self.checkExpansions(subUnit,subParent)
            if out != self.CONTINUE:
                codeCopy = copy.deepcopy(code)
                try:
                    out, currParseCode, codeCopy = self.evaluateStatement(subUnit, subParent, codeCopy)
                except IndexError:
                    out = self.FAILED
                if out == self.CONTINUE or out == self.FAILED:
                    if currParseCodeCopy == None:
                        return outCode
                    parseCode.children.extend(currParseCodeCopy.children)
                    return outCode
                #add to the unit
                currParseCodeCopy = copy.deepcopy(currParseCode)
                ct += 1
                subParent.append(unit*ct)
                outCode = codeCopy
    
    #parses grammar rule with reusable subgrammar components 
    def evaluateBrackets(self, unit, code, parseCode):
        return self.evaluateBraces(unit,code,parseCode)
        
    #builds new grammars for grammar with a choice
    def createBonusParenthesisStatements(self,unit,sub):
        index = sub.index(unit)
        out = [] 
        ####infinite loop here
        for val in unit[1:-1].split():
            out.append(sub[:index] + ['~'] +[val] + sub[index+1:])
        return out

############################################################
#THE ACTUAL PARSER!!!!!!!!!
#Parse input token list into tree
def parse(exp, code):
    print("\n################ Tokenizing input...")
    tokens = JavaTokenizer.tokenize(code)
    tokensCopy = copy.deepcopy(tokens)
    print(tokens)
    print("\n############### Parsing Code...")
    block = GrammarData.data[exp]
    print(f"Head Grammar: Name = {block[0]}, Format = {block[1]}")
    p = Parent()
    try:
        final = Node(p,block,tokens)
    except IndexError:
        print('Leftover tokens->', tokens)
        print('Passed?', False)
        print(f'Depth-> INDEX ERROR: Parser expected token but got None')
        return TreeNode('ParseError'), tokensCopy, len(tokens)
    print("Leftover tokens->",final.code)  
    print("Passed?", final.passed)
    depth = final.tokenDepth.initialLength-final.tokenDepth.depth
    print(f'Depth-> {depth}/{final.tokenDepth.initialLength}')
    print('\n##################### Assigning parents and children')
    assignParentsToChildren(final.parseCode)
    final.parseCode.parent = None
    print("\n##################### Printing tree....")
    makeTree(final.parseCode,0)                 
    return final.parseCode, tokensCopy, depth
###############################################################
       
#########TESTING#########

#special object to append the completed parse tree to
class Parent(object):
    
    def __init__(self):
        self.head = "Top Level Parent"
        self.parseCode = TreeNode('Top')
        self.parseCode.parent = None

def testBNF():
    for line in GrammarData.data:
        print(line)
        #input("Press Enter for next line>")
        
#creates a tree in terminal for debug
def makeTree(T, indent):
    print(indent*'  '+"HEAD: "+T.name)
    for i in T.children:
        if isinstance(i,TreeNode):
            makeTree(i, indent + 1)
        else:
            print(indent*'  '+str(i))
            
#recurses through parse tree to assign parent instances to their children
def assignParentsToChildren(parseTree):
    parseTree.giveSelfToChildren()
    for child in parseTree.children:
        if isinstance(child, TreeNode):
            assignParentsToChildren(child)
            
#draws a file format from the tree
def getPathString(trace):
    traceStr = ""
    for val in trace:
        traceStr += str(val)+'|'
    traceStr = traceStr[:-1]
    return traceStr     

def testParse():
    #Test case 1
    code1 = '''  
    public class OddPyramid{   
        public static int SCALE = 13;
        public static void main(String[] args){
            for (int i = 1; i <= SCALE; i += 2){
                System.out.println();
                boolean b = false;
                int a;
            }
        }
        
        public static void printCh(int num, String str){
            for (int i = 1; i <= num; i++){
                System.out.print(str);
            }
        }
    }
    '''
    exp1 = 'TypeDeclaration'
    #Test case 2
    code2 = '''
    public class HelloWorld{
        public static void HelloWorld(String[] args){
            System.out.println("Hello World!");
        }
        
        public static int thisIsATest(int test){
            System.out.println("testing");
            return 1;
        }
    }
    '''

    exp2 = 'TypeDeclaration'
    #Test case 3
    code3 = '''
    a(1 + 3 * (3+2));
    '''
    exp3 = 'Expression3'
    #Test case 4
    code4 = '''
    Student(); 
    '''
    exp4 = 'Creator'
    #parse(exp1,code1)
    #parse(exp2,code2)
    #parse(exp3,code3)
    parse(exp4,code4)
    
#testParse()