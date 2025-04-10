/**
 * Ezekiel A. Mitchell
 * Prof. Yueting Cheng
 * CPSC 2430 Data Structures
 * Lab 01 - Test Lab
 * April 09, 2025
 */

#include "lab1.h"
#include <iostream>
#include <cstdlib>
using namespace std;

// Main function: Process command-line arguments and manage triangle operations
int main(int argc, char* argv[]) {
    // Validate number of command-line arguments
    if (argc != 6) {
        cout << "Usage: ./lab1_main <height> <unit width> <start line> <span> <fill unit>" << endl;
        return 1;
    }
    
    // Parse command-line arguments
    int height = atoi(argv[1]);
    int unit = atoi(argv[2]);
    int start = atoi(argv[3]);
    int span = atoi(argv[4]);
    int fill = atoi(argv[5]);
    
    // Create, fill, print, and clean up triangle
    int** triangle = createTriangle(height, unit);
    fillTriangle(triangle, height, unit, start, span, fill);
    printTriangle(triangle, height, unit);
    deleteTriangle(triangle, height);
    
    return 0;
}