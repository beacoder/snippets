#include <iostream>
#include <vector>
#include <assert.h>
#include <stdlib.h>
#include <time.h>

using namespace std;
#define MAXNUMBER 50000

void PrintArray(int *array, int n);
void BubbleSort(int *array, int n);
void SelectionSort(int *array, int n);
void QuickSort(int *array, int l, int r);
int BinarySearch(int *array, int n, int value);

// define single list
struct _Node
{
  int     data;
  _Node * next;

  ~_Node()
  {
    cout << data << " is freed !" << std::endl;
  }
};
typedef struct _Node Node, * PNode;

void PrintSingleList(PNode head);
PNode CreateSingleList(int *array, int n);
PNode ReverseSingleList(PNode head);
void FreeSingleList(PNode head);

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
  int result = BinarySearch(numbers, MAXNUMBER, 100);

  time(&end);
  elapsed = difftime(end, beg);

  cout << "Sort and Search" << std::endl << std::endl;
  cout << "sort " << MAXNUMBER << " numbers" << std::endl;
  cout << "time elapsed in " << elapsed << " seconds" << std::endl;
  //PrintArray(numbers, MAXNUMBER);

  cout << std::endl << std::endl;
  
  // single list
  int list[10] = {1,2,3,4,5,6,7,8,9,10};
  PNode head = CreateSingleList(list, 10);

  cout << "single list operation" << std::endl << std::endl;
  cout << "list before reverse" << std::endl;
  PrintSingleList(head);

  cout << "list after reverse" << std::endl;
  PNode new_head = ReverseSingleList(head);
  PrintSingleList(new_head);

  cout << std::endl << "free the heap space occupied by the list" << std::endl;
  FreeSingleList(new_head);
  
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
      while (array[--j] > pivot) if(left == j) break;

      // if the bigger one is on the right of the smaller one,
      // then we don't have to swap them
      if(i >= j) break;

      // swap the bigger one with the smaller one
      std::swap(array[i], array[j]);
  }

  // at last, we find the right final position for pivot in the array
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
        {
            left = mid + 1;
        }
        else if(array[mid] > value)
        {
            right = mid - 1;
        }
        else
            return mid;
    }

    return -1;
}

// create single list with same order as array's
PNode CreateSingleList(int *array, int n)
{
  PNode head, pre;
  head = pre = NULL;
  
  for(int i = 0; i < n; ++i)
  {
    Node* pNode = new Node();
    pNode->data = array[i];

    // head Node
    if(NULL == pre)
    {
      pre = pNode;
      head = pNode;
    }
    else
    {
      pre->next = pNode;
      pre = pNode;
    }
  }

  // tail Node
  if(NULL != pre)
    pre->next = NULL;
  
  return head;
}

// tail insert method to reverse the single list
PNode ReverseSingleList(PNode head)
{
  if(NULL == head)
    return NULL;

  PNode cur,next,new_head;
  cur = head;
  new_head = NULL;

  while(NULL != cur)
  {
    next = cur->next;
    
    cur->next = new_head;
    new_head = cur;

    cur = next;
  }

  return new_head;
}

void PrintSingleList(PNode head)
{
  PNode cur = head;
  
  while(NULL != cur)
  {
    cout << cur->data << " -> ";
    cur = cur->next;
  }

  cout << "NULL" << std::endl;
}

void PrintArray(int *array, int n)
{
  for(int i = 0; i < n; ++i)
  {
    cout << array[i] << std::string(" ");
  }

  cout << std::endl;
}

void FreeSingleList(PNode head)
{
  PNode cur = head;
  PNode temp = NULL;
  
  while(NULL != cur)
  {
    temp = cur;
    cur = cur->next;
    delete temp;
  }
}
