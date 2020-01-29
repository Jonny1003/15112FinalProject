#@Jonathan Ke
#@9/26/2019


#AnnotationTypeDeclaration:
#    @ interface Identifier AnnotationTypeBody

from JavaLang import JavaLang as Java
import JavaTokenizer
from Token import *

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
                out.append((prevLine.strip()[:-1], tuple(sub)))
                sub = []
                prevLine = line
    out.pop(0) #first term is a dud
    return out

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
            i += len(s)
            out.append(" ".join(s))
        elif L[i] != '{' and '{' in L[i]:
            s = []
            for val in L[i:]:
                if val != '}' and '}' in val:
                    s.append(val)
                    break
            i += len(s)
            out.append(" ".join(s))
        else:
            out.append(L[i])
            i+=1
    return out
                
                

def testBreakDownBNF():
    ruleList = breakDownBNF(Java.JavaGrammar2)
    #for r in ruleList:
    #   print(r)   

class GrammarData:
    data = breakDownBNF(Java.JavaGrammar2)      
            
class Node(object):
    def __init__(self, parent, grammarBlock, compareCode, tokenIterator):
        self.head = grammarBlock[0]
        self.body = grammarBlock[1]
        print(self.body)
        self.parent = parent
        self.currentChild = None
        self.code = compareCode
        self.tokenIterator = tokenIterator
        self.tokenIteratorCopy = tokenIterator
        
        #for tracking children visits
        self.bodyIndex = 0
        self.subIndex = -1
        self.inParenthesis = False
        self.inBraces = False
        self.inBrackets = False
        
        print(self.head,"->",self.body)
        
        #start checking children
        self.getNextChild()
       
    def returnToParent(self, boolean, tokenIterator):
        if self.parent == None:
            print("WE MADE IT")
        else:
            self.parent.accept(self,boolean, tokenIterator) 
            
    def returnToSelf(self,boolean):
        if boolean == False and self.bodyIndex >= len(self.body):
            self.returnToParent(False, tokenIterator)
        else:
            self.bodyIndex += 1
            self.tokenIterator = self.tokenIteratorcopy
            self.getNextChild()
            
    #visits a child
    def visit(self, child):
        for block in GrammarData.data:
            if block[0] == child:
                self.currentChild = Node(self,block,self.code)
                return
    
    def accept(self,child,boolean, tokenIterator):
        if boolean == False and self.inParenthesis:
            self.parenthesisIndex += 1
            if self.parenthesisIndex == len(self.parenthesisList):
                #parenthesis condition has failed
                self.returnToSelf(False)
            else: #continue checking potential statements
                self.visit(self.parenthesisList[self.parenthesisIndex])
        elif boolean == False and self.inBrackets:
            self.getNextChild()
        elif boolean == False and self.inBraces:
            self.getNextChild()
        elif boolean == False:
            self.returnToSelf(False)
        else: #the test passed!       
            self.tokenIterator = tokenIterator
            if self.inBraces:
                if (self.braceIndex < len(self.braceList)-1):
                    self.braceIndex +=1
                    self.visit(self.braceList[self.braceIndex])
                else: #whole entire expression passed, try again
                    self.braceIndex = 0
                    self.visit(self.braceList[self.braceIndex])
            elif self.inBrackets and self.bracketIndex < len(self.bracketList)-1:
                self.bracketIndex += 1
                self.visit(self.bracketList[self.bracketIndex])
            else:
                #reset internal iterators
                self.inBraces = False
                self.inBrackets = False
                self.inParenthesis = False
                self.getNextChild()
            
    
    def getNextChild(self):
        if self.nextTerm():
            print("RETURNED",self.head, "to", self.parent.head)
        else:
            term = self.body[self.bodyIndex][self.subIndex]
            self.getChild(term)
        
    def getChild(self, term):
        #check if terminal, nonterminal, or other statement
        print(term)
        if term in ('[',']','(',')','{','}'): #special terminal values
            if self.code[self.tokenIterator].string == term: #we found a match!
                self.tokenIterator += 1
            self.getNextChild()
        #check grammar rule cases
        elif '[' in term: #bracket statements
            self.inBrackets = True
            self.bracketList = term[1:-1].split()
            print(term[1:-1])
            self.bracketIndex = 0
            self.evaluateBracket()
        elif '{' in term: #brace statements
            self.inBraces = True
            self.braceList = term[1:-1].split()
            print(term[1:-1])
            self.braceIndex = 0
            self.visit(self.braceList[self.braceIndex])
        elif '(' in term: #parenthesis statements
            self.inParenthesis = True
            print(term[1:-1])
            self.parenthesisList = term[1:-1].split()
            self.parenthesisIndex = 0
            self.visit(self.parenthesisList[self.parenthesisIndex])
        elif term.isupper(): #terminal variable
            if term == 'IDENTIFIER' and isinstance(self.code[self.tokenIterator],Identifier):
                print(self.code[self.tokenIterator].string)
                self.tokenIterator += 1
                self.getNextChild()
            else:
                self.returnToSelf(False)
        elif term[0].isupper(): #nonterminal
            self.visit(term)
        else: #terminal case
            if self.code[self.tokenIterator].string == term: #we found a match!
                self.tokenIterator += 1
                self.getNextChild()
            else: 
                self.returnToSelf(False)
                
    def evaluateBracket(self):
        self.getChild(self.bracketList[self.bracketindex])
    
    #moves visitor up one, returns True to parent and self if finished     
    def nextTerm(self):
        #move loop forward 1
        self.subIndex += 1
        if self.subIndex >= len(self.body[self.bodyIndex]):
            #finished checking a statement, statement passes!
            print("WE PARSED SOMETHING!-> "+self.head)      
            self.returnToParent(True,self.tokenIterator)    
            return True
        return False
        
        
        
code = '''

public class PrintMyself{
    public static void main(String[] args) throws Exception{
        Scanner con = new Scanner(new File("PrintMyself.java"));
        while (con.hasNextLine()){
            System.out.println(con.nextLine());
            byte b = 'a';
            
        }
        int a = 5;
        int b = ++a;
        b = ++a;
        System.out.println(a);
        System.out.println(b);
    }
    /**
     * 
     * dsjkaldjksjlajdk
     */
    //Obsdjfbwodfnjsnvlknffenvljnwfjlvnefjlbnefjlfvnerwkfidsodjfnakdnkasnvnfovoae
}


'''
code = 'import java.util.Scanner;'

def main(code):
    tokens = JavaTokenizer.tokenize(code)
    for block in GrammarData.data:
            if block[0] == 'ImportDeclaration':
                final = Node(None,block,tokens,0)
                return "DONE"
    
print(main(code))

def checkLiteral(term):
    if term in ('true','false','null'):
        return True
    elif term.isalpha():
        return True
    elif term[0] == term[-1] :
        if term[0] == '''"''':
            return True
        elif len(term) == 3 or term[1:-1] in ["\\","\\n","\\t"]:
            return True
    return False
    