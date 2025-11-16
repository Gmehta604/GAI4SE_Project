#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_81.h"

namespace CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_81
{

void CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_81_bad::action(int data) const
{
    {
        int i;
        int buffer[10] = { 0 };

        if (data >= 0)
        {
            buffer[data] = 1;
            
            for(i = 0; i < 10; i++)
            {
                printIntLine(buffer[i]);
            }
        }
        else
        {
            printLine("ERROR: Array index is negative.");
        }
    }
}

}
#endif 
