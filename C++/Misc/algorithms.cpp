/** 
 * gcc compile command is :
 * g++ -g -Wall algorithms.cpp -o algorithms
*/

#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

using namespace std;

// constexpr objects are const and are initialized with values known during compilation.
// constexpr functions can produce compile-time results when called with arguments
// whose values are known during compilation.
constexpr uint32_t MAXNUMBER = 50000;

void BubbleSort(int *array, int n);
void SelectionSort(int *array, int n);
void InsertionSort(int *array, int n);
void QuickSort(int *array, int l, int r);
int BinarySearch(int *array, int n, int value);

int main(void)
{
  // init rand function
  srand (time(NULL));

  int numbers[MAXNUMBER];
  for(int i = 0; i < MAXNUMBER; ++i)
    numbers[i] = rand();

  time_t beg, end; 
  double elapsed;
  time(&beg);

  //BubbleSort(numbers, MAXNUMBER);
  //SelectionSort(numbers, MAXNUMBER);
  //InsertionSort(numbers, MAXNUMBER);
  QuickSort(numbers, 0, MAXNUMBER - 1);
  BinarySearch(numbers, MAXNUMBER, 100);

  time(&end);
  elapsed = diff
