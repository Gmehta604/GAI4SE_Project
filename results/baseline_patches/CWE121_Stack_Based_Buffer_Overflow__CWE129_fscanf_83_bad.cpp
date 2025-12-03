#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_83.h"

namespace CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_83
{
CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_83_bad::CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_83_bad(int dataCopy)
{
    data = dataCopy;
    
    fscanf(stdin, "%d", &data);
}

CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_83_bad::~CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_83_bad()
{
    {
        int i;
        int buffer[10] = { 0 };

        if (data >= 0 && data <= (10-1))
        {
            buffer[data] = 1;
            
            for(i = 0; i < 10; i++)
            {
                printIntLine(buffer[i]);
            }
        }
        else
        {
            printLine("ERROR: Array index is out of bounds");
        }
    }
}
}
#endif