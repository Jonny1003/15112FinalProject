#@Jonathan Ke
#@12/2/2019
#Game implementation for matching code in IDE to displayed tree

from JavaTreeBuilder import *
import Translator
import random
import tkinter.font

#top level app
class TreeBuilderGame(ModalApp):
    
    def __init__(self, parent, width = 500, height = 500):
        parent.treeBuilderGameWindow = self
        super().__init__(width = width, height = height)
    
    def appStarted(self):
        self.level1 = Level1()
        self.level2 = Level2()
        self.level3 = Level3()
        self.levels = (self.level1, self.level2, self.level3)
        self.levelNumber = 0
        self.currentLevel = self.level1
        self.helpMode = GameHelpMode()
        self.winMode = WinMode()
        self.setActiveMode(self.currentLevel)
        
    def setNextLevel(self):
        self.levelNumber += 1
        if self.levelNumber == len(self.levels):
            print('All levels passed!')
            self.setActiveMode(self.winMode)
        else:
            self.currentLevel = self.levels[self.levelNumber]
            self.setActiveMode(self.currentLevel)
        
#help mode 
class GameHelpMode(Mode):
    
    def redrawAll(self, canvas):
        text = '''
Observe the syntax breakdown of your code. 
Press to zoom-in on a treenode
Press 'Get Java Tree' or 'Get Python Tree' to switch 
between the Java and Python translations of your code.
Red labels represent an actual Java token while black 
labels represent a Java grammar structure.

Write the correct code in the Java text editor until it 
matches the Java code structure presented in this window.
Click "Match Code to Level" when you think you have written
the code to match the level.
        '''
        canvas.create_text(self.width/2, self.height/2, 
                           text = text)
        
    def mousePressed(self, event):
        self.app.setActiveMode(self.app.currentLevel)
        
class WinMode(Mode):
    
    def appStarted(self):
        self.timerDelay = 500
        self.colors = []
        for i in range(0, 256, 20):
            for j in range(0, 256, 20):
                for k in range(0, 256, 20):
                    self.colors.append("#%02x%02x%02x" % (i, j, k))
        print(len(self.colors))
        self.colorIndex = 0
        self.spacingIndex = 0
        self.val = 1
        self.win = 'You Win!!!!!!!!!!!!'
        self.writeCharIndex = 0
    
    def timerFired(self):
        self.colorIndex = random.randint(0,len(self.colors)-1)
        self.spacingIndex += self.val
        if self.spacingIndex == 2:
            self.val = -1
        elif self.spacingIndex == 0:
            self.val = 1
        self.writeCharIndex = (self.writeCharIndex+1)%len(self.win)
    
    def redrawAll(self, canvas):
        text = '''
**************************************************
*  []   []  []   [][][]    []     []   []     []   [][][]   [][][][] *
*  []   []  []      []      [][]  []   [][]  []    []         []    []  *
*  []   []  []      []      [] [] []   [] [] []    [][][]   [][][]    *
*  []   []  []      []      []  [][]   []  [][]    []         []   []    *
*  [][][][][]   [][][]   []    []    []    []    [][][]    []     []  *
**************************************************
        '''
        
        canvas.create_text(self.width/2, self.height/2, 
                           font = ('Monospaced', int(18/(self.spacingIndex+1))),
                           text = self.textAdjust(text), 
                           fill = self.colors[self.colorIndex],
                           justify = CENTER)
        
        size = len(self.colors)-1
        for i in range(200):
            x, y = self.width/2, self.height/2 
            while (self.width/5 < x < self.width*4/5 and 
                   self.height/3 < y < self.height*2/3):
                x = random.randint(0,self.width)
                y = random.randint(0,self.height)
            canvas.create_text(x,y, font = 'Calibri 12', 
                               text = self.win[:self.writeCharIndex],
                               fill = self.colors[random.randint(0,size)])
        
                           
        
    def textAdjust(self, text):
        out = ''
        f = self.spacingIndex
        for c in text:
            if c == '*':
                out += '*'+' '*(f)
            elif c == '[':
                out += '['+'*'*f
            elif c == '\n':
                out += '\n'+'\n'*f
            else:
                out += c
        return out
        
    
#extends from JavaTreeMode, implements game display for general level
class GoalTreeLevel(JavaTreeMode):
    
    def __init__(self, level, difficulty, levelNumber):
        self.level = level
        self.levelNumber = levelNumber
        self.difficulty = difficulty
        pyCode, javaTree, pyTree, tokens, depth = Translator.compile(self.level)
        self.pythonTree = pyTree
        self.syntaxTree = javaTree
        self.pyLevel = PythonTreeGameMode(self)
        super().__init__()
    
    def appStarted(self):
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
        
        #game variables
        self.getLabeledNodes(self.syntaxTree)
        
    def getLabeledNodes(self, tree):
        if random.randint(0, self.difficulty) == 0:
            tree.willBeLabeled = True
        else:
            tree.willBeLabeled = False
        if isinstance(tree, TreeNode):
            for child in tree.children:
                self.getLabeledNodes(child)
                
    def redrawAll(self, canvas):
        super().redrawAll(canvas)
        canvas.create_text(self.width-5, self.height-5, text = 'Create Code\nto Match\nThis Tree!',
                           font = 'Arial 20 bold', anchor = 'se', justify = CENTER)
        canvas.create_text(self.width-2, 2, text = f'LVL {self.levelNumber}',
                           font = 'Helvetica 30 bold italic', anchor = 'ne', justify = CENTER)
        
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
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = 'blue',
                           width = 1)
        if treeNode.willBeLabeled:
            #name the node
            if isinstance(treeNode, TreeNode):
                canvas.create_text(x,y, text = treeNode.name, font = 'Arial 10')
            elif isinstance(treeNode, Token): #token
                canvas.create_text(x,y, text = treeNode.string, font = 'Arial 10',
                                fill = 'red')
            else:
                canvas.create_text(x,y, text = treeNode, font = 'Arial 10',
                                fill = 'red')
                
    def drawDilation(self, canvas):
        r = self.dilationRadius
        canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, width = 3,
                           fill = 'white')
        dR = self.dFactor*self.radius
        for circle in self.dilatedNodes:
            coord = circle[1]
            if coord[0]**2+coord[1]**2 <= r*r:
                #draw lines between points
                self.drawDilatedLines(canvas, circle)
        for circle in self.dilatedNodes:
            node = circle[0]
            if isinstance(node, TreeNode):
                label = node.name
                color = 'black'
            elif isinstance(node, Token):
                label = node.string
                color = 'red'
            else:
                label = node.string
                color = 'red'
            coord = circle[1]
            if coord[0]**2+coord[1]**2 <= r*r:
                canvas.create_oval(coord[0]+self.x-dR, coord[1]+self.y-dR,
                                    coord[0]+self.x+dR, coord[1]+self.y+dR,
                                    fill = 'blue', width = 2)
                if node.willBeLabeled:
                    canvas.create_text(coord[0]+self.x,coord[1]+self.y, text = label,
                                        font = 'Arial 15 bold', fill = color)
                    
    def mousePressed(self, event):
        if (self.rectVals[0] < event.x < self.rectVals[2] 
            and self.rectVals[1] < event.y < self.rectVals[3]):
            self.app.setActiveMode(self.pyLevel)
        rectVals2 = (4, self.height-4, 48, self.height-26)
        if (rectVals2[0] < event.x < rectVals2[2] 
            and rectVals2[1] > event.y > rectVals2[3]):
            self.app.setActiveMode(self.app.helpMode)
        self.isDilated = True
        self.dilatedNodes = self.createDilation(event.x, event.y)
        self.x, self.y = event.x, event.y
        
#implements game mode Python tree window
class PythonTreeGameMode(PythonTreeMode):
    
    def __init__(self, javaParent):
        self.syntaxTree = javaParent.pythonTree
        self.javaLevel = javaParent
        super().__init__()
        
    def appStarted(self):
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
        canvas.create_oval(x-r, y-r, x+r, y+r, fill = 'blue',
                           width = 1)
        
    def mousePressed(self, event):
        if (self.rectVals[0] < event.x < self.rectVals[2] 
            and self.rectVals[1] < event.y < self.rectVals[3]):
            self.app.setActiveMode(self.javaLevel)
        rectVals2 = (4, self.height-4, 48, self.height-26)
        if (rectVals2[0] < event.x < rectVals2[2] 
            and rectVals2[1] > event.y > rectVals2[3]):
            self.app.setActiveMode(self.app.helpMode)
                
#level 1 of game       
class Level1(GoalTreeLevel):
    
    def __init__(self):
        level = '''
public class HelloWorld{
    public static void HelloWorld(String[] args){
        System.out.println("Hello World!");
    }
}
        '''
        super().__init__(level, 0, 1)
   
#level 2 of game     
class Level2(GoalTreeLevel):
    
    def __init__(self):
        level = '''
public class Means{
    public static void main(String[] args){
        System.out.println(Means(1234,4321));
    }
    
    public static int Means(int num, int num2){
        return (num+num2)/2;
    }
}
        '''
        super().__init__(level, 0, 2)
        
#level 3
class Level3(GoalTreeLevel):
    
    def __init__(self):
        level = '''
public class ICanMakeArraysAndForLoops{
    public static void main(String[] args){
        int[] arr = new int[5];
        for (int i = 0; i < 5; i++){
            arr[i] = i;
        }
    }
}
        '''
        super().__init__(level, 0, 3)
        
def testTreeBuilderGame():
    TreeBuilderGame(None, width = 500, height = 500)
    
#testTreeBuilderGame()