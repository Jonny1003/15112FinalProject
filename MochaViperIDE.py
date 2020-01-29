#@Jonathan Ke
#@12/2/2019
#Main user interface for Translator

import tkinter as tk 
from PIL import Image, ImageTk
import Translator
import os
import parser 
from JavaLang import JavaLang
from PythonLang import PythonLang
import Parser2
import JavaTreeBuilder
import TreeBuilderGame
from TreeNode import TreeNode

#parent frame
class MochaViperIDE(tk.Frame):
    
    def __init__(self, master = None):
        super().__init__(master)
        #statics
        self.inFileName = 'PasteAndRunInTerminalDONOTTOUCHPLS.py'
        self.outFileName = 'OutputFromTerminalDONOTTOUCH.txt'
        self.master = master
        #draw widgets
        self.createJavaWidgets()
        self.createPythonWidgets()
        self.makeButtons()
        self.createTerminalWidget()
        self.pack()
        #tree visualization variables
        self.javaTree = None
        self.pythonTree = None
        self.drawTreeApp = None
        self.treeBuilderGameWindow = None
        
    def createJavaWidgets(self):
        #name/labels
        image = Image.open('java.png')
        imageResized = image.resize((20,16))
        self.javaImage = ImageTk.PhotoImage(imageResized)
        label = tk.Label(self, justify = tk.LEFT, compound = tk.LEFT,
                         text = ' Java Text Editor', font = ('Courier', 12), 
                         image = self.javaImage, padx = 0, bg = 'turquoise')
        label.grid(row = 0, column = 1, sticky = tk.NSEW)
        #line number coordinator
        self.javaLineNumbers = tk.Text(self, height = 35, width = 4)
        self.javaLineNumbers.tag_configure('regular', font = ('Courier', 12))
        for i in range(1,101):
            self.javaLineNumbers.insert(tk.END,str(i)+(3-len(str(i)))*' '+'|\n', 'regular')
        self.javaLineNumbers.grid(row = 1, column = 0, rowspan = 35, sticky = tk.NSEW)
        self.javaLineNumbers.config(state = tk.DISABLED)
        
        #java text editor
        self.javaText = tk.Text(self, height = 35, width = 60, tabs = '1c', font = ('Courier', 12))
        self.javaText.grid(row = 1, column = 1, rowspan = 35,  sticky = tk.NSEW)
        text = '''
public class HelloWorld{
    public static void main(String[] args){
        System.out.println("Hello World!");
        int[] i = new int[1];
    }
}
        '''
        
        self.javaText.tag_configure('error', font = ('Courier', 12, 'italic'),
                                    foreground = 'red')
        self.javaText.tag_configure('keyword', foreground = 'purple',
                                    font = ('Courier', 12))
        self.javaText.tag_configure('primitives', foreground = 'blue',
                                    font = ('Courier', 12))
        self.javaText.tag_configure('regular', font = ('Courier', 12))
        self.textBoxRowJava = 2
        
        self.javaText.insert(tk.END, text, 'regular')
        
        #java scrollbar
        self.javaScroll = tk.Scrollbar(self, bd = 1, bg = 'grey')
        self.javaScroll.grid(row = 1, column = 2, rowspan = 35, sticky = tk.NSEW)
        
        #configure scrollbar with textbox
        self.javaScroll.config(command = self.javaText.yview)
        self.javaText.config(yscrollcommand=self.javaScroll.set)
        
        #highlight function
        self.javaLineNumbers.tag_configure('highlighter', foreground = 'blue',
                                           font = ('Arial', 12))
        self.currentLineNum = 1
        self.javaLineNumbers.after(5, self.highlightLine)
        #scroll function
        self.javaLineNumbers.after(10, self.onScrollJava)
        
    #self-calling function for scrollbar implementation and updating java window
    def onScrollJava(self):
        #check for lowest line overflow
        lowestLineJava = float(self.javaText.index(tk.END))
        if lowestLineJava > 100:
            self.javaText.delete('101.0',tk.END)
            lowestLineJava = 100
        #check to update scrollbar
        newRow = int(self.javaText.yview()[0]*lowestLineJava)
        if newRow != self.textBoxRowJava:
            self.javaLineNumbers.yview_scroll(newRow-self.textBoxRowJava, 'units')
            self.textBoxRowJava = newRow
        #don't let user scroll the line numbers
        scrollBarRow = int(self.javaLineNumbers.yview()[0]*100)+1
        if scrollBarRow != self.textBoxRowJava: 
            self.javaLineNumbers.yview_scroll(-scrollBarRow+self.textBoxRowJava, 'units')
        self.javaLineNumbers.after(5, self.onScrollJava)
        
    def createPythonWidgets(self):
        #labels
        image = Image.open('python.jpg')
        imageResized = image.resize((20,16))
        self.pythonImage = ImageTk.PhotoImage(imageResized)
        label = tk.Label(self, justify = tk.LEFT, compound = tk.LEFT,
                         text = ' Python Compiled Text', font = ('Courier', 12), 
                         image = self.pythonImage, padx = 0, bg = 'turquoise')
        label.grid(row = 0, column = 5, sticky = tk.NSEW)
        #line number coordinator
        self.pythonLineNumbers = tk.Text(self, height = 35, width = 4, font = ('Courier', 12))
        self.pythonLineNumbers.tag_configure('regular', font = ('Courier', 12))
        for i in range(1,101):
            self.pythonLineNumbers.insert(tk.END,str(i)+(3-len(str(i)))*' '+'|\n', 'regular')
        self.pythonLineNumbers.grid(row = 1, column = 4, rowspan = 35, sticky = tk.NSEW)
        self.pythonLineNumbers.config(state = tk.DISABLED)
        self.pythonLineNumbers.after(10, self.onScrollPython)
        
        #python text editor
        self.pythonText = tk.Text(self, height = 35, width = 60, tabs = '1c', font = ('Courier', 12))
        self.pythonText.grid(row = 1, column = 5, rowspan = 35, sticky = tk.NSEW)
        
        self.pythonText.tag_configure('error', font = ('Courier', 12, 'italic'),
                                    foreground = 'red')
        self.pythonText.tag_configure('keyword', foreground = 'purple',
                                    font = ('Courier', 12))
        self.pythonText.tag_configure('primitives', foreground = 'blue',
                                    font = ('Courier', 12))
        self.pythonText.tag_configure('regular', font = ('Courier', 12))
        
        text = '''Fancy Python Text'''
        self.pythonText.insert(tk.END, text, 'regular')
        self.textBoxRowPy = 1
        
        #scrollbar
        pythonScroll = tk.Scrollbar(self, bd = 1, bg = 'grey')
        pythonScroll.grid(row = 1, column = 6, rowspan = 35, sticky = tk.NSEW)
        #configure scrollbar with textbox
        pythonScroll.config(command = self.pythonText.yview)
        self.pythonText.config(yscrollcommand=pythonScroll.set)
        
        #highlight function
        self.pythonLineNumbers.tag_configure('highlighter', foreground = 'blue',
                                           font = ('Arial', 12))
        self.pythonCurrentLine = 1
      
     #self-calling function for scrollbar implementation and updating for python window  
    def onScrollPython(self):
        #check for out of bounds and reset to in bounds(99 line limit rn):
        lowestLinePy = float(self.pythonText.index(tk.END))
        if lowestLinePy > 100:
            self.pythonText.delete('101.0',tk.END)
            lowestLinePy = 100
        newRow = int(self.pythonText.yview()[0]*lowestLinePy)
        if newRow != self.textBoxRowPy:
            self.pythonLineNumbers.yview_scroll(newRow-self.textBoxRowPy, 'units')
            self.textBoxRowPy = newRow
        scrollBarRow = int(self.pythonLineNumbers.yview()[0]*100)+1
        if scrollBarRow != self.textBoxRowPy: #don't let user scroll the line numbers
            self.pythonLineNumbers.yview_scroll(-scrollBarRow+self.textBoxRowPy, 'units')
        self.pythonLineNumbers.after(5, self.onScrollPython)
        
    def makeButtons(self):
        #compile to python button
        self.compileButton = tk.Button(self, text = 'Compile', border = 3, 
                                 anchor = tk.CENTER, padx = 4, pady = 3,
                                 height = 1, width = 8, state = tk.NORMAL,
                                 activeforeground = 'red')
        self.compileButton.grid(row = 1, column = 3, sticky = tk.NSEW)
        self.compileButton.config(command = self.compile)
        #run button
        self.runPyButton = tk.Button(self, text = 'Run Python', border = 3, 
                                     anchor = tk.CENTER, state = tk.NORMAL,
                                     activeforeground = 'red')
        self.runPyButton.grid(row = 2, column = 3, sticky = tk.NSEW)
        self.runPyButton.config(command = self.runPython)
        #clear terminal button
        self.clearTerminalButton = tk.Button(self, text = 'New Terminal', border = 3,
                                       anchor = tk.CENTER, state = tk.NORMAL,  
                                       activeforeground = 'red')
        self.clearTerminalButton.grid(row = 3, column = 3, sticky = tk.NSEW)
        self.clearTerminalButton.config(command = self.emptyTerminal)
        #smart compile button
        self.smartCompileButton = tk.Button(self, text = 'SmartCompile', border = 3,
                                            anchor = tk.CENTER, state = tk.NORMAL,
                                            activeforeground = 'red')
        self.smartCompileButton.grid(row = 4, column = 3, sticky = tk.NSEW)
        self.smartCompileButton.config(command = self.smartCompile)
        #tree builder button
        self.treeBuilderButton = tk.Button(self, text = 'Visualize\nCode Tree', border = 3,
                                           anchor = tk.CENTER, state = tk.NORMAL,
                                           activeforeground = 'red')
        self.treeBuilderButton.grid(row = 5, column = 3, sticky = tk.NSEW)
        self.treeBuilderButton.config(command = self.drawTrees)
        #tree matching game buttons
        self.treeGameButton = tk.Button(self, text = 'Play Tree\n Game', border = 3,
                                        anchor = tk.CENTER, state = tk.NORMAL,
                                        activeforeground = 'red')
        self.treeGameButton.grid(row = 6, column = 3, sticky = tk.NSEW)
        self.treeGameButton.config(command = self.playGame)
        self.checkTreeButton = tk.Button(self, text = 'Match Code\nto Level', border = 3,
                                         anchor = tk.CENTER, state = tk.DISABLED,
                                         activeforeground = 'red')
        self.checkTreeButton.grid(row = 7, column = 3, sticky = tk.NSEW)
        self.checkTreeButton.config(command = self.matchCodeToLevel)
        #load button
        self.fileOpenLabel = tk.Label(self, text = 'Enter File Name:', anchor = tk.CENTER)
        self.fileOpenLabel.grid(row = 8, column = 3, sticky = tk.NSEW)
        self.openFileEntry = tk.Entry(self, font = ('Calibri', '12'), fg = 'grey', justify = tk.CENTER)
        self.openFileEntry.insert(0, 'Enter File Name Here')
        self.openFileEntry.config(fg = 'grey')
        self.openFileEntry.grid(row = 9, column = 3, sticky = tk.NSEW)
        self.loadButton = tk.Button(self, text = 'Open', anchor = tk.CENTER, activeforeground = 'red')
        self.loadButton.grid(row = 10, column = 3, sticky = tk.NSEW)
        self.loadButton.config(command = self.openFile)     
        #save button
        self.fileSaveLabel = tk.Label(self, anchor = tk.CENTER, text = 'Save File As:')
        self.fileSaveLabel.grid(row = 11, column = 3, sticky = tk.NSEW)
        self.saveFileEntry = tk.Entry(self, font = ('Calibri', '12'), fg = 'grey', justify = tk.CENTER)
        self.saveFileEntry.insert(0, 'Enter Name')
        self.saveFileEntry.config(fg = 'grey', relief = tk.SUNKEN)
        self.saveFileEntry.grid(row = 12, column = 3, sticky = tk.NSEW)
        self.saveButton = tk.Button(self, text = 'Save', anchor = tk.CENTER, activeforeground = 'red')
        self.saveButton.grid(row = 13, column = 3, sticky = tk.NSEW)
        self.saveButton.config(command = self.saveFile)    
        
    def saveFile(self):
        fileName = self.saveFileEntry.get()
        if (not fileName.endswith('.java') and not fileName.endswith('.py') 
            or ' ' in fileName):
            self.terminal.insert(tk.END, 'Invalid file format!\n')
        else:
            newFile = open('Projects'+os.sep+fileName, 'w+')
            if fileName.endswith('.py'):
                contents = self.pythonText.get('1.0',tk.END)
            else:
                contents = self.javaText.get('1.0',tk.END)
            newFile.write(contents)
            newFile.close()
            self.terminal.insert(tk.END, 'Saved!\n')
        
    def openFile(self):
        fileName = self.openFileEntry.get()
        #check if legal file
        if fileName.endswith('.java') or fileName.endswith('.py'):
            path = self.findFilePath(fileName)
            if path == False:
                self.terminal.insert(tk.END, 'No file found! Make sure file is in Projects folder.\n')
                return
            self.terminal.insert(tk.END, 'Opened!\n')
            newFile = open(path, 'r')
            text = newFile.readlines()
            newFile.close()
            if len(text) > 100:
                text = text[:100]
            if fileName.endswith('java'):
                self.javaText.delete('1.0', tk.END)
                self.javaText.insert(tk.END,''.join(text))
            else:
                self.pythonText.delete('1.0', tk.END)
                self.pythonText.insert(tk.END,''.join(text))
        else:
            self.terminal.insert(tk.END, 'Invalid file format!\n')
            
    @staticmethod
    def findFilePath(fileName, currentPath = None):
        if currentPath == None:
            currentPath = 'Projects'
        if os.path.isfile(currentPath):
            if currentPath.endswith(fileName):
                return currentPath
            else: 
                return False
        else:
            try:
                for content in os.listdir(currentPath):
                    filePath = currentPath+os.sep+content
                    output = MochaViperIDE.findFilePath(fileName, currentPath = filePath)
                    if output != False:
                        return output
            except Exception:
                return False
        return False
    
                
                                       
        
    #starts game app
    def playGame(self):
        self.treeGameButton.config(state = tk.DISABLED)
        self.checkTreeButton.config(state = tk.NORMAL)
        print('playgame??')
        #pass self to child so child can assign itself to parent 
        #Python runs assignment last, else this would be cleaner
        TreeBuilderGame.TreeBuilderGame(self, width = 700, height = 700)
        
    #checks if code in JavaWindow matches structure of the current level's parse tree
    def matchCodeToLevel(self):
        self.compile()
        if self.parseError:
            self.terminal.insert(tk.END,
                "Your code did not compile. I cannot verify if it's right!\n")
        else:
            playerTree = self.javaTree
            levelTree = self.treeBuilderGameWindow.currentLevel.syntaxTree
            if self.checkMatchingTreeStructures(playerTree, levelTree):
                self.terminal.insert(tk.END, 'You passed the level!\n')
                self.treeBuilderGameWindow.setNextLevel()
            else:
                self.terminal.insert(tk.END, 'OOF! Try again!\n')
            
    #tests if two trees are structurally identical 
    @staticmethod
    def checkMatchingTreeStructures(tree1, tree2):
        if type(tree1) != type(tree2):
            return False
        elif isinstance(tree1, TreeNode):
            if len(tree1.children) != len(tree2.children):
                return False #nodes have different number of children
            for i in range(len(tree1.children)):
                c1 = tree1.children[i]
                c2 = tree2.children[i]
                if not MochaViperIDE.checkMatchingTreeStructures(c1, c2):
                    return False #error occured in matching children
            return True
        return True #terminal nodes 
    
    #runs tree visualization app
    def drawTrees(self):
        if self.javaTree != None and self.pythonTree != None:
            self.drawTreeApp = JavaTreeBuilder.TreeApp(self.javaTree, self.pythonTree)
        else:
            text = "You have not compiled any code yet!\n"
            self.terminal.insert(tk.END, text)
        
    #resets terminal file and backend files for terminal implementation
    def emptyTerminal(self):
        txt = 'New Terminal. MochaPython V1.0\n'
        #edit outFile
        outFile = open(self.outFileName, 'w+')
        outFile.write(txt)
        outFile.close()
        #edit terminal
        self.terminal.delete('1.0', tk.END)
        self.terminal.insert(tk.END, txt)
          
    #runs Python code in os terminal, prints to IDE "terminal"
    def runPython(self):
        inFile = open(self.inFileName, 'w+')
        pythonText = self.pythonText.get('1.0', tk.END)
        inFile.write(pythonText)
        inFile.close()
        cmd = f'python3 {self.inFileName} >> {self.outFileName}'
        os.system(cmd)
        outFile = open(self.outFileName, 'r')
        contents = outFile.read()
        outFile.close()
        if self.prevContents == contents:    
            self.terminal.insert(tk.END, 
                                 'Program finished running. No outputs to terminal'+
                                 ' (You may be seeing this because of a syntax error'+
                                 ' in the Python script being run).\n')
        else:
            self.terminal.delete('1.0',tk.END)
            self.terminal.insert(tk.END, contents)
        self.prevContents = contents
        self.terminal.see(tk.END)
        self.highlightPython()
        
    def createTerminalWidget(self):
        self.terminal = tk.Text(self, height = 5, width = 60, font = 'Courier 12')
        self.terminal.insert(tk.END, 'MochaPythonIDE V1.0\n')
        self.terminal.grid(row = 37, column = 1, columnspan = 5, sticky = tk.NSEW)
        terminalScrollbar = tk.Scrollbar(self, bd = 1, bg = 'grey')
        terminalScrollbar.grid(row = 37, column = 6, sticky = tk.NSEW)
        
        #configure scrollbar with textbox
        terminalScrollbar.config(command = self.terminal.yview)
        self.terminal.config(yscrollcommand = terminalScrollbar.set)
        
        #label
        text = 'T\nE\nR\nM\nI\nN\nA\nL\n \nO\nU\nT\nP\nU\nT'
        label = tk.Label(self, font = 'Courier 12', text =  text, height = 15,
                         background = 'turquoise')
        label.grid(row = 37, column = 0, sticky = tk.NSEW)
        
        #create a copy of current terminal input
        outFile = open('OutputFromTerminalDONOTTOUCH.txt', 'r')
        self.prevContents = outFile.read()
        outFile.close()
        
    #highlight java syntax
    def highlightJava(self):
        javaCode = self.javaText.get('1.0', tk.END)
        self.javaText.delete('1.0', tk.END)
        i = 0
        word = ''
        while i < len(javaCode):
            char = javaCode[i]
            if javaCode[i].isalpha():
                word += javaCode[i]
            else:
                if word in JavaLang.primitives:
                    self.javaText.insert(tk.END, word, 'primitives')
                elif word in JavaLang.keywords:
                    self.javaText.insert(tk.END, word, 'keyword')
                else: 
                    self.javaText.insert(tk.END, word, 'regular')
                word = ''
                self.javaText.insert(tk.END, char, 'regular')
            i += 1 
            
    #highlight java syntax
    def highlightPython(self):
        pythonCode = self.pythonText.get('1.0', tk.END)
        self.pythonText.delete('1.0', tk.END)
        i = 0
        word = ''
        while i < len(pythonCode):
            char = pythonCode[i]
            if pythonCode[i].isalpha():
                word += pythonCode[i]
            else:
                if word in PythonLang.keywords:
                    self.pythonText.insert(tk.END, word, 'keyword')
                else:
                    self.pythonText.insert(tk.END, word, 'regular')
                word = ''
                self.pythonText.insert(tk.END, char, 'regular')
            i += 1 
    
    def highlightLine(self):
        self.javaLineNumbers.config(state = tk.NORMAL)
        #clear previous highlight
        startOfLine = f'{self.currentLineNum-1}.0'
        startOfNextLine = f'{self.currentLineNum}.0'
        lineNumber = self.javaLineNumbers.get(startOfLine, startOfNextLine)
        self.javaLineNumbers.delete(startOfLine, startOfNextLine)
        self.javaLineNumbers.insert(startOfLine, lineNumber, 'regular')
        currentIndex = self.javaText.index(tk.INSERT)
        #highlight current line
        self.currentLineNum = int(float(currentIndex))+1
        startOfLine = f'{self.currentLineNum-1}.0'
        startOfNextLine = f'{self.currentLineNum}.0'
        lineNumber = self.javaLineNumbers.get(startOfLine, startOfNextLine)
        self.javaLineNumbers.delete(startOfLine, startOfNextLine)
        self.javaLineNumbers.insert(startOfLine, lineNumber, 'highlighter')
        self.javaLineNumbers.config(state = tk.DISABLED)
        #repeat for python line numbers
        self.pythonLineNumbers.config(state = tk.NORMAL)
        #clear previous highlight
        startOfLine = f'{self.pythonCurrentLine-1}.0'
        startOfNextLine = f'{self.pythonCurrentLine}.0'
        lineNumber = self.pythonLineNumbers.get(startOfLine, startOfNextLine)
        self.pythonLineNumbers.delete(startOfLine, startOfNextLine)
        self.pythonLineNumbers.insert(startOfLine, lineNumber, 'regular')
        currentIndex = self.pythonText.index(tk.INSERT)
        #highlight current line
        self.pythonCurrentLine = int(float(currentIndex))+1
        startOfLine = f'{self.pythonCurrentLine-1}.0'
        startOfNextLine = f'{self.pythonCurrentLine}.0'
        lineNumber = self.pythonLineNumbers.get(startOfLine, startOfNextLine)
        self.pythonLineNumbers.delete(startOfLine, startOfNextLine)
        self.pythonLineNumbers.insert(startOfLine, lineNumber, 'highlighter')
        self.pythonLineNumbers.config(state = tk.DISABLED)
        self.javaLineNumbers.after(50, self.highlightLine)
        
    #translate function
    def compile(self):
        javaCode = self.javaText.get('1.0',tk.END)
        (pythonCode, self.javaTree, self.pythonTree, 
         javaTokens, parseDepth) = Translator.compile(javaCode)
        print(pythonCode)
        self.pythonText.delete('1.0', tk.END)
        if pythonCode == '': #did not complete parse
            self.parseError = True
            errorMessage = """COMPILE ERROR 
###################################
# _____   _______________________ #
# |>!<|  | OH NO! OH NO! OH NO! | #
# -|*|--{| OH NO! OH NO! OH NO! | # 
#  [ ]   | OH NO! OH NO! OH NO! | #
# == ==  | OH NO! OH NO! OH NO! | #
###################################
"""
            self.pythonText.insert(tk.END, errorMessage, 'regular')
            self.highlightSyntaxException(javaTokens, parseDepth)
        else: #completed parsing and translation
            self.parseError = False
            self.pythonText.insert(tk.END, pythonCode, 'regular')
            self.highlightJava()
            self.highlightPython()
            
    #compiles current code and updates grammar file with grammar  
    def smartCompile(self):
        self.compile()
        if self.parseError == False:
            Parser2.makeTree(self.javaTree, 0)
            JavaLang.updateGrammar(self.javaTree)
            Parser2.GrammarData.refresh()
            
    #highlights code error in Java window
    def highlightSyntaxException(self, tokens, parseDepth):
        highlightToken = tokens[parseDepth-1]
        #find the index of token we want to highlight in textbox
        text = self.javaText.get('1.0', tk.END)
        textCopy = ''+text
        for i in range(parseDepth-1):
            text = text.lstrip().lstrip(tokens[i].string)
        countIndex = len(textCopy) - len(text) #index of token
        prevLineIndex = textCopy[:countIndex-1].rindex('\n')
        nextLineIndex = countIndex+textCopy[countIndex:].index('\n')
        textPt1 = textCopy[:prevLineIndex]
        highlight = textCopy[prevLineIndex:nextLineIndex]
        textPt2 = textCopy[nextLineIndex:]
        self.javaText.delete('1.0',tk.END)
        self.javaText.insert(tk.END, textPt1)
        self.javaText.insert(tk.END, highlight, 'error')
        self.javaText.insert(tk.END, textPt2)

def runApp():
    root = tk.Tk()
    root.title('MochaPythonIDE V1.0')
    app = MochaViperIDE(master=root)
    app.mainloop()
    
def main():
    runApp()

if __name__ == '__main__':
    main()