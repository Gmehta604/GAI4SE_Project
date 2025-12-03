#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE762_Mismatched_Memory_Management_Routines__delete_array_char_calloc_81.h"

namespace CWE762_Mismatched_Memory_Management_Routines__delete_array_char_calloc_81
{

void CWE762_Mismatched_Memory_Management_Routines__delete_array_char_calloc_81_bad::action(char * data) const
{
    if (data != NULL) {
        /* FIX: Free memory using free() */
        free(data);
    }
}

}
#endif