#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE36_Absolute_Path_Traversal__char_connect_socket_fopen_81.h"

#ifdef _WIN32
#define FOPEN fopen
#else
#define FOPEN fopen
#endif

namespace CWE36_Absolute_Path_Traversal__char_connect_socket_fopen_81
{

void CWE36_Absolute_Path_Traversal__char_connect_socket_fopen_81_bad::action(char * data) const
{
    {
        FILE *pFile = NULL;
        pFile = FOPEN(data, "wb+");
        if (pFile != NULL)
        {
            fclose(pFile);
        }
    }
}

}
#endif