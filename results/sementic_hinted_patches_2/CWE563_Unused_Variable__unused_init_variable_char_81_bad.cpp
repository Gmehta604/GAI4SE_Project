#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE563_Unused_Variable__unused_init_variable_char_81.h"

namespace CWE563_Unused_Variable__unused_init_variable_char_81
{

void CWE563_Unused_Variable__unused_init_variable_char_81_bad::action(char data) const
{
    char data = 'A'; // Initialize data
    
    ; 
}

}
#endif