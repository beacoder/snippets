/** 
 * gcc compile command is :
 * gcc -g -Wall -L/usr/lib checkmem.c -o checkmem
 */

#include <stdio.h>
#include <stdlib.h>

typedef unsigned char byte;

static void provideChunk(void **pChunk, int elemNum, int elemSize)
{
  if (NULL != pChunk)
  {
    *pChunk = (void *)calloc(elemNum, elemSize);    
  }  
}

int main(int argc, char *argv[])
{
  byte **** pChunk4 = NULL;

  int size = sizeof(byte*);
  provideChunk((void **)&pChunk4, 14, size);
  printf ("address of p and p+1 of type \"byte ****\" is %p --> %p, %d !",
          pChunk4, pChunk4 + 1,
          (int)(*(pChunk4-1)));
  printf ("\n");

  byte *** pChunk3 = NULL;
  provideChunk((void **)&pChunk3, 13, size);
  printf ("address of p and p+1 of type \"byte ***\" is %p --> %p, %d !",               pChunk3, pChunk3 + 1,
          (int)(*(pChunk3-1)));
  printf ("\n");

  byte ** pChunk2 = NULL;
  provideChunk((void **)&pChunk2, 12, size);
  printf ("address of p and p+1 of type \"byte **\" is %p --> %p, %d !",
          pChunk2, pChunk2 + 1,
          (int)(*(pChunk2-1)));
  printf ("\n");

  byte * pChunk1 = NULL;
  provideChunk((void **)&pChunk1, 11, size);
  printf ("address of p and p+1 of type \"byte *\" is %p --> %p, %d !",
          pChunk1, pChunk1 + 1,
          (int)(*(pChunk1-1)));
  printf ("\n");
  
  return 0;
}
