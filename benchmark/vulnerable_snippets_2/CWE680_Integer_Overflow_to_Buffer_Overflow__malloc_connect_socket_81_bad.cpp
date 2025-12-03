#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE680_Integer_Overflow_to_Buffer_Overflow__malloc_connect_socket_81.h"

namespace CWE680_Integer_Overflow_to_Buffer_Overflow__malloc_connect_socket_81
{

void CWE680_Integer_Overflow_to_Buffer_Overflow__malloc_connect_socket_81_bad::action(int data) const
{
    {
        size_t i;
        int *intPointer;
                intPointer = (int*)malloc(data * sizeof(int));
        if (intPointer == NULL) {exit(-1);}
        for (i = 0; i < (size_t)data; i++)
        {
            intPointer[i] = 0; 
        }
        printIntLine(intPointer[0]);
        free(intPointer);
    }
}

}
#endif 
