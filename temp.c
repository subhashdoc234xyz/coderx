#include <stdio.h>

int main() {
    int numbers[10]; // Declare an array to store 10 integers
    int i;           // Loop counter

    printf("Enter 10 integers:\n");

    // Loop to get 10 integer inputs
    for (i = 0; i < 10; i++) {
        printf("Enter integer %d: ", i + 1);
        if (scanf("%d", &numbers[i]) != 1) {
            printf("Invalid input. Please enter an integer.\n");
            // Optionally handle error or exit
            return 1; // Indicate an error
        }
    }

    printf("\nYou entered the following integers:\n");

    // Loop to print the 10 stored integers
    for (i = 0; i < 10; i++) {
        printf("Integer %d: %d\n", i + 1, numbers[i]);
    }

    return 0; // Indicate successful execution
}