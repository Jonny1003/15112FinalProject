#Jonathan Ke
#11/19/2019
#Output parse node and tree structures, translating helper structures

#java parse tree object class
class TreeNode:
    
    def __init__(self, name):
        self.name = name
        self.children = []
        
    def addChild(self, child):
        self.children.append(child)
        
    def giveSelfToChildren(self):
        for child in self.children:
            child.parent = self
        
    #returns pathway of first appearance of token or None
    #the last value of pathway is the token
    def findToken(self, token, pathway):
        for i in range(len(self.children)):
            child = self.children[i]
            returned = self.checkEqualTokens(child, token, pathway)
            if returned != None:
                return returned
        return None #token not found, return to parent
    
    def checkEqualTokens(self, child, token, pathway):
        if (isinstance(token, NodeCapturer) 
            and isinstance(child,TreeNode)
            and token.name == child.name):
                    token.capture(child)
                    pathway.append(self)
                    pathway.append(child)
                    return pathway
        elif isinstance(child,TreeNode): #nonterminal path
            path = child.findToken(token, pathway+[self])
            if path != None:
                return path
        elif isinstance(token,Capturer) and isinstance(child,token.tokenType):
            token.capture(child.string)
            pathway.append(self)
            pathway.append(child)
            return pathway
        elif isinstance(child, Token) and child.string == token: 
            #check if the child's value exactly matches token input
            pathway.append(self)
            pathway.append(child)
            return pathway
        return None
        
    def compareToStatement(self, tokenList):
        for token in tokenList:
            if self.findToken(token, []) == None:
                return False
        return True
    
    def getStatementPaths(self, tokenList):
        firstPath = self.findToken(tokenList[0],[])
        if firstPath == None: #statement not found
            return None
        pathways = [firstPath]
        for token in tokenList[1:]:
            print('token =',token)
            potentialPath = self.findNearestTokenPath(token,pathways[-1])
            if potentialPath == None:
                return None
            pathways.append(potentialPath)
        return pathways
    
    #checks if the subsequent token to the current token path 
    #is parameter token
    def findNextToken(self, token, currentPath):
        child = currentPath[-1]
        parent = currentPath[-2]
        if len(parent.children.index(child)) == 1:
            pass
        indexOfChild = parent.children.index(child)
                
    def __repr__(self):
        return self.name
    
#special object used to extract certain token types from tree
class Capturer(object):
    
    def __init__(self, tokenType):
        self.tokenType = tokenType
        
        
    def capture(self, value):
        print(value)
        if value == 'true':
            value = 'True'
        elif value == 'false':
            value = 'False'
        elif value == 'null':
            value = 'None'
        elif value == '&&':
            value = 'and'
        elif value == '||':
            value = 'or'
        self.value = value
        
#used to extract entire subtrees from current tree
class NodeCapturer(object):
    def __init__(self,name, changeName = None):
        self.name = name
        self.tokenType = TreeNode
        self.changeName = changeName
    
    def capture(self, node):
        self.node = node
        if self.changeName != None:
            self.node.name = self.changeName
        
    def __repr__(self):
        return f'Node Capturer<{self.name}>'
        
#used to extract a subtree and specify where it will move up the current tree
class NodeMover(NodeCapturer):
    
    def __init__(self, name, desiredParent, childAhead = None,
                 childBehind = None, changeName = None):
        super().__init__(name, changeName = changeName)
        self.parentDestination = desiredParent
        self.childAhead = childAhead
        self.childBehind = childBehind
    
    def moveToNewParent(self):
        parent = self.node.parent
        while parent.name != self.parentDestination:
            parent = parent.parent
        children = parent.children
        if self.childAhead == None and self.childBehind == None:
            children.append(self.node)
        else:
            for i in range(len(children)):
                if not isinstance(children[i],str):
                    if children[i].name == self.childAhead:
                        children.insert(i+1,self.node)
                        return
                    elif children[i].name == self.childBehind:
                        children.insert(i-1,self.node)
                        return