/** 
 * gcc compile command is :
 * g++ -g -Wall algorithms.cpp -o algorithms
*/

#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

using namespace std;

// constexpr => evaluated in compile time.
// constexpr functions will be evaluated at compile time when all its arguments are constant expressions
// and the result is used in a constant expression as well.
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
  elapsed = difftime(end, beg);

  cout << "Sort and Search\n\n";
  cout << "sort " << MAXNUMBER << " numbers\n";
  cout << "time elapsed in " << elapsed << " seconds\n\n" << std::endl;
  
  return 0;
}

void BubbleSort(int *array, int n)
{
  for(int i = n; i > 0; --i)
  {
    for(int j = 0; j < i-1; ++j)
    {
      if(array[j] > array[j+1])
      {
        std::swap(array[j], array[j+1]);
      }
    }
  }
}

void SelectionSort(int *array, int n)
{
  for(int j = 0; j < n; ++j)
  {
    int min = j;
    for(int i = j; i < n; ++i)
    {
      if(array[min] > array[i])
      {
        min = i;
      }
    }

    std::swap(array[j], array[min]);
  }
}

void InsertionSort(int *array, int n)
{
  int j, pivot;
  
  for(int i = 1; i < n; ++i)
  {
    pivot = array[i];

    // find the first element smaller than pivot,
    // starting from array[i-1]
    j = i - 1;
    while ((0 <= j) && (array[j] > pivot))
    {
      array[j+1] = array[j];
      --j;
    }

    // right position for pivot
    array[j+1] = pivot;
  }
}

int partition(int *array, int left, int right)
{
  int i = left-1, j = right, pivot = array[right];

  for (;;)
  {
    // find the first one which is bigger than pivot
    while (array[++i] < pivot) ;

    // find the first one which is smaller than pivot
    while (array[--j] > pivot) if(left == j) break;

    // if the bigger one is on the right of the smaller one,
    // then we don't have to swap them
    if(i >= j) break;

    // swap the bigger one with the smaller one
    std::swap(array[i], array[j]);
  }

  // at last, we find the right final position for pivot in the array
  // left is smaller than pivot and right is bigger than pivot
  std::swap(array[i], array[right]);
  return i;
}

void QuickSort(int *array, int left, int right)
{
  if (left >= right) return;

  // divide and conquer
  int border = partition(array, left, right);
  QuickSort(array, left, border-1);
  QuickSort(array, border+1, right);
}

int BinarySearch(int *array, int n, int value)
{
  int mid = 0, left = 0, right = n-1;

  while(left <= right)
  {
    mid = (left + right)/2;

    if(array[mid] < value)
      left = mid + 1;
    else if(array[mid] > value)
      right = mid - 1;
    else
      return mid;
  }

  return -1;
}
