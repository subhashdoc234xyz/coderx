import java.util.Scanner;

class IntegerInputPrinter {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Loop through each integer input
        for (int i = 0; i < 10; i++) {
            System.out.print("Enter an integer: ");
            int number = scanner.nextInt();

            // Print the integer
            System.out.println(number);
        }

        // Close the scanner to release resources
        scanner.close();
    }
}