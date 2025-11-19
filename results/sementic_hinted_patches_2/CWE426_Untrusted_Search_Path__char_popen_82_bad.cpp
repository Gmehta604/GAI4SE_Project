#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE426_Untrusted_Search_Path__char_popen_82.h"

#ifdef _WIN32
#define POPEN _popen
#define PCLOSE _pclose
#else 
#define POPEN popen
#define PCLOSE pclose
#endif

namespace CWE426_Untrusted_Search_Path__char_popen_82
{

void CWE426_Untrusted_Search_Path__char_popen_82_bad::action(char * data)
{
    {
        FILE *pipe;
        pipe = POPEN("sh", "wb");
        if (pipe != NULL)
        {
            PCLOSE(pipe);
        }
    }
}

}
#endif