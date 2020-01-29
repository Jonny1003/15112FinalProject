#@Jonathan Ke
#@11/25/2019
#Creates a visual representation of java and python trees for code analysis. 
#cmu_112_graphics taken from http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html#events

from cmu_112_graphics import *
from Token import Token
from TreeNode import TreeNode
import Translator
import math
from fractions import Fraction

#top level controller app
class TreeApp(ModalApp):
    
    def __init__(self, javaTree, pythonTree, width = 700, height = 700):
        self.javaSyntaxTree = javaTree
        self.pythonSyntaxTree = pythonTree
        super().__init__(width = width, height = height)
    
    def appStarted(self):
        self.javaTreeMode = JavaTreeMode()
        self.pythonTreeMode = PythonTreeMode()
        self.helpMode = HelpMode()
        self.setActiveMode(self.javaTreeMode)
        
#help mode implementation
class HelpMode(Mode):
    
    def redrawAll(self, canvas):
        text = '''
Observe the syntax breakdown of your code. 
Press to zoom-in on a treenode
Press 'Get Java Tree' or 'Get Python Tree' to switch 
between the Java and Python translations of your code.
        '''
        canvas.create_text(self.width/2, self.height/2, 
                           text = text)
        
    def mousePressed(self, event):
        self.app.setActiveMode(self.app.javaTreeMode)
    
#main mode for drawing the tree
class JavaTreeMode(Mode):
    
    def appStarted(self):
        self.syntaxTree = self.app.javaSyntaxTree
        self.unitHeight = self.findTreeHeight(self.syntaxTree)
        #create an object representing how what positions in each layer
        #of tree have been filled
        self.layerCounts = dict()
        self.findWidthAtLayers(self.syntaxTree, 0, self.layerCounts)
        self.layersDict = dict()
        self.mouseHovering = False
        self.mouseHoveringHelp = False
        self.rectVals = (4,21,160,43)
        self.isDilated = False
        self.dFactor = 2
        
    def redrawAll(self, canvas):
        #find parameters for drawing the tree(varies based on window size)
        for layer in self.layerCounts:
            self.layersDict[layer] = 1
        self.incrementHeight = self.height/(self.unitHeight+1)
        #draw the tree
        self.drawNode(canvas, self.syntaxTree, self.width/2, 8)
        #draw the labels
        self.drawName(canvas)
        #draw highlights
        rectVals2 = (4, self.height-4, 49, self.height-26)
        if self.mouseHoveringHelp:
            canvas.create_rectangle(rectVals2[0], rectVals2[1], rectVals2[2], rectVals2[3],
                                    fill = 'turquoise', width = 2, outline = 'red')
        else:
            canvas.create_rectangle(rectVals2[0], rectVals2[1], rectVals2[2], rectVals2[3],
                                    fill = 'turquoise', width = 2)
        canvas.create_text(5, self.height-5, text = 'Help', anchor = 'sw',
                           font = 'Arial 20 bold')
        #draw dilation if it's on
        if self.isDilated:
            self.drawDilation(canvas)
            
    #dilation drawing function
    def drawDilation(self, canvas):
        #draw dilation space
        r = self.dilationRadius
        canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, width = 3,
                           fill = 'white')
        dR = self.dFactor*self.radius
        #draw the lines inside the dilation space
        for circle in self.dilatedNodes:
            coord = circle[1]
            if coord[0]**2+coord[1]**2 <= r*r:
                #draw lines between points
                self.drawDilatedLines(canvas, circle)
        #draw the node shapes and labels for the nodes
        for circle in self.dilatedNodes:
            node = circle[0]
            if isinstance(node, TreeNode):
                label = node.name
                color = 'black'
            elif isinstance(node, Token):
                label = node.string
                color = 'blue'
            else:
                label = node.string
                color = 'blue'
            coord = circle[1]
            if coord[0]**2+coord[1]**2 <= r*r:
                canvas.create_oval(coord[0]+self.x-dR, coord[1]+self.y-dR,
                                    coord[0]+self.x+dR, coord[1]+self.y+dR,
                                    fill = 'yellow', width = 2)
                canvas.create_text(coord[0]+self.x,coord[1]+self.y, text = label,
                                    font = 'Arial 15 bold', fill = color)
                
    #draws a connector line structure inside the dilation space
    def drawDilatedLines(self, canvas, currentNode):
        node = currentNode[0]
        coord = currentNode[1]
        for circle in self.dilatedNodes: #check if the parent is in the dilation
            if circle[0] == node.parent: 
                newCoord = circle[1]
                if (newCoord[0]**2+newCoord[1]**2 > self.dilationRadius**2):
                    newCoord = self.betterGetIntersectionWrapper(coord,newCoord,
                                                          self.dilationRadius)
                canvas.create_line(coord[0]+self.x, coord[1]+self.y,
                                   newCoord[0]+self.x, newCoord[1]+self.y,
                                   width = 2)
                break
        if isinstance(node, TreeNode): 
            for child in node.children: #draw the lines between current node and children
                for circle in self.dilatedNodes:
                    if circle[0] == child:
                        newCoord = circle[1]
                        if (newCoord[0]**2+newCoord[1]**2 > self.dilationRadius**2):
                            newCoord = self.betterGetIntersectionWrapper(coord,newCoord,
                                                                  self.dilationRadius)
                        canvas.create_line(coord[0]+self.x, coord[1]+self.y,
                                   newCoord[0]+self.x, newCoord[1]+self.y,
                                   width = 2)
                        break
                    
    @staticmethod
    def betterGetIntersectionWrapper(pt1, pt2, r, lamba = 4):
        #pt2 must be outside the circle!
        return JavaTreeMode.betterGetIntersection(pt1,pt2, r, lamba)

    #recursive function using bijection approximation
    @staticmethod
    def betterGetIntersection(pt1, pt2, r, lamba):
        guessX = (pt1[0]+pt2[0])/2
        guessY = (pt1[1]+pt2[1])/2
        if r**2-lamba <= guessX**2+guessY**2 <= r**2+lamba:
            return (guessX, guessY)
        if r**2 < guessX**2+guessY**2:
            return JavaTreeMode.betterGetIntersection(pt1, (guessX, guessY), r,lamba)
        return JavaTreeMode.betterGetIntersection((guessX, guessY), pt2, r,lamba)
                        
    #extremely inaccurate. Deprecated. Bits are horrible at computing decimals... :(
    @staticmethod 
    def getIntersection(pt1, pt2, r):
        if pt1[0]-pt2[0] == 0: #slope undefined
            y = int(math.sqrt(r*r-pt1[0]*pt1[0]))
            if min(pt1[1],pt2[1]) <= y <= max(pt2[1],pt1[1]):
                return pt1[0], y
            else:
                return pt1[0], -y
        else:
            x0, y0 = Fraction(pt1[0]), Fraction(pt1[1])
            x1, y1 = Fraction(pt2[0]), Fraction(pt2[1])
            dY = y1-y0
            dX = x1-x0
            slope = dY/dX
            if slope*slope > 1:
                solution = JavaTreeMode.getIntersection((y1,x1),(y0,x0),r)
                return solution[1], solution[0]
            a = slope*slope+1
            b = 2*slope*y0-2*slope*slope*x0
            c = y0*y0 - 2*slope*y0*x0 - r*r
            x2 = (-b + Fraction(math.sqrt(b*b-4*a*c)))/2/a
            y2 = slope*x2-slope*x0+y0       
            if ((min(x0,x1)-10 <= x2 and x2 <= max(x0,x1)+10)
                or (min(y0,y1)-10 <= y2 and y2 <= max(y0,y1)+10)):
                return float(x2), float(y2)   
            #try the other solution   
            x3 = (-b - Fraction(math.sqrt(b*b-4*a*c)))/2/a
            y3 = slope*x3-slope*x0+y0
            if ((min(x0,x1)-10 <= x3 <= max(x0,x1)+10)
                or (min(y0,y1)-10 <= y3 <= max(y0,y1)+10)):
                return float(x3), float(y3)
            return float(x2), float(y2)
        
    #draws the labels in the window
    def drawName(self, canvas):
        canvas.create_text(5,0, anchor = 'nw', text = 'Java Parse Tree',
                         font = 'Arial 20 bold')
        rectVals = self.rectVals
        if self.mouseHovering:
            canvas.create_rectangle(rectVals[0],rectVals[1],rectVals[2],rectVals[3],
                                    fill = 'turquoise', width = 2,
                                    outline = 'red')
        else:
            canvas.create_rectangle(rectVals[0],rectVals[1],rectVals[2],rectVals[3],
                                    fill = 'turquoise', width = 2)
        canvas.create_text(5,20, anchor = 'nw', text = 'Get Python Tree',
                           font = 'Arial 20 bold')
        
    #toggles button highlights
    def mouseMoved(self, event):
        if (self.rectVals[0] < event.x < self.rectVals[2] 
            and self.rectVals[1] < event.y < self.rectVals[3]):
            self.mouseHovering = True
        else:
            self.mouseHovering = False
        rectVals2 = (4, self.height-4, 48, self.height-26)
        if (rectVals2[0] < event.x < rectVals2[2] 
            and rectVals2[1] > event.y > rectVals2[3]):
            self.mouseHoveringHelp = True
        else:
            self.mouseHoveringHelp = False
            
    #toggle off dilations
    def mouseReleased(self, event):
        self.isDilated = False
    
    def mousePressed(self, event):
        #trigger modal app 
        if (self.rectVals[0] < event.x < self.rectVals[2] 
            and self.rectVals[1] < event.y < self.rectVals[3]):
            self.app.setActiveMode(self.app.pythonTreeMode)
        rectVals2 = (4, self.height-4, 48, self.height-26)
        if (rectVals2[0] < event.x < rectVals2[2] 
            and rectVals2[1] > event.y > rectVals2[3]):
            self.app.setActiveMode(self.app.helpMode)
        #toggle dilation 
        self.isDilated = True
        self.dilatedNodes = self.createDilation(event.x, event.y)
        self.x, self.y = event.x, event.y

    #calculates the number of vertical layers
    @staticmethod
    def findTreeHeight(tree, currentHeight = 0, maxHeight = 0):
        if not isinstance(tree, TreeNode):
            if currentHeight > maxHeight:
                return currentHeight
            else:
                return maxHeight
        children = tree.children
        for child in children:
            height = JavaTreeMode.findTreeHeight(child, currentHeight = currentHeight+1,
                                    maxHeight = maxHeight)
            if height > maxHeight: maxHeight = height
        return maxHeight
    
    #calculates the number of nodes at each vertical layer
    @staticmethod
    def findWidthAtLayers(tree, currentLayer, layers):
        if currentLayer in layers:
            layers[currentLayer] += 1
        else:
            layers[currentLayer] = 1
        if isinstance(tree, TreeNode):
            for child in tree.children:
                JavaTreeMode.findWidthAtLayers(child, currentLayer+1, layers)
                
    #finds the nodes that can be potentially dilated
    @staticmethod
    def findNodesAroundMouse(x, y, radius, tree, nodesList = None):
        if nodesList == None:
            nodesList = []
        if x-radius < tree.x < x+radius and y-radius < tree.y < y+radius:
            nodesList.append(tree)
        if isinstance(tree, TreeNode):
            for child in tree.children:
                JavaTreeMode.findNodesAroundMouse(x,y,radius, child, 
                                                     nodesList = nodesList)
        return nodesList
    
    #recalculated dilation space
    def mouseDragged(self, event):
        self.dilatedNodes = self.createDilation(event.x, event.y)
        self.x, self.y = event.x, event.y
                
    #draw the tree recursively
    def drawNode(self, canvas, treeNode, x, y, layer = 1):
        if not isinstance(treeNode, str):
            treeNode.x = x
            treeNode.y = y
        #calculate the space the child is allow to draw itself
        if isinstance(treeNode, TreeNode):
            numberOfChildren = len(treeNode.children)
            unitWidth = self.width / (self.layerCounts[layer]+1)
            #draw the children node lines
            y2 = y+self.incrementHeight 
            x2 = self.layersDict[layer]*unitWidth
            for child in treeNode.children:
                #draw child
                canvas.create_line(x,y,x2,y2, width = 1)
                self.layersDict[layer] += 1
                self.drawNode(canvas, child, x2, y2, layer = layer+1)
                x2 += unitWidth
        #draw the node itself
        self.radius = 5
        r = self.radius
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = 'yellow',
                           width = 1)
        #name the node
        if isinstance(treeNode, TreeNode):
            canvas.create_text(x,y, text = treeNode.name, font = 'Arial 10')
        elif isinstance(treeNode, Token): #token
            canvas.create_text(x,y, text = treeNode.string, font = 'Arial 10 bold',
                               fill = 'blue')
        else:
            canvas.create_text(x,y, text = treeNode, font = 'Arial 10 bold',
                               fill = 'blue')
            
    #returns  nodes to be potentially drawn in dilated space
    def createDilation(self, x, y):
        self.dilationRadius = 200
        nodes = self.findNodesAroundMouse(x, y, self.dilationRadius*4, self.syntaxTree)
        dilatedNodes = []
        dFactor = self.dFactor
        for node in nodes:
            if isinstance(node, TreeNode):
                dilatedNodes.append((node,(dFactor*(node.x-x), dFactor*(node.y-y))))
            elif isinstance(node, Token):
                dilatedNodes.append((node,(dFactor*(node.x-x), dFactor*(node.y-y))))
            else:
                dilatedNodes.append((node,(dFactor*(node.x-x), dFactor*(node.y-y))))
        return dilatedNodes
            

#draws Python tree structure        
class PythonTreeMode(JavaTreeMode):
    
    def appStarted(self):
        self.syntaxTree = self.app.pythonSyntaxTree
        self.unitHeight = self.findTreeHeight(self.syntaxTree)
        self.incrementHeight = self.height/self.unitHeight-1
        #create an object representing how what positions in each layer
        #of tree have been filled
        self.layerCounts = dict()
        self.findWidthAtLayers(self.syntaxTree, 0, self.layerCounts)
        self.layersDict = dict()
        self.mouseHovering = True
        self.mouseHoveringHelp = False
        self.rectVals = (4,21,138,43)
        self.isDilated = False
        
    #override label drawings in JavaTreeMode
    def drawName(self, canvas):
        canvas.create_text(5,0, anchor = 'nw', text = 'Python Parse Tree',
                         font = 'Arial 20 bold')
        rectVals = self.rectVals
        if self.mouseHovering:
            canvas.create_rectangle(rectVals[0],rectVals[1],rectVals[2],rectVals[3],
                                    fill = 'turquoise', width = 2,
                                    outline = 'red')
        else:
            canvas.create_rectangle(rectVals[0],rectVals[1],rectVals[2],rectVals[3],
                                    fill = 'turquoise', width = 2)
        canvas.create_text(5,20, anchor = 'nw', text = 'Get Java Tree',
                           font = 'Arial 20 bold')
        
    #THIS MODE WILL NOT SUPPORT DILATION FUNCTION!!!!!!
    def mousePressed(self, event):
        if (self.rectVals[0] < event.x < self.rectVals[2] 
            and self.rectVals[1] < event.y < self.rectVals[3]):
            self.app.setActiveMode(self.app.javaTreeMode)
        #help button collision checker
        rectVals2 = (4, self.height-4, 48, self.height-26)
        if (rectVals2[0] < event.x < rectVals2[2] 
            and rectVals2[1] > event.y > rectVals2[3]):
            self.app.setActiveMode(self.app.helpMode)
       
    #THIS MODE WILL NOT SUPPORT DILATION FUNCTION!!!!!!     
    def mouseDragged(self,event):
        pass
    
def testApp():
    code = """
    public class HelloWorld{
       public static void main(String[] args){
           int i = 0;
       }
       
       public static void main1(String[] args){
           int i = 0;
       }
       
       public static void main2(String[] args){
           int i = 0;
       }
    }
    """
    code, javaTree, pythonTree, tokens, depth = Translator.compile(code)
    myTreeApp = TreeApp(javaTree, pythonTree, width = 800, height = 700 )

#testApp()

    
    
    