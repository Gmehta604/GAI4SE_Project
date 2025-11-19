#include <windows.h>

void CWE176_Improper_Handling_of_Unicode_Encoding__w32_82_good::action(wchar_t * data)
{
    {
        char convertedText[10];
        int requiredSize = WideCharToMultiByte(CP_ACP, WC_COMPOSITECHECK, data, -1, convertedText, sizeof(convertedText), 0, 0);
        if (requiredSize == 0)
        {
            /* Handle error */
        }
        else
        {
            WideCharToMultiByte(CP_ACP, WC_COMPOSITECHECK, data, -1, convertedText, requiredSize, 0, 0);
        }
    }
}