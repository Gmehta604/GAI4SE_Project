#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE36_Absolute_Path_Traversal__char_connect_socket_fopen_82.h"

#ifdef _WIN32
#define FOPEN fopen
#else
#define FOPEN fopen
#endif

namespace CWE36_Absolute_Path_Traversal__char_connect_socket_fopen_82
{

void CWE36_Absolute_Path_Traversal__char_connect_socket_fopen_82_bad::action(char * data)
{
    {
        FILE *pFile = NULL;
        /* POTENTIAL FLAW: Possibly opening a file without validating the file name or path */
        pFile = FOPEN(data, "wb+");
        if (pFile != NULL)
        {
            fclose(pFile);
        }
    }
}

}
#endif