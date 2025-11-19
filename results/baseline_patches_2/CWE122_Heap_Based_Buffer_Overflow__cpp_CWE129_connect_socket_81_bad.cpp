#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE122_Heap_Based_Buffer_Overflow__cpp_CWE129_connect_socket_81.h"

namespace CWE122_Heap_Based_Buffer_Overflow__cpp_CWE129_connect_socket_81
{

void CWE122_Heap_Based_Buffer_Overflow__cpp_CWE129_connect_socket_81_bad::action(int data) const
{
    {
        int i;
        int * buffer = new int[10];
       
        for (i = 0; i < 10; i++)
        {
            buffer[i] = 0;
        }
        if (data >= 0 && data <= (10 - 1))
        {
            buffer[data] = 1;
            
            for(i = 0; i < 10; i++)
            {
                printIntLine(buffer[i]);
            }
        }
        else
        {
            printLine("ERROR: Array index is out-of-bounds");
        }
        delete[] buffer;
    }
}

}
#endif