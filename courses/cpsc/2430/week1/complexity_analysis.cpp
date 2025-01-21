#include <iostream>
#include <string>
#include <chrono>
using namespace std;
using namespace std::chrono;

void numberSwapOne(int x, int y) {
    auto start = high_resolution_clock::now();

    int temp = x;
    x = y;
    y = temp;

    std::cout << "x: " << x << std::endl;
    std::cout << "y: " << y << std::endl;

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);

    cout << "Method 1: " << duration.count() << endl;
}

void numberSwapTwo(int x, int y) {
    auto start = high_resolution_clock::now(); // start timer

    x = x + y;
    y = x - y;
    x = x - y;

    std::cout << "x: " << x << std::endl;
    std::cout << "y: " << y << std::endl;

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<microseconds>(stop - start);

    cout << "Method 2: " << duration.count() << endl;
}

int main() {
    int a = 5, b = 10;
    numberSwapOne(a, b);
    numberSwapTwo(a, b);
    return 0;
}