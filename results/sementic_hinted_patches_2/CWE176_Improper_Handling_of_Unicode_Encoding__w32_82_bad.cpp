#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE176_Improper_Handling_of_Unicode_Encoding__w32_82.h"

namespace CWE176_Improper_Handling_of_Unicode_Encoding__w32_82
{

void CWE176_Improper_Handling_of_Unicode_Encoding__w32_82_bad::action(wchar_t * data)
{
    {
        char convertedText[10] = "";
        int requiredSize = WideCharToMultiByte(CP_ACP, WC_COMPOSITECHECK, data, -1, convertedText, sizeof(convertedText), 0, 0);
        if (requiredSize > 0 && requiredSize < sizeof(convertedText))
        {
            WideCharToMultiByte(CP_ACP, WC_COMPOSITECHECK, data, -1, convertedText, requiredSize, 0, 0);
        }
    }
}

}
#endif