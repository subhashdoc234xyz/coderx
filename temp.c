#include <stdio.h>

int main() {
    int numbers[10]; // Declare an array to store 10 integers
    int i;           // Loop counter

    // Loop to get 10 integer inputs from the user
    printf("Please enter 10 integers:\n");
    for (i = 0; i < 10; i++) {
        printf("Enter integer %d: ", i + 1);
        scanf("%d", &numbers[i]); // Read an integer and store it in the array
    }

    // Loop to print the 10 stored integers
    printf("\nYou entered the following integers:\n");
    for (i = 0; i < 10; i++) {
        printf("Integer %d: %d\n", i + 1, numbers[i]);
    }

    return 0; // Indicate successful execution
}