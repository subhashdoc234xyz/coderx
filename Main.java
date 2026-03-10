import java.util.Scanner;

class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int[] numbers = new int[10];

        System.out.println("Enter 10 integers:");

        // Read 10 integers
        for (int i = 0; i < 10; i++) {
            numbers[i] = scanner.nextInt();
        }

        // Print the integers
        System.out.println("You entered:");
        for (int i = 0; i < 10; i++) {
            System.out.println(numbers[i]);
        }

        scanner.close();
    }
}