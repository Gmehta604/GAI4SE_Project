#ifndef OMITBAD

#include <stdio.h>
#include <string.h>
#include <unistd.h>

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
        char *args[] = {"/bin/sh", "-c", "ls -la", NULL};
        pipe = POPEN(args[0], "wb");
        if (pipe != NULL)
        {
            PCLOSE(pipe);
        }
    }
}

}
#endif