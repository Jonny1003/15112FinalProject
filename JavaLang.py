#@Jonathan Ke (jak2)
#@9/26/2019
#
#Names groupings and lists of Java syntax and diction
#implements Java grammar rules
#Includes functions for updating JavaGrammar text file with editing functions and grammar prioritization
#algorithms. Functions are called by MochaPythonIDE
#
#lists not completed!!!!!!

from TreeNode import TreeNode
from Token import *


class JavaLang(object):
    keywords = tuple("""abstract	assert	boolean	 break
                    byte	case	catch	char
                    class	const	continue	default
                    do	double	else	enum
                    extends	final	finally	float
                    for	goto	if	implements
                    import	instanceof	int interface
                    long	native	new	package
                    private	protected	public	return
                    short	static	strictfp	super   
                    switch	synchronized	this	throw
                    throws	transient	try	void
                    volatile	while""".split())
    
    primitives = tuple("""
                        int boolean double byte
                        float char short long
                         """.split())
    
    separators = tuple(".,;{}[]()")

    operators = tuple(reversed("""
    =	>	<	!	~	?	:	 	 	 	 
    ==	<=	>=	!=	&&	||	++	--	 	 	 
    +	-	*	/	&	|	^	%	<<	>>	>>>
    +=	-=	*=	/=	&=	|=	^=	%=	<<=	>>=	>>=
    """.split()))
    
    keywordsLang = "' | '".join(keywords)
    separatorLang = "' | '".join(separators)
    operatorsLang = "' | '".join(operators)
    primitivesLang = "' | '".join(primitives)
    
    
    
    JavaGrammar2 = '''Identifier:
    IDENTIFIER

QualifiedIdentifier:
    Identifier { . Identifier }

QualifiedIdentifierList: 
    QualifiedIdentifier { , QualifiedIdentifier }

CompilationUnit: 
    [[Annotations] package QualifiedIdentifier ;] {ImportDeclaration} {TypeDeclaration}

ImportDeclaration: 
    import [static] Identifier { . Identifier } [. *] ;

TypeDeclaration: 
    ClassOrInterfaceDeclaration
    ;

ClassOrInterfaceDeclaration: 
    {Modifier} (ClassDeclaration | InterfaceDeclaration)

ClassDeclaration: 
    NormalClassDeclaration
    EnumDeclaration

InterfaceDeclaration: 
    NormalInterfaceDeclaration
    AnnotationTypeDeclaration



NormalClassDeclaration: 
    class Identifier [TypeParameters] [extends Type] [implements TypeList] ClassBody

EnumDeclaration:
    enum Identifier [implements TypeList] EnumBody

NormalInterfaceDeclaration: 
    interface Identifier [TypeParameters] [extends TypeList] InterfaceBody

AnnotationTypeDeclaration:
    @ interface Identifier AnnotationTypeBody

Type:
    BasicType { [ ] }
    ReferenceType  { [ ] }

BasicType: 
    byte
    short
    char
    int
    long
    float
    double
    boolean

ReferenceType:
    Identifier [TypeArguments] { . Identifier [TypeArguments] }

TypeArguments: 
    < TypeArgument { , TypeArgument } >

TypeArgument:  
    ReferenceType
    ? [ (extends | super) ReferenceType ]

NonWildcardTypeArguments:
    < TypeList >

TypeList:  
    ReferenceType { , ReferenceType }



TypeArgumentsOrDiamond:
    < > 
    TypeArguments

NonWildcardTypeArgumentsOrDiamond:
    < >
    NonWildcardTypeArguments



TypeParameters:
    < TypeParameter { , TypeParameter }        >

TypeParameter:
    Identifier [extends Bound]

Bound:  
    ReferenceType { & ReferenceType }

Modifier: 
    Annotation
    public
    protected
    private
    static 
    abstract
    final
    native
    synchronized
    transient
    volatile
    strictfp

Annotations:
    Annotation {Annotation}

Annotation:
    @ QualifiedIdentifier [( [AnnotationElement] )]

AnnotationElement:
    ElementValuePairs
    ElementValue

ElementValuePairs:
    ElementValuePair { , ElementValuePair }

ElementValuePair:
    Identifier = ElementValue
    
ElementValue:
    Annotation
    Expression1 
    ElementValueArrayInitializer

ElementValueArrayInitializer:
    { [ElementValues] [,] }

ElementValues:
    ElementValue { , ElementValue }

ClassBody: 
    { {ClassBodyDeclaration} }

ClassBodyDeclaration:
    ; 
    {Modifier} MemberDecl
    [static] Block

MemberDecl:
    MethodOrFieldDecl
    void Identifier VoidMethodDeclaratorRest
    Identifier ConstructorDeclaratorRest
    GenericMethodOrConstructorDecl
    ClassDeclaration
    InterfaceDeclaration

MethodOrFieldDecl:
    Type Identifier MethodOrFieldRest

MethodOrFieldRest:  
    FieldDeclaratorsRest ;
    MethodDeclaratorRest

FieldDeclaratorsRest:  
    VariableDeclaratorRest { , VariableDeclarator }

MethodDeclaratorRest:
    FormalParameters { [ ] } [throws QualifiedIdentifierList] (Block | ;)

VoidMethodDeclaratorRest:
    FormalParameters [throws QualifiedIdentifierList] (Block | ;)

ConstructorDeclaratorRest:
    FormalParameters [throws QualifiedIdentifierList] Block

GenericMethodOrConstructorDecl:
    TypeParameters GenericMethodOrConstructorRest

GenericMethodOrConstructorRest:
    (Type | void) Identifier MethodDeclaratorRest
    Identifier ConstructorDeclaratorRest

InterfaceBody: 
    { {InterfaceBodyDeclaration} }

InterfaceBodyDeclaration:
    ; 
    {Modifier} InterfaceMemberDecl

InterfaceMemberDecl:
    InterfaceMethodOrFieldDecl
    void Identifier VoidInterfaceMethodDeclaratorRest
    InterfaceGenericMethodDecl
    ClassDeclaration
    InterfaceDeclaration

InterfaceMethodOrFieldDecl:
    Type Identifier InterfaceMethodOrFieldRest

InterfaceMethodOrFieldRest:
    ConstantDeclaratorsRest ;
    InterfaceMethodDeclaratorRest

ConstantDeclaratorsRest: 
    ConstantDeclaratorRest { , ConstantDeclarator }

ConstantDeclaratorRest: 
    { [ ] } = VariableInitializer

ConstantDeclarator: 
    Identifier ConstantDeclaratorRest

InterfaceMethodDeclaratorRest:
    FormalParameters { [ ] } [throws QualifiedIdentifierList] ; 

VoidInterfaceMethodDeclaratorRest:
    FormalParameters [throws QualifiedIdentifierList] ;  

InterfaceGenericMethodDecl:
    TypeParameters (Type | void) Identifier InterfaceMethodDeclaratorRest

FormalParameters: 
    ( [FormalParameterDecls] )

FormalParameterDecls: 
    {VariableModifier}  Type FormalParameterDeclsRest

VariableModifier:
    final
    Annotation

FormalParameterDeclsRest: 
    VariableDeclaratorId [, FormalParameterDecls]
    ... VariableDeclaratorId



VariableDeclaratorId:
    Identifier { [ ] }



VariableDeclarators:
    VariableDeclarator { , VariableDeclarator }

VariableDeclarator:
    Identifier [VariableDeclaratorRest]

VariableDeclaratorRest:
    { [ ] } [= VariableInitializer]

VariableInitializer:
    ArrayInitializer
    Expression

ArrayInitializer:
    {ArrayInitializerSub}
    
ArrayInitializerSub:
    { [ VariableInitializer { , VariableInitializer } [,] ] }

Block: 
    { {BlockStatements} }

BlockStatements: 
    {BlockStatement}

BlockStatement:
    LocalVariableDeclarationStatement
    ClassOrInterfaceDeclaration
    Statement

LocalVariableDeclarationStatement:
    {VariableModifier}  Type VariableDeclarators ;

Statement:
    Block
    ;
    Identifier : Statement
    StatementExpression ;
    if ParExpression Statement [ElseStatement] 
    assert Expression [: Expression] ;
    switch ParExpression { SwitchBlockStatementGroups } 
    while ParExpression Statement
    do Statement WhileSubStatement ;
    for ( ForControl ) Statement
    break [Identifier] ;
    continue [Identifier] ;
    return [Expression] ;
    throw Expression ;
    synchronized ParExpression Block
    try Block (Catches | [Catches] Finally)
    try ResourceSpecification Block [Catches] [Finally]
    
WhileSubStatement:
    while ParExpression
    
ElseStatement:
    else Statement

StatementExpression: 
    Expression

Catches:
    CatchClause { CatchClause }

CatchClause:  
    catch ( {VariableModifier} CatchType Identifier ) Block

CatchType:
    QualifiedIdentifier { | QualifiedIdentifier }

Finally:
    finally Block

ResourceSpecification:
    ( Resources [;] )

Resources:
    Resource { ; Resource }

Resource:
    {VariableModifier} ReferenceType VariableDeclaratorId = Expression 

SwitchBlockStatementGroups: 
    { SwitchBlockStatementGroup }

SwitchBlockStatementGroup: 
    SwitchLabels BlockStatements

SwitchLabels:
    SwitchLabel { SwitchLabel }

SwitchLabel: 
    case Expression :
    case EnumConstantName :
    default :

EnumConstantName:
    Identifier



ForControl:
    ForVarControl
    ForInit ; [Expression] ; [ForUpdate]
    
ForControlExp:
    Expression

ForVarControl:
    {VariableModifier} Type VariableDeclaratorId  ForVarControlRest

ForVarControlRest:
    ForVariableDeclaratorsRest ; [ForControlExp] ; [ForUpdate]
    : Expression

ForVariableDeclaratorsRest:
    [= VariableInitializer] { , VariableDeclarator }

ForInit: 
ForUpdate:
    StatementExpression

Expression: 
    Expression1 [AssignmentOperator Expression1]

AssignmentOperator: 
    = 
    +=
    -= 
    *=
    /=
    &=
    |=
    ^=
    %=
    <<=
    >>=
    >>>=

Expression1: 
    Expression2 [Expression1Rest]

Expression1Rest: 
    ? Expression : Expression1

Expression2:
    Expression3 [Expression2Rest]

Expression2Rest:
    { InfixOp Expression3 }
    instanceof Type

InfixOp: 
    || 
    &&
    |
    ^
    &
    ==
    !=
    <
    >
    <=
    >=
    <<
    >>
    >>>
    +
    -
    *
    /
    %

Expression3: 
    ++ Expression3
    -- Expression3
    PrefixOp Expression3
    ( (Expression | Type) ) Expression3
    Primary {Selector} {PostfixOp}

PrefixOp: 
    !
    ~
    +
    -

PostfixOp: 
    ++
    --

Primary: 
    Literal
    ParExpression
    Identifier { . Identifier } [IdentifierSuffix]
    this [Arguments]
    super SuperSuffix
    new Creator
    NonWildcardTypeArguments (ExplicitGenericInvocationSuffix | this Arguments)
    BasicType { [ ] } . class
    void . class



Literal:
    IntegerLiteral
    FloatingPointLiteral
    CharacterLiteral 	
    StringLiteral 	
    BooleanLiteral
    NullLiteral

ParExpression: 
    ( Expression )

Arguments:
    ( [ArgumentsSub] )
    
ArgumentsSub:
    Expression { , Expression }

SuperSuffix: 
    Arguments 
    . Identifier [Arguments]

ExplicitGenericInvocationSuffix: 
    super SuperSuffix
    Identifier Arguments

Creator:  
    Type [ Expression ] 
    NonWildcardTypeArguments CreatedName ClassCreatorRest
    [CreatedName] (ClassCreatorRest | ArrayCreatorRest)

CreatedName:   
    Identifier [TypeArgumentsOrDiamond] { . Identifier [TypeArgumentsOrDiamond] }

ClassCreatorRest: 
    Arguments [ClassBody]

ArrayCreatorRest:
    [ (] { [ ] } ArrayInitializer  |  Expression ] {[ Expression ]} { [ ] })



IdentifierSuffix:
    Arguments 
    IdentifierSuffixSub
    . (class | ExplicitGenericInvocation | this)
    . new [NonWildcardTypeArguments] InnerCreator
    . super Arguments 
    
IdentifierSuffixSub:
    { [ ] } . class 
    Expression

ExplicitGenericInvocation:
    NonWildcardTypeArguments ExplicitGenericInvocationSuffix

InnerCreator:  
    Identifier [NonWildcardTypeArgumentsOrDiamond] ClassCreatorRest



Selector:
    . Identifier [Arguments]
    . ExplicitGenericInvocation
    . this
    . super SuperSuffix
    . new [NonWildcardTypeArguments] InnerCreator
    [ Expression ]

EnumBody:
    { [EnumConstants] [,] [EnumBodyDeclarations] }

EnumConstants:
    EnumConstant
    EnumConstants , EnumConstant

EnumConstant:
    [Annotations] Identifier [Arguments] [ClassBody]

EnumBodyDeclarations:
    ; {ClassBodyDeclaration}


AnnotationTypeBody:
    { [AnnotationTypeElementDeclarations] }

AnnotationTypeElementDeclarations:
    AnnotationTypeElementDeclaration
    AnnotationTypeElementDeclarations AnnotationTypeElementDeclaration

AnnotationTypeElementDeclaration:
    {Modifier} AnnotationTypeElementRest

AnnotationTypeElementRest:
    Type Identifier AnnotationMethodOrConstantRest ;
    ClassDeclaration
    InterfaceDeclaration
    EnumDeclaration  
    AnnotationTypeDeclaration

AnnotationMethodOrConstantRest:
    AnnotationMethodRest
    ConstantDeclaratorsRest  

AnnotationMethodRest:
    ( ) [[ ]] [default ElementValue]

'''

    '''
    @staticmethod
    #DO NOT USE!!!!!!!!!!!!!!! Will edit JavaGrammar file in horrible ways... DONT TOUCH!
    def tagGrammarLinesStart():
        javaFile = open('JavaGrammar', 'r')
        javaGrammar = javaFile.read().splitlines()
        javaFile.close()
        for i in range(len(javaGrammar)):
            line = javaGrammar[i]
            if line != '' and line[0] == ' ': #valid line
                line += ' 0'
                javaGrammar[i] = line
        javaFile = open('JavaGrammar', 'w')
        for line in javaGrammar:
            javaFile.write(line+'\n')
        javaFile.close()
    '''
    
    #updates JavaGrammar with analytics from javaTree structure
    @staticmethod
    def updateGrammar(javaTree):
        #get all grammars used in captureGrammars
        treeGrammars = dict()
        JavaLang.captureGrammars(javaTree, treeGrammars)
        #open grammar file
        javaFile = open('JavaGrammar', 'r')
        javaGrammar = javaFile.read().splitlines()
        javaFile.close()
        #create dictionary of grammars for searching
        ordering, grammarDict = JavaLang.createCurrentGrammarDict(javaGrammar)
        #add children grammars in parents, update orderings of grammar
        for grammar in treeGrammars:
            possGrammars = grammarDict[grammar]
            for child in treeGrammars[grammar]:
                for struct in possGrammars:
                    if child == struct[:-1]: #last value in struct is occurence count
                        struct[-1] = str(int(struct[-1])+1)
                        break
                    #cannot add new grammar definitions due 
                    #to limitations in expression parsing :(
                    #the grammar implemented to parse Java has its limitations sadly...
            #merge sort children and set to grammar key
            grammarDict[grammar] = JavaLang.mergeSortGrammars(possGrammars)
        #rewrite grammar file
        file = open('JavaGrammar','w+')
        for grammarName in ordering:
            file.write(grammarName+'\n')
            for struct in grammarDict[grammarName]:
                file.write('\t'+' '.join(struct)+'\n')
            file.write('\n')
        file.close()
                
    #sorts the grammar specifications for a certain grammar structure
    #using merge sort algorithm, implemented recursively      
    @staticmethod            
    def mergeSortGrammars(L):
        if len(L) <= 1:
            return L
        half = len(L)//2
        L1 = JavaLang.mergeSortGrammars(L[:half])
        L2 = JavaLang.mergeSortGrammars(L[half:])
        out = []
        i1 = 0
        i2 = 0
        while True:
            if i1 >= len(L1):
                out.extend(L2[i2:])
                return out
            elif i2 >= len(L2):
                out.extend(L1[i1:])
                return out
            if int(L1[i1][-1]) > int(L2[i2][-1]):
                out.append(L1[i1])
                i1 += 1
            else:
                out.append(L2[i2])
                i2 += 1
                
    #takes grammar specification and breaks it down into a dictionary 
    #and ordered list        
    @staticmethod
    def createCurrentGrammarDict(javaGrammar):
        #get current state of grammar
        currentGrammar = dict() #hash the parent definitions
        dictOrder = [] #keep track of their orders though!
        parent = None
        for line in javaGrammar:
            if line != '':
                if line[0].isspace():
                    #is child definition
                    lineList = line.split() #omit count(the last element)
                    currentGrammar[parent].append(lineList)
                else:
                    #is a parent definition
                    currentGrammar[line.strip()] = []
                    parent = line.strip()
                    dictOrder.append(parent)
        return dictOrder, currentGrammar
        
    #adds grammars found in javaTree to currentDict
    @staticmethod
    def captureGrammars(javaTree, currentDict):
        node, grammar = JavaLang.getGrammarFromNode(javaTree)
        if node in currentDict:
            currentDict[node].append(grammar)
        else:
            currentDict[node] = [grammar]
        for child in javaTree.children:
            if isinstance(child, TreeNode):
                JavaLang.captureGrammars(child, currentDict)  
    
    #creates grammar-definition tuple from a TreeNode object
    @staticmethod
    def getGrammarFromNode(node):
        name = node.name+':'
        children = node.children
        grammar = list()
        for child in children:
            if isinstance(child, TreeNode):
                grammar.append(child.name)
            elif isinstance(child, Token):
                if (isinstance(child, Separator) 
                    or isinstance(child, Keyword)
                    or isinstance(child, Operator)):
                    grammar.append(child.string)
                elif isinstance(child, Identifier):
                    grammar.append('Identifier')
                elif isinstance(child, Literal):
                    grammar.append('Literal')
        return (name, grammar)
    
def testGetGrammarFromNode():
    node = TreeNode('GenericNode')
    node.children = [TreeNode('AnotherGenericNode'), Separator('('), Keyword('public'),
                     Identifier('MYID'), Literal('"LITTY"'), Operator('+')]
    assert(JavaLang.getGrammarFromNode(node) 
           == ('GenericNode', ('AnotherGenericNode', '(', 'public', 'Identifier', 'Literal', '+')))
    
#testGetGrammarFromNode()