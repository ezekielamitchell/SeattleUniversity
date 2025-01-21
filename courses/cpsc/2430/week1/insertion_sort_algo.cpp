#include <iostream>
#include <cmath>

using namespace std;

int* insertion_sort(int list[], int size) {
    for (int i=1; i<size; i++) {
        int key = list[i];
        int j = i - 1;
        while (j >= 0 && list[j] > key) {
            j = j - 1;
        }
        list[j+1]=key;
    }
    
    for (int i = 0; i < size; i++){
        cout << list[i] << ' ';
    }

    return list;
}


int main() {
    int list[] = {5, 3, 2, 4, 1};
    int size = 0;

    for (int i=0; i<sizeof(list)/sizeof(list[0]); i++){
        size++;
    }

    insertion_sort(list, size);


    return 1;
}