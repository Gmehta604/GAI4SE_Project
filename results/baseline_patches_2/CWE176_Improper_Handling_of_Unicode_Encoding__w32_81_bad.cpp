#include <windows.h>

void CWE176_Improper_Handling_of_Unicode_Encoding__w32_81_good::action(wchar_t * data) const
{
    {
        char convertedText[10] = "";
        int requiredSize;
        requiredSize = WideCharToMultiByte(CP_UTF8, WC_COMPOSITECHECK, data, -1, convertedText, 0, 0, 0);
        WideCharToMultiByte(CP_UTF8, WC_COMPOSITECHECK, data, -1, convertedText, requiredSize , 0, 0);
    }
}