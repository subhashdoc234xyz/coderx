import java.util.Scanner;

class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        
        // Loop runs exactly 10 times
        for (int i = 1; i <= 10; i++) {
            System.out.print("Enter integer #" + i + ": ");
            int number = input.nextInt(); // Captures the input
            
            System.out.println("You entered: " + number);
        }
        
        input.close(); // Good practice to close the scanner
    }
}