import math
class IsPerfectSquare :
    def main ( self , args ) :
        print ( self . isPerfectSquare ( 0 ) == True ) 
        print ( self . isPerfectSquare ( 1 ) == True ) 
        print ( self . isPerfectSquare ( 16 ) == True ) 
        print ( self . isPerfectSquare ( 1234 * 1234 ) == True ) 
        print ( self . isPerfectSquare ( 15 ) == False ) 
        print ( self . isPerfectSquare ( - 16 ) == False ) 

    def isPerfectSquare ( self , n ) :
        if ( n < 0 ) :
            
            return False 

        x = math . sqrt ( n ) 
        if ( x * x == n ) :
            
            return True 

        return False 




IsPerfectSquare().main('')



