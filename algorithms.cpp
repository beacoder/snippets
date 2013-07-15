#include <iostream>
#include <vector>
#include <assert.h>
#include <stdlib.h>
#include <time.h>

using namespace std;
#define MAXNUMBER 50000

void BubbleSort(int *array, int n);
void SelectionSort(int *array, int n);
void QuickSort(int *array, int l, int r);

void PrintArray(int *array, int n)
{
  for(int i = 0; i < n; ++i)
    {
      cout << array[i] << std::string(" ");
    }

  cout << std::endl;
}

int main(void)
{
  // init rand function
  srand (time(NULL));

  int numbers[MAXNUMBER];
  for(int i = 0; i < MAXNUMBER; ++i)
    {
      numbers[i] = rand();
    }

  time_t beg, end; 
  double elapsed;
  time(&beg);

  //BubbleSort(numbers, MAXNUMBER);
  //SelectionSort(numbers, MAXNUMBER);
  QuickSort(numbers, 0, MAXNUMBER - 1);

  time(&end);
  elapsed = difftime(end, beg);

  cout << "time elapsed in seconds" << std::endl;
  cout << elapsed << std::endl;

  //PrintArray(numbers, MAXNUMBER);

  return 0;
}

void BubbleSort(int *array, int n)
{
  int temp = 0;
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

int partition(int *array, int left, int right)
{
  int i = left-1, j = right, pivot = array[right];

  for (;;)
    {
      // find the first one which is bigger than pivot
      while (array[++i] < pivot) ;

      // find the first one which is smaller than pivot
      while (array[--j] > pivot) if(j == left) break;

      // if the bigger one is on the right of the smaller one,
      // then we don't have to swap them
      if(i >= j) break;

      // swap the bigger one with the smaller one
      std::swap(array[i], array[j]);
    }

  std::swap(array[i], array[right]);
  return i;
}

void QuickSort(int *array, int left, int right)
{
  if (right <= left) return;

  // divide and conquer
  int border = partition(array, left, right);
  QuickSort(array, left, border-1);
  QuickSort(array, border+1, right);
}
