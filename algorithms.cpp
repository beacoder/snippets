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
	      std::swap(number[j], number[j+1])
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
