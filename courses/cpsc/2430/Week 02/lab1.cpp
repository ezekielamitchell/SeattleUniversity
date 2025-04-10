#include <iostream>
#include "lab1.h"
using namespace std;

// Function 1. Create Triangle: Dynamically allocate a triangle with border 1s
int** createTriangle(int n, int m) {
    // Allocate array of pointers for rows
    int** triangle = new int*[n];
    
    for (int i = 0; i < n; ++i) {
        // Calculate width of each row: increases with row number
        int width = (i + 1) * m;
        triangle[i] = new int[width];
        
        // Set border elements to 1, interior elements to 0
        for (int j = 0; j < width; ++j) {
            if (i == 0 || i == n - 1 || j == 0 || j == width - 1) {
                triangle[i][j] = 1;
            } else {
                triangle[i][j] = 0;
            }
        }
    }
    return triangle;
}

// Function 2. Fill Triangle: Selectively fill a sub-region with 2s
void fillTriangle(int** triangle, int n, int m, int start_n, int span_n, int fill_m) {
    // Iterate through specified rows, avoiding out-of-bounds access
    for (int i = start_n; i < start_n + span_n && i < n - 1; ++i) {
        // Calculate line length and fill area
        int line_len = (i + 1) * m;
        int fill_count = (i - start_n + 1) * fill_m;
        int start_index = 1;
        
        // Fill elements with 2, respecting line boundaries
        for (int j = 0; j < fill_count && start_index + j < line_len - 1; ++j) {
            triangle[i][start_index + j] = 2;
        }
    }
}

// Function 3. Print Triangle: Display triangle elements with spacing
void printTriangle(int** triangle, int n, int m) {
    for (int i = 0; i < n; ++i) {
        // Calculate row width and print all elements
        int width = (i + 1) * m;
        for (int j = 0; j < width; ++j) {
            cout << triangle[i][j] << " ";
        }
        cout << endl;
    }
}

// Function 4. Delete Triangle: Free dynamically allocated memory
void deleteTriangle(int** triangle, int n) {
    // Delete each row first
    for (int i = 0; i < n; ++i) {
        delete[] triangle[i];
    }
    // Delete the array of pointers
    delete[] triangle;
}