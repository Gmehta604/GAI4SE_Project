
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE176_Improper_Handling_of_Unicode_Encoding__w32_81.h"

namespace CWE176_Improper_Handling_of_Unicode_Encoding__w32_81
{

void CWE176_Improper_Handling_of_Unicode_Encoding__w32_81_bad::action(wchar_t * data) const
{
    {
        char convertedText[10] = "";
        int requiredSize;
        requiredSize = WideCharToMultiByte(CP_ACP, WC_COMPOSITECHECK, data, -1, convertedText, 0, 0, 0);
        WideCharToMultiByte(CP_ACP, WC_COMPOSITECHECK, data, -1, convertedText, requiredSize , 0, 0);
    }
}

}
#endif 
