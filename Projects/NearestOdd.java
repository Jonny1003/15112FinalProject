

public class NearestOdd {

   public static void main(String[] args) {
        System.out.println(nearestOdd(13) == 13);
    		System.out.println(nearestOdd(12) == 11);
    		System.out.println(nearestOdd(-13) == -13);
    		System.out.println(nearestOdd(-12) == -13);
   }

	public static int nearestOdd(int a){
		if (a%2 == 0){
			if (a+1-a < 1){
				return a+1;
			} else {
				return a-1;
			}
		} else {
			return a;
		}
	}
}
        














