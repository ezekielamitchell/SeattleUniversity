#ifndef LAB1_H
#define LAB1_H

int** createTriangle(int n, int m);
void fillTriangle(int** triangle, int n, int m, int start_n, int span_n, int fill_m);
void printTriangle(int** triangle, int n, int m);
void deleteTriangle(int** triangle, int n);

#endif
