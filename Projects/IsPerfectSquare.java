

public class IsPerfectSquare {

   public static void main(String[] args) {
        System.out.println(isPerfectSquare(0) == true);
    		System.out.println(isPerfectSquare(1) == true);
    		System.out.println(isPerfectSquare(16) == true);
    		System.out.println(isPerfectSquare(1234*1234) == true);
    		System.out.println(isPerfectSquare(15) == false);
    		System.out.println(isPerfectSquare(-16) == false);
   }

	public static boolean isPerfectSquare(int n){
		if (n < 0){
			return false;
		}
		double x = Math.sqrt(n);
		if (x*x == n){
			return true;
		}
		return false;
	}
}
        







