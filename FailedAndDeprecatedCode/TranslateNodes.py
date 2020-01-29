from Parser2 import Capturer, NodeCapturer, parse, makeTree, TreeNode
from Token import*
import copy

def translatePrint(tree):
    #exact statement we want replaced in the tree
    capturer = Capturer(Literal)
    printStatement = ['System','.','out','.','println',
                      "(",capturer,')',';']
    replacementStatement = ['print','(',capturer,')']
    translate(tree,printStatement,replacementStatement)
    printStatement = ['System','.','out','.','print',
                      "(",capturer,')',';']
    replacementStatement = ['print','(',capturer,',',"end",'=',"''",')']
    translate(tree,printStatement,replacementStatement)
    
        
def translateClassDeclaration(tree):
    modifier = NodeCapturer("Modifier")
    classBody = NodeCapturer("ClassBody")
    identifier = Capturer(Identifier)
    statement = [modifier, "class", identifier, classBody]
    translated = ['class', identifier, ':', classBody]
    translate(tree,statement,translated)
    
def translateFormalParameterDecls(tree):
    rest = NodeCapturer("FormalParameterDeclsRest")
    statement = [NodeCapturer('Type'),rest]
    translated = [rest]
    translate(tree, statement, translated)
    
def translateIdentifiers(tree):
    identifier = Capturer(Identifier)
    translate(tree,[identifier],[identifier])
    
#removes all token instances from tree
def translateLeftoverTokens(tree):
    i = 0
    while i < len(tree.children):
        node = tree.children[i]
        if isinstance(node, Token):
            tree.children.remove(node)
        else:
            if isinstance(node, TreeNode):
                translateLeftoverTokens(node)
            i += 1
        
def translateStaticVoidMethod(tree):
    modifier = NodeCapturer("Modifier")
    identifier = Capturer(Identifier)
    formalParameterDecls = NodeCapturer("FormalParameterDecls")
    blockStatements = NodeCapturer("BlockStatements")
    statement = [modifier, 'static', 'void', identifier, 
                 '(',formalParameterDecls, ')',
                 '{', blockStatements, '}']
    translatedStatement = ['def', identifier, '(', 'self', ',',
                           formalParameterDecls, ')', ':',
                           blockStatements]
    translate(tree,statement,translatedStatement)
    
def translateMethods(tree):
    translateStaticVoidMethod(tree)
    #translate general methods
    modifier = NodeCapturer("Modifier")
    identifier = Capturer(Identifier)
    formalParameterDecls = NodeCapturer("FormalParameterDecls")
    blockStatements = NodeCapturer("BlockStatements")
    statement = [modifier, 'void', identifier, 
                 '(',formalParameterDecls, ')',
                 '{', blockStatements, '}']
    translatedStatement = ['def', identifier, '(', 'self', ',',
                           formalParameterDecls, ')', ':',
                           blockStatements]
    translate(tree,statement, translatedStatement)
    translateFormalParameterDecls(tree)

    
def translate(tree, java, python):
    while True:
        #find the statement 
        pathList = tree.getStatementPaths(java)
        if pathList == None: 
            print("Statement Not Found->",java)
            return #statement does not exist
        print("Statement Found->",java)
        node = findFatherNode(pathList)
        node.children.clear()
        replacementStatement = []
        for token in python:
            if isinstance(token,Capturer):
                replacementStatement.append(token.value)
            elif isinstance(token,NodeCapturer):
                print(token.name)
                replacementStatement.append(token.node)
            else:
                replacementStatement.append(token)
        node.children.extend(replacementStatement)
    
def findFatherNode(pathList):
    firstPath = pathList[0]
    for i in range(1,len(firstPath)):
        node = firstPath[i]
        for path in pathList:
            if path[i] != node:
                return firstPath[i-1]
    return firstPath[-2] #return second to last element

def getPathString(trace):
    traceStr = ""
    for val in trace:
        traceStr += str(val)+'|'
    traceStr = traceStr[:-1]
    return traceStr

def testTranslator():
    code = '''
public class HelloWorld{
    

    public static void HelloWorld(String[] args){
        System.out.println("Hello World!");
    }

}
'''
    exp = 'ClassOrInterfaceDeclaration'
    tree = parse(exp,code)
    print("\n########### Translating class declarations.....")
    translateClassDeclaration(tree)
    print("\n########### Reprinting tree...")
    #makeTree(tree,0)
    print("\n########### Translating method declarations.....")
    translateMethods(tree)
    print("\n########### Reprinting tree...")
    makeTree(tree,0)
    print("\n########### Translating print statements.....")
    translatePrint(tree)
    print("\n########### Translating identifiers.....")
    translateIdentifiers(tree)
    print("\n########### Reprinting tree...")
    #makeTree(tree,0)
    print("\n########### Translating leftover tokens.....")
    translateLeftoverTokens(tree)
    print("\n########### Reprinting tree...")
    makeTree(tree,0)
    
    #Final form python code:
    print("\n########### Outputing code!")
    print(writePython(tree,0,''))
    
def writePython(tree, indent, out):
    out += '  ' * indent
    if (len(tree.children) == 1 and 
        isinstance(tree.children[0],TreeNode)):
        return writePython(tree.children[0],indent,out)
    else:
        for child in tree.children:
            if isinstance(child,TreeNode):
                out += '\n'
                out = writePython(child,indent+1,out)
            else:
                out += child + ' '
        #out += '\n'
        return out
    
testTranslator()


            