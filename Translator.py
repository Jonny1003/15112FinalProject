######
#@Jonathan ke
#@12/2/2019

from Parser2 import parse, makeTree
from TreeNode import *
from Token import*
import copy

##########################################################
#Translations from Java syntax to Python syntax

#base class 
class Translations(object):
    
    def __init__(self, translation):
        self.old = translation[0]
        self.new = translation[1]
        
class Println(Translations):
    def __init__(self):
        capturer = NodeCapturer('IdentifierSuffix')
        super().__init__((['System','.','out','.','println', capturer],
                          ['print',capturer]))
        
class Print(Translations):
    def __init__(self):
        capturer = NodeCapturer('IdentifierSuffix')
        super().__init__((['System','.','out','.','print', capturer],
                          ['print',capturer]))
        
class IdentifierMethodChain(object):
    def __init__(self):
        self.translations = []
        'Identifier { . Identifier } [IdentifierSuffix]'
        for i in range(10,-1,-1):    
            idSuffix = NodeCapturer('IdentifierSuffix')
            id1 = Capturer(Identifier)
            match = [id1]
            for j in range(i):
                match.extend(['.',Capturer(Identifier)])
            match.append(idSuffix)
            translate = ['self','.']+match
            self.translations.append(Translations((match, translate)))
        
class PostFixOps(object):
    def __init__(self):
        self.translations = [Translations((['++'], ['+=','1'])), 
                             Translations((['--'], ['-=', '1']))]
        
class PrefixOps(object):
    def __init__(self):
        self.translations = [Translations((['!'], ['not']))]
        
class Expression3(object):
    def __init__(self):
        expr3 = NodeCapturer('Expression3')
        expr3Pt2 = NodeCapturer('Expression3')
        self.translations = [Translations((['--', expr3], [expr3, '-=', '1'])),
                             Translations((['++', expr3], [expr3, '+=', '1']))]
        
class ClassOrInterfaceDeclaration(Translations):
    def __init__(self):
        capturer0 = NodeCapturer('Modifier')
        capturer1 = NodeCapturer('ClassDeclaration')
        super().__init__(([capturer0, capturer1],
                          [capturer1]))
        
class ClassBodys(Translations):
    def __init__(self):
        numBodyStatements = 100
        self.translations = []
        for i in range(numBodyStatements):
            bodys = [NodeCapturer('ClassBodyDeclaration') for j in range(i)]
            classBody = ['{']+bodys+['}']
            self.translations.append(
                Translations((classBody, bodys)))
        
class NormalClassDeclaration(Translations):
    def __init__(self):
        cap = Capturer(Identifier)
        body = NodeCapturer('ClassBody')
        super().__init__((['class',cap,body],
                          ['class',cap,':',body]))
        
class LocalVariableDeclarationStatement(Translations):
    def __init__(self):
        typeCap = NodeCapturer('Type')
        decl = NodeCapturer('VariableDeclarators')
        super().__init__(([typeCap,decl,';'],
                          [decl]))
        

class ClassBodyDeclarations(Translations):
    def __init__(self):
        self.translations = []
        numModifiers = 12
        for i in range(numModifiers+1):
            orig = [NodeCapturer('Modifier') for j in range(i)]
            memb = NodeCapturer('MemberDecl')
            orig.append(memb)
            self.translations.append(Translations(
                (orig, [memb])))
            
class MemberDecl(Translations):
    def __init__(self):
        methodDeclRest = NodeCapturer("VoidMethodDeclaratorRest")
        name = Capturer(Identifier)
        super().__init__((['void',name,methodDeclRest], 
                          ['def', name, methodDeclRest]))
        
class VoidMethodDeclaratorRest(Translations):
    def __init__(self):
        formalParam = NodeCapturer('FormalParameters')
        block = NodeCapturer('Block')
        match = [formalParam, block]
        translation = [formalParam, ':', block]
        super().__init__((match,translation))
        
class FormalParameterDecls(Translations):
    def __init__(self):
        typeVal = NodeCapturer("Type")
        declRest = NodeCapturer('FormalParameterDeclsRest')
        super().__init__(([typeVal, declRest], 
                          [declRest]))

class Block(Translations):
    def __init__(self):
        statements = NodeCapturer('BlockStatements')
        super().__init__((['{',statements,'}'],
                          [statements]))
        
class Statement(Translations):
    def __init__(self):
        stateExpr = NodeCapturer('StatementExpression')
        super().__init__(([stateExpr,';'],
                          [stateExpr]))
        
class VariableDeclarator(Translations):
    def __init__(self):
        identifier = Capturer(Identifier)
        super().__init__(([identifier],[]))
        
class FormalParameters(object):
    def __init__(self):
        formalParams = NodeCapturer('FormalParameterDecls')
        match = ['(',formalParams,')']
        translation = ['(','self',',',formalParams,')']
        self.translations = [Translations((match,translation))]
        self.translations.append(Translations((['(',')'],['(','self',')'])))
        
class StatementFor(Translations):
    def __init__(self):
        forControl = NodeCapturer('ForControl')
        statement = NodeCapturer('Statement')
        match = ['for','(',forControl,')',statement]
        translate = [forControl, ':', statement]
        super().__init__((match,translate))
        
class ForVarControl(Translations):
    def __init__(self):
        typeCap = NodeCapturer('Type')
        varDeclIdCap = NodeMover('VariableDeclaratorId', 'BlockStatements', 
                                 childBehind = 'BlockStatement',
                                 changeName = 'BlockStatement')
        rest = NodeCapturer('ForVarControlRest')
        match = [typeCap, varDeclIdCap, rest]
        translate = [varDeclIdCap, rest]
        super().__init__((match,translate))
        
class ForVarControlRest(Translations):
    def __init__(self):
        declRest = NodeMover('ForVariableDeclaratorsRest', 'BlockStatements',
                             childBehind = 'BlockStatement')
        exp = NodeCapturer('ForControlExp')
        update = NodeMover('ForUpdate', 'Statement', changeName = 'BlockStatement')
        match = [declRest,';',exp,';',update]
        translate = [declRest, 'while', exp, update]
        super().__init__((match,translate))
        
class ForVarControlRestEmpty1(Translations):
    def __init__(self):
        declRest = NodeMover('ForVariableDeclaratorsRest', 'BlockStatements',
                             childBehind = 'BlockStatement')
        update = NodeMover('ForUpdate', 'Statement', changeName = 'BlockStatement')
        match = [declRest,';',';',update]
        translate = [declRest, 'while', 'True', update]
        super().__init__((match,translate))
        
class ForVarControlRestEmpty2(Translations):
    def __init__(self):
        declRest = NodeMover('ForVariableDeclaratorsRest', 'BlockStatements',
                             childBehind = 'BlockStatement')
        exp = NodeCapturer('ForControlExp')
        match = [declRest,';', exp, ';']
        translate = [declRest, 'while', exp]
        super().__init__((match,translate))
        
class ForVarControlRestEmpty3(Translations):
    def __init__(self):
        declRest = NodeMover('ForVariableDeclaratorsRest', 'BlockStatements',
                             childBehind = 'BlockStatement')
        match = [declRest,';', ';']
        translate = [declRest, 'while', 'True']
        super().__init__((match,translate))
        
class StatementReturnNone(Translations):
    def __init__(self):
        super().__init__((['return',';'],['return']))
                         
class StatementReturn(Translations):
    def __init__(self):
        expr = NodeCapturer('Expression')
        super().__init__((['return',expr,';'],['return',expr]))
    
class StatementWhile(Translations):
    #while ParExpression Statement
    def __init__(self):
        parExpr = NodeCapturer('ParExpression')
        statement = NodeCapturer('Statement')
        super().__init__((['while', parExpr, statement],
                          ['while', parExpr, ':', statement]))
        
class StatementIf(Translations):
    def __init__(self):
        #if ParExpression Statement [else Statement] 
        parExpr = NodeCapturer('ParExpression')
        statement = NodeCapturer('Statement')
        match = ['if', parExpr, statement]
        translate = ['if', parExpr,':', statement]
        super().__init__((match,translate))
        
class StatementIfElse(Translations):
    def __init__(self):
        #if ParExpression Statement [else Statement] 
        parExpr = NodeCapturer('ParExpression')
        statement = NodeCapturer('Statement')
        elseStatement = NodeMover('ElseStatement','BlockStatement',
                                  childAhead = 'Statement',
                                  changeName = 'Statement')
        match = ['if', parExpr, statement, elseStatement]
        translate = ['if', parExpr, ':', statement, elseStatement]
        super().__init__((match,translate))
        
class StatementElse(Translations):
    def __init__(self):
        statement = NodeCapturer('Statement')
        match = ['else', statement]
        translate = ['else', ':', statement]
        super().__init__((match, translate))
        
class StatementEmpty(Translations):
    def __init__(self):
        super().__init__(([';'],[]))
        
class StatementBreak(Translations):
    def __init__(self):
        super().__init__((['break',';'],['break']))
        
class StatementDoWhile(Translations):
    def __init__(self):
        # do Statement while ParExpression ;
        statement = NodeCapturer('Statement')
        whileSub = NodeCapturer('WhileSubStatement', changeName = 'Statement')
        match = ['do', statement, whileSub, ';']
        translate = [statement, whileSub, ':', statement]
        super().__init__((match, translate))
        
class WhileSubStatement(Translations):
    def __init__(self):
        #while ParExpression -> converted to statement
        parExpr = NodeCapturer('ParExpression')
        match = ['while', parExpr]
        translate = ['while', parExpr]
        super().__init__((match, translate))
        
class PrimaryNew(Translations):
    def __init__(self):
        creator = NodeCapturer('Creator')
        match = ['new', creator]
        translate = [creator]
        super().__init__((match, translate))
        
class PrimaryLiteral(Translations):
    def __init__(self):
        lit = Capturer(Literal)
        super().__init__(([lit],[lit]))
        
class CreatorArray(Translations):
    def __init__(self):
        # Type [ Literal ] 
        TYPE = NodeCapturer('Type')
        expr = NodeCapturer('Expression')
        match = [TYPE, '[', expr, ']']
        translate = ['[', 'None', 'for', 'i', 'in', 'range','(', expr, ')', ']']
        super().__init__((match, translate))
        
class MethodOrFieldDeclarator1(Translations):
    def __init__(self):
        TYPE = NodeCapturer('Type')
        identifier = Capturer(Identifier)
        rest = NodeCapturer('MethodDeclaratorRest')
        match = [TYPE, identifier, rest]
        translate = ['def', identifier, rest]
        super().__init__((match, translate))
        
class MethodOrFieldDeclarator2(Translations):
    def __init__(self):
        TYPE = NodeCapturer('Type')
        identifier = Capturer(Identifier)
        rest = NodeCapturer('FieldDeclaratorsRest')
        match = [TYPE, identifier, rest, ';']
        translate = [identifier, rest]
        super().__init__((match, translate))
        
class MethodDeclaratorRest(Translations):
    def __init__(self):
        '''MethodDeclaratorRest: 
               FormalParameters Block 
        '''
        parameters = NodeCapturer('FormalParameters')
        block = NodeCapturer('Block')
        match = [parameters, block]
        translate = [parameters, ':', block]
        super().__init__((match, translate))
        
class MethodOrFieldRest(Translations):
    def __init__(self):
        'FieldDeclaratorsRest ;'
        decl = NodeCapturer('FieldDeclaratorsRest')
        match = [decl, ';']
        translate = [decl]
        super().__init__((match, translate))
        
class FieldDeclaratorsRestTranslations(object):
    def __init__(self):
        'VariableDeclaratorRest { , VariableDeclarator }'
        self.translations = []
        for i in range(1,15):
            first = NodeCapturer('VariableDeclaratorRest')     
            match = [first]
            for j in range(i):
                match.extend([',', NodeMover('VariableDeclarator', 'ClassBody',
                                             changeName = 'ClassBodyDeclaration')])
            translate = [i for i in match if i != ',']
            self.translations.append(Translations((match, translate)))
        self.translations.reverse()
        
class ConstructDecl(Translations):
    def __init__(self):
        identifier = Capturer(Identifier)
        rest = NodeCapturer('ConstructorDeclaratorRest')
        match = [identifier, rest]
        translate = ['__init__', rest]
        super().__init__((match, translate))
        
class ConstructorDeclaratorRest(Translations):
    def __init__(self):
        param = NodeCapturer('FormalParameters')
        block = NodeCapturer('Block')
        match = [param, block]
        translate = [param, ':', block]
        super().__init__((match, translate))
        
class HashCode(Translations):
    def __init__(self):
        rest = NodeCapturer('MethodDeclaratorRest')
        TYPE = NodeCapturer('Type')
        match = [TYPE, 'hashCode', rest]
        translate = ['__hash__', rest]
        super().__init__((match, translate))
        
class ToString(Translations):
    def __init__(self):
        rest = NodeCapturer('MethodDeclaratorRest')
        TYPE = NodeCapturer('Type')
        match = [TYPE, 'toString', rest]
        translate = ['__repr__', rest]
        super().__init__((match, translate))
        
class VariableDeclarators(object):
    
    def __init__(self):
        'VariableDeclarator { , VariableDeclarator }'
        self.translations = []
        for i in range(1,15):     
            first = NodeCapturer('VariableDeclarator')
            match = [first]
            for j in range(i):
                match.extend([',', NodeMover('VariableDeclarator', 'BlockStatements',
                                             changeName = 'BlockStatementVariableDeclarator')])
            translate = [i for i in match if i != ',']
            self.translations.append(Translations((match, translate)))
        self.translations.reverse()
        
         
######################################################################## 
        
#Dictionary of all translations implemented
class TranslateDictionary(object):
    main = {
        'Primary': [Println(), Print(), PrimaryNew(), PrimaryLiteral()]+IdentifierMethodChain().translations,
        'ClassOrInterfaceDeclaration': [ClassOrInterfaceDeclaration()],
        'ClassBody': ClassBodys().translations,
        'NormalClassDeclaration': [NormalClassDeclaration()],
        'ClassBodyDeclaration': ClassBodyDeclarations().translations,
        'MemberDecl': [MemberDecl(), ConstructDecl()],
        'VoidMethodDeclaratorRest': [VoidMethodDeclaratorRest()],
        'MethodOrFieldDecl': [HashCode(), ToString(), MethodOrFieldDeclarator2(),
                              MethodOrFieldDeclarator1()],
        'FieldDeclaratorsRest': FieldDeclaratorsRestTranslations().translations,
        'MethodOrFieldRest': [MethodOrFieldRest()],
        'MethodDeclaratorRest': [MethodDeclaratorRest()],
        'ConstructorDeclaratorRest': [ConstructorDeclaratorRest()],
        'FormalParameters': FormalParameters().translations,
        'FormalParameterDecls': [FormalParameterDecls()],
        'Block': [Block()],
        'Statement': [Statement(), StatementFor(), StatementReturnNone(),
                      StatementReturn(), StatementIfElse(), StatementIf(),
                      StatementElse(), StatementEmpty(), StatementBreak(),
                      StatementDoWhile(), WhileSubStatement()],
        'LocalVariableDeclarationStatement': [LocalVariableDeclarationStatement()],
        'PostfixOp': PostFixOps().translations,
        'VariableDeclarators': VariableDeclarators().translations,
        'VariableDeclarator': [VariableDeclarator()],
        'PrefixOp': PrefixOps().translations,
        'Expression3': Expression3().translations,
        'ForVarControl': [ForVarControl()],
        'ForVarControlRest': [ForVarControlRest(), ForVarControlRestEmpty1(),
                              ForVarControlRestEmpty2(), ForVarControlRestEmpty3()],
        'Creator': [CreatorArray()],
        'BlockStatementVariableDeclarator': [VariableDeclarator()]
    }

#recursively traverses tree and translates each node using dictionary
def traverseAndTranslate(tree, translations):
    if tree.name in translations:
        translate(tree,translations[tree.name])
    for child in tree.children:
        if isinstance(child, TreeNode):
            traverseAndTranslate(child,translations)
        elif isinstance(child, Token):
            i = tree.children.index(child)
            tree.children[i] = child.string

#translates a node using translations
def translate(tree, translations):
    for translation in translations:
        matchStatement = translation.old
        if match(tree, matchStatement):
            tree.children.clear()
            for newVal in translation.new:
                if isinstance(newVal, NodeMover):
                    newVal.moveToNewParent()
                elif isinstance(newVal, NodeCapturer):
                    print(newVal)
                    tree.children.append(newVal.node)
                elif isinstance(newVal, Capturer):
                    tree.children.append(newVal.value)
                else: #newVal is a string
                    tree.children.append(newVal)
            return

#boolean checker: translation matches node 
def match(tree, translation):
    children = tree.children
    i = 0
    while i < len(translation):
        if i >= len(children): return False
        child = children[i]
        comp = translation[i]
        if isinstance(child, Token):
            if isinstance(comp, str) and child.string != comp:
                return False
            elif isinstance(comp, Capturer):
                if isinstance(child,comp.tokenType):
                    comp.capture(child.string)
                else: return False
            elif isinstance(comp, NodeCapturer):
                return False
        elif isinstance(child, TreeNode):
            if isinstance(comp, str) or isinstance(comp, Capturer):
                return False
            elif isinstance(comp, NodeCapturer):
                if comp.name == child.name:
                    comp.capture(child)
                else: 
                    return False
        else: return False
        i += 1
    if i < len(children): return False
    print("Matched!",translation,'\n\t', end = '')
    for child in children: print(child,end = ', ')
    print()
    return True

#takes Python tree and creates legal Python script
def writePython(tree, indent, out):
    newLine = False
    if (len(tree.children) == 1 and 
        isinstance(tree.children[0],TreeNode)):
        if tree.children[0].name not in {'BlockStatement','ClassBodyDeclaration',
                                         'BlockStatementVariableDeclarator'}:
            return(writePython(tree.children[0],indent, out))
    for child in tree.children:
        if isinstance(child,TreeNode):
            if (child.name == 'BlockStatement' or child.name == 'Statement' or 
                child.name == 'BlockStatementVariableDeclarator'):
                out += '\n'+indent*'    '
            elif child.name == 'ClassBodyDeclaration':
                newLine = True
                out += '\n'+indent*'    '
            out = writePython(child,indent, out)
        elif child == ':':
            newLine = True
            indent += 1
            out += ':'
        else:
            out += child + ' '
    if newLine: 
        out += '\n'
    return out

#tokenizes, parses, then compiles Java code to Python code
def compile(code):
    exp = 'ClassOrInterfaceDeclaration'
    tree, tokenizedInput, depth = parse(exp, code)
    treeCopy = copy.deepcopy(tree)
    dictionary = TranslateDictionary.main
    traverseAndTranslate(treeCopy,dictionary)
    traverseAndTranslate(treeCopy,dictionary) #recheck translations for nodeMovements
    return writePython(treeCopy, 0, ''), tree, treeCopy, tokenizedInput, depth
    
def testTranslator():
    code = '''
// Java program to demonstrate working of 
// hasCode() and toString() 
public class Student 
{ 

  
    // Constructor 
    Student() 
    { 
        roll_no = last_roll; 
        last_roll++; 
    } 
  
    // Overriding hashCode() 
    
    public int hashCode() 
    { 
        return roll_no; 
    } 
  
    // Driver code 
    public static void main(String args[]) 
    { 
        Student s = new Student(); 
  
        // Below two statements are equivalent 
        System.out.println(s); 
        System.out.println(s.toString()); 
    } 
} 
'''

    exp = 'ClassOrInterfaceDeclaration'
    tree, tokens, depth = parse(exp,code)
    
    print('\n################## translating...')
    treeCopy = copy.deepcopy(tree)
    dictionary = TranslateDictionary.main
    traverseAndTranslate(treeCopy,dictionary)
    traverseAndTranslate(treeCopy,dictionary) #recheck translations for nodeMovements
    print('\n################## printing translation')
    makeTree(treeCopy,0)
    print('\n################## resulting code')
    print(writePython(treeCopy,0,""))
    
#testTranslator()
    
    
        