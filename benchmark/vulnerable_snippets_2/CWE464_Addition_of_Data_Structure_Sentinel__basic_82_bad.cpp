
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE464_Addition_of_Data_Structure_Sentinel__basic_82.h"

namespace CWE464_Addition_of_Data_Structure_Sentinel__basic_82
{

void CWE464_Addition_of_Data_Structure_Sentinel__basic_82_bad::action(char data)
{
    {
        char charArraySink[4];
        charArraySink[0] = 'x';
        
        charArraySink[1] = data;
        charArraySink[2] = 'z';
        charArraySink[3] = '\0';
        printLine(charArraySink);
    }
}

}
#endif 
