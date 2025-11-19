#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE78_OS_Command_Injection__char_connect_socket_execl_82.h"

#ifdef _WIN32
#include <process.h>
#define EXECL _execl
#else 
#define EXECL execl
#endif

namespace CWE78_OS_Command_Injection__char_connect_socket_execl_82
{

void CWE78_OS_Command_Injection__char_connect_socket_execl_82_bad::action(char * data)
{
    
    EXECL(COMMAND_INT_PATH, COMMAND_INT_PATH, COMMAND_ARG1, COMMAND_ARG3, (char *)NULL);
}

}
#endif