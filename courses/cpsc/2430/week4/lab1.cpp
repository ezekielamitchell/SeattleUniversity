/*
Ezekiel A. Mitchell
Prof. Xin Zhao
CPSC [2430] Data Structures
January 27, 2024
Lab #1
*/

#include<iostream>

using namespace std;

void mystery(int number) { // Big O : O(n)
    int x=0, y=1, z=0;
    for (int i=0; i<number; i++) {
        cout << x << " ";
        z=x+y;
        x=y;
        y=z;
    }
}

void nestedLoop(int n) {
    for (int i=1; i<=n; i++){
        for (int j=1; j<n; j++){
            for (int k=n; k>=1; k--){
                int sum = i+j+k;
                cout << sum << endl;
            }
        }
    }
}

void nestedLoopTwo(int N){
    int a=0;
    for (int i=0; i<N; i++){
        for(int j=N; j>i; j--){
            a = a+i+j;
        }
    }
}

void nestedLoopThree(int n){
    for (int i=1; i<=n; i++){
        for (int j=1; j<=100; j++){
            int sum = i+j;
        }
    }
}

void nestedLoopFour(int n){
    for (int i=0; i<n; i++){
        for (int j=i; j>0; j/=2){
            cout << j << endl;
        }
    }
}

int main() {
    nestedLoopFour(3);
    return 0;
}