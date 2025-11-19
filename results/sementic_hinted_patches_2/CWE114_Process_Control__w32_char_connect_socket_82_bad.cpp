#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE114_Process_Control__w32_char_connect_socket_82.h"

#include <windows.h>

namespace CWE114_Process_Control__w32_char_connect_socket_82
{

void CWE114_Process_Control__w32_char_connect_socket_82_bad::action(char * data)
{
    {
        HMODULE hModule;
        size_t len = strlen(data);
        if (len > MAX_PATH)
        {
            return;
        }
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