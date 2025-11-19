#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE762_Mismatched_Memory_Management_Routines__delete_array_char_calloc_82.h"

namespace CWE762_Mismatched_Memory_Management_Routines__delete_array_char_calloc_82
{

void CWE762_Mismatched_Memory_Management_Routines__delete_array_char_calloc_82_bad::action(char * data)
{
    if (data != NULL) {
        /* FIX: Free memory correctly */
        free(data);
    }
}

}
#endif