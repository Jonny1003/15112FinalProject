class NearestOdd :
    def main ( self , args ) :
        print ( self . nearestOdd ( 13 ) == 13 ) 
        print ( self . nearestOdd ( 12 ) == 11 ) 
        print ( self . nearestOdd ( - 13 ) == - 13 ) 
        print ( self . nearestOdd ( - 12 ) == - 13 ) 

    def nearestOdd ( self , a ) :
        
        if ( a % 2 == 0 ) :
            
            
            if ( a + 1 - a < 1 ) :
                
                return a + 1 

            else :
                
                return a - 1 


        else :
            
            return a 



NearestOdd().main('')


