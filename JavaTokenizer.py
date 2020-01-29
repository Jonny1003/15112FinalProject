#######
#@Jonathan Ke
#@9/23/2019
#########
#Parses and converts Java code into list of tokens following description given by 
#https://www.cs.cmu.edu/~pattis/15-1XX/15-200/lectures/tokens/lecture.html
#The following algorithm is implemented:
'''
The first phase, a Java compiler tokenizes a program by scanning its characters left to right,
top to bottom (there is a hidden end-of-line character at the end of each line; recall that it 
is equivalent to white space), and combining selected characters into tokens. It works by repeating 
the following algorithm (an algorithm is a precise set of instructions):

Skip any white space...
...if the next character is an underscore, dollar, or alphabetic character, it builds an identifier token.
    Except for recognizing keywords and certain literals (true, false, null) which all share the form of 
    identifiers, but are not themselves identifiers
...if the next character is a numeric character, ' or ", it builds a literal token.
...if the next character is a period, that is a seperator unless the character after it is a numeric character (in 
    which case it builds a double literal).
...if the next two characters are a // or /* starting a comment, it builds a comment token.
...if the next character is anything else, it builds a separator or operator token (trying
    to build the longest token, given that white space separates tokens, except in a char or String literal).

Recall that white space (except when inside a textual literal or comment) separates tokens.
Also, the Java compiler uses the "longest token rule": it includes characters in a token until it reaches a 
character that cannot be included.

Finally, after building and recognizing each token, the Java compiler passes all tokens (except for comments, 
which are ignored after being tokenized) on to the next phase of the compiler.
'''
from Token import *
from JavaLang import JavaLang

def tokenize(code):
    '''str -> [Token]
    Creates a list of java tokens from input code
    '''
    out = []
    i = 0
    while i < len(code):
        if code[i].isspace():
            i += 1
        elif code[i] in '_$' or code[i].isalpha():
            #identifiers, keywords, true, false, null
            token = getNextWord(code[i:])
            if token in {'true','false','null'}:
                out.append(Literal(token))
            elif token in JavaLang.keywords:
                out.append(Keyword(token))
            else:
                out.append(Identifier(token))
            i += len(token)
        elif code[i].isnumeric() or code[i] == '"' or code[i] == "'": #literals
            token = getLiteral(code[i:])
            out.append(Literal(token))
            i += len(token)
        elif code[i:].startswith('//'): #comments
            if '\n' in code[i:]:
                endIndex = code.index('\n',i)
            else:
                endIndex = len(code)
            i = endIndex
        elif code[i:].startswith('/*'): #comments
            term = '*/'
            endIndex = code.find(term,i) 
            if endIndex == -1:
                raise CreateException('Comment not tokenizable', 'Check your comment ended!')
            i = endIndex
        elif code[i] in JavaLang.separators: #separators
            out.append(Separator(code[i]))
            i += 1
        else: #operators
            token = getOperator(code,i)
            out.append(Operator(token))
            i += len(token)
    return out
        
def getOperator(s, i):
    #parses out an operator
    if s[i:i+3] in JavaLang.operators:
        return s[i:i+3]
    elif s[i:i+2] in JavaLang.operators:
        return s[i:i+2]
    elif s[i] in JavaLang.operators:    
        return s[i]
    raise CreateException("OperatorNotFoundException", s[i:i+3] +" not recognized")
    
def peek(s, i):
    #light peeking function, handles index exceptions
    if i >= len(s):
        return None
    else:
        return s[i]

def getLiteral(s):
    #parses literals
    if s[0] == '"': #string literals
        return getString(s, '"')
    elif s[0] == "'": #char literals
        return getString(s, "'")
    else: #double, int, and long literals
        return getNum(s)

def getNextWord(s):
    #parses identifiers
    '''str -> str
    Gets the nearest word'''
    for i in range(len(s)):
        if not (s[i].isalnum() or s[i] == '_'):
            return s[:i]
    raise CreateException("WordNotFoundException", "Could not parse word")

def getString(s, char):
    '''str -> str
    Parses first Java string from input'''
    out = char
    i = 1
    while i < len(s):
        if s[i] == '\\':
            out += s[i:i+2]
            i+=2
        elif s[i] == char:
            return out + char
        else:
            out += s[i]
            i+= 1
    raise CreateException("STRINGNOTFOUNDEXCEPTION",
             "Could not parse string") #for debugging purposes

def getNum(s):
    #parses numerical literals
    for i in range(len(s)):
        if not s[i].isnumeric() and s[i] != '.':
            return s[:i]
    raise CreateException("NumberNotFoundException", "Could not parse number")

##Object Classes necessary for errors and using code
#######################################################
class CreateException(Exception):
    def __init__(self, exp, message):
        self.expression = exp
        self.message = message

#Test functions
#######################################################
def testTokenize():
    inputStr0 = '''
import java.util.Scanner;
import java.io.File;
public class PrintMyself{
    public static void main(String[] args) throws Exception{
        Scanner con = new Scanner(new File("PrintMyself.java"));
        while (con.hasNextLine()){
            System.out.println(con.nextLine());
            byte b = 'a';
        }
    }
    /**
     * 
     * dsjkaldjksjlajdk
     */
    //Obsdjfbwodfnjsnvlknffenvljnwfjlvnefjlbnefjlfvnerwkfidsodjfnakdnkasnvnfovoae
}
'''
#The following test is pulled from the website below:
#https://www.cs.cmu.edu/~pattis/15-1XX/15-200/lectures/tokens/lecture.html
    inputStr1 = '''
import java.util.Scanner;
import java.io.File;
public class PrintMyself{
    public static void main(String[] args) throws Exception{
        Scanner con = new Scanner(new File("PrintMyself.java"));
        while (con.hasNextLine()){
            System.out.println(con.nextLine());
            byte b = 'a';
            a = -1; 
        }
    }
    /**
     * 
     * dsjkaldjksjlajdk
     */
    //Obsdjfbwodfnjsnvlknffenvljnwfjlvnefjlbnefjlfvnerwkfidsodjfnakdnkasnvnfovoae
}
'''

    inputStr2 = '''
    //////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////
//
// Description:
//
//   This program computes the time it take to drop an object (in a vacuum)
// form an arbitrary height in an arbitrary gravitational field (so it can
// be used to calculate drop times on other planets). It models a straight
// input/calculate/output program: the user enters the gravitation field
// and then the height; it calculates thd drop time and then prints in on
// the console.
//
//////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////


import edu.cmu.cs.pattis.cs151xx.Prompt;


public class Application {


  public static void main(String[] args)
    {
      try {

        double gravity;        //meter/sec/sec
        double height;         //meters
        double time;           //sec
		  
		  
        //Input
		  
        gravity = Prompt.forDouble("Enter gravitational acceleration (in meters/sec/sec)");
        height  = Prompt.forDouble("Enter height of drop (in meters)");
		  
		  
        //Calculate
		  
        time = Math.sqrt(2.*height/gravity);
		  
		  
        //Output
		  
        System.out.println("\nDrop time = " + time + " secs");

		  
      }catch (Exception e) {
        e.printStackTrace();
        System.out.println("main method in Application class terminating");
        System.exit(0);  
   }

}
    '''
    print("#############START###########")
    out = tokenize(inputStr1)
    for L in out:
        print(L)
    print("############END#############")

#testTokenize()