#include <iostream>

using namespace std;

// Recursion
// Occurs when a function calls itself in its own definition
/**
 * Requirements:
 * 1. Base case (stop condition)
 * 2. Recursive case - breaks problem insto smaller instances
 */


// ** Types of Recursion ** //

// LINEAR : At most (1) recursive call
int sum(const int arr[], int n) {
    // Base case: empty array
    if (n == 0) {
        return 0;
    }
    // Base case: single element
    if (n == 1) {
        return arr[0];
    }
    // Recursive case
    return sum(arr, n - 1) + arr[n - 1]; // ONLY (1) CALL
}

// BINARY : At most (2) recursive calls
int fibb(int n) {
    // Base cases
    if (n <= 1) {
        return n;
    }
    // Recursive case
    return fibb(n-1) + fibb(n-2);
}

// MULTIPLE : multiple recursive calls

int factorial(int n) {
    int result = 1;
    for (int i=1; i<=n; i++){
        result *= i;
    }
    return result;
}


int main(){
    const int ar[5] = {1, 2, 3, 4, 5};
    cout << sum(ar, 5) << endl;  // Pass the actual size of the array

    cout << "Fibonacci sequence:" << endl;
    for (int i=0; i<9; i++){
        cout << fibb(i) << " ";
    }
    cout << endl;

    // A dynamic array is an array whose size can be determined at runtime rather than
    // compile time

    // create dynamic array
    int size = 5;
    int* arr = new int[size];

    // use array
    for (int i=0; i<size; i++) {
        arr[i] += 1;
        cout << arr[i] << endl;
    }

    swap(arr[2], arr[4]);

    // must deallocate when done
    delete[] arr;
    arr = nullptr;

    // Create 2D dynamic array
    int rows = 3;
    int cols = 4;
    int** matrix = new int*[rows];
    for (int i=0; i<rows; i++){
        matrix[i] = new int[cols];
        cout << matrix[i] << endl;
    }
    // Deallocate 2D array
    for (int i=0; i<rows; i++){
        delete[] matrix[i];
    }

    delete[] matrix;
    matrix = nullptr;

    cout << factorial(0) << endl;

    return 0;
}