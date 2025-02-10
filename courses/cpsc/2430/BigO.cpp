#include <iostream>
#include <vector>
#include <algorithm>

// Function with O(1) complexity
// This function performs a constant time operation
void constantTimeOperation(int n) {
    std::cout << "Constant time operation: " << n << std::endl;
}

// Function with O(n) complexity
// This function performs a linear time operation
void linearTimeOperation(const std::vector<int>& vec) {
    for (int i : vec) {
        std::cout << i << " ";
    }
    std::cout << std::endl;
}

// Function with O(n^2) complexity
// This function performs a quadratic time operation
void quadraticTimeOperation(const std::vector<int>& vec) {
    for (size_t i = 0; i < vec.size(); ++i) {
        for (size_t j = 0; j < vec.size(); ++j) {
            std::cout << vec[i] << ", " << vec[j] << " ";
        }
        std::cout << std::endl;
    }
}

// Function with O(log n) complexity
// This function performs a logarithmic time operation
void logarithmicTimeOperation(const std::vector<int>& vec, int target) {
    bool found = std::binary_search(vec.begin(), vec.end(), target);
    std::cout << "Element " << (found ? "found" : "not found") << std::endl;
}


// Function with O(n log n) complexity
// This function performs a linearithmic time operation
void linearithmicTimeOperation(std::vector<int>& vec) {
    std::sort(vec.begin(), vec.end());
    for (int i : vec) {
        std::cout << i << " ";
    }
    std::cout << std::endl;
}

int main() {
    std::vector<int> vec = {5, 3, 8, 6, 2, 7, 4, 1};

    constantTimeOperation(10);
    linearTimeOperation(vec);
    quadraticTimeOperation(vec);
    logarithmicTimeOperation(vec, 2);
    linearithmicTimeOperation(vec);

    return 0;
}