#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE590_Free_Memory_Not_on_Heap__delete_array_char_declare_81.h"

namespace CWE590_Free_Memory_Not_on_Heap__delete_array_char_declare_81
{

void CWE590_Free_Memory_Not_on_Heap__delete_array_char_declare_81_bad::action(char * data) const
{
    printLine(data);
    
    delete [] data;
}

}
#endif 
