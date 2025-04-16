#include <iostream>

using namespace std;

struct Node {
    int data;
    Node* left;
    Node* right;
};

// Iterative
int minVal(Node* root) {
    Node* current = root;
    while (current->left != NULL){
        current = current->left;
    }
    return current->data;
}

// Recursive
int minValue(Node* root) {
    if (root->left == NULL){
        return root->data;
    }
    return minValue(root->left);
}

int maxLinear(const int arr[], int n) {
    // Base case
    if (n==1){
        return arr[0];
    }
    // Recursive case
    int maxOfRest = maxLinear(arr, n-1);
    return (maxOfRest > arr[n-1]) ? maxOfRest : arr[n-1];
}

int maxBinary(const int arr[], int left, int right){
    if (left==right){return arr[left];}
    if (right - left == 1){return arr[left] > arr[right] ?}

}

int main(){
    cout << "pass" << endl;
    return 0;
}