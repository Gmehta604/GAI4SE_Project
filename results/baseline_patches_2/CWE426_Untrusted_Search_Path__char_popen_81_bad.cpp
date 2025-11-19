#ifndef OMITBAD

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#ifdef _WIN32
#define POPEN _popen
#define PCLOSE _pclose
#else 
#define POPEN popen
#define PCLOSE pclose
#endif

namespace CWE426_Untrusted_Search_Path__char_popen_81
{

void CWE426_Untrusted_Search_Path__char_popen_81_bad::action(char * data) const
{
    {
        FILE *pipe;
        char *cmd;
        cmd = "/bin/sh";
        pipe = POPEN(cmd, "wb");
        if (pipe != NULL)
        {
            PCLOSE(pipe);
        }
    }
}

}
#endif