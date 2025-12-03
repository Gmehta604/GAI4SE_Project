#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_83.h"

#define CHAR_ARRAY_SIZE (3 * sizeof(data) + 2)

namespace CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_83
{
CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_83_bad::CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_83_bad(int dataCopy)
{
    data = dataCopy;
    {
        char inputBuffer[CHAR_ARRAY_SIZE] = "";
        if (fgets(inputBuffer, CHAR_ARRAY_SIZE, stdin) != NULL)
        {
            
            data = atoi(inputBuffer);
        }
        else
        {
            printLine("fgets() failed.");
        }
    }
}

CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_83_bad::~CWE121_Stack_Based_Buffer_Overflow__CWE129_fgets_83_bad()
{
    {
        int i;
        int buffer[10] = { 0 };

        if (data >= 0 && data <= 9)
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
    }
}
}
#endif