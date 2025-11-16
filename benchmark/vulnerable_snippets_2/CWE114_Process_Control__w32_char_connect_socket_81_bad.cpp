
#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE114_Process_Control__w32_char_connect_socket_81.h"

#include <windows.h>

namespace CWE114_Process_Control__w32_char_connect_socket_81
{

void CWE114_Process_Control__w32_char_connect_socket_81_bad::action(char * data) const
{
    {
        HMODULE hModule;
        hModule = LoadLibraryA(data);
        if (hModule != NULL)
        {
            FreeLibrary(hModule);
            printLine("Library loaded and freed successfully");
        }
        else
        {
            printLine("Unable to load library");
        }
    }
}

}
#endif 
