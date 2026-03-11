import java.util.Scanner;

class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int[] numbers = new int[10]; // Array to store 10 integers

        System.out.println("Please enter 10 integers:");

        // Loop to ask for 10 integer inputs
        for (int i = 0; i < 10; i++) {
            System.out.print("Enter integer " + (i + 1) + ": ");
            numbers[i] = scanner.nextInt(); // Read integer input and store in the array
        }

        System.out.println("\nYou entered the following integers:");

        // Loop to print the stored integers
        for (int i = 0; i < 10; i++) {
            System.out.println("Integer " + (i + 1) + ": " + numbers[i]);
        }
        
        scanner.close(); // Close the scanner to prevent resource leaks
    }
}