#include <iostream>
#include <vector>
#include <assert.h>
#include <stdlib.h>
#include <time.h>

using namespace std;
#define MAXNUMBER 20000

void BubbleSort(int *number, int n);
void SelectionSort(int *number, int n);

void PrintArray(int *number, int n)
{
    for(int i = 0; i < n; ++i)
    {
        cout << number[i] << std::string(" ");
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
    SelectionSort(numbers, MAXNUMBER);

    time(&end);
    elapsed = difftime(end, beg);

    cout << "time elapsed in seconds" << std::endl;
    cout << elapsed << std::endl;

    //PrintArray(numbers, MAXNUMBER);

    return 0;
}

// 冒泡排序
void BubbleSort(int *number, int n)
{
    int temp = 0;
    for(int i = n; i > 0; --i)
    {
        for(int j = 0; j < i-1; ++j)
        {
            if(number[j] > number[j+1])
            {
                std::swap(number[j], number[j+1]);
            }
        }
    }
}

// 选择排序
void SelectionSort(int *number, int n)
{
    for(int j = 0; j < n; ++j)
    {
        int min = j;

        for(int i = j; i < n; ++i)
        {
            if(number[min] > number[i])
            {
                min = i;
            }
        }

        std::swap(number[j], number[min]);
    }
}