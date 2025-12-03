#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE401_Memory_Leak__new_array_int_82.h"

namespace CWE401_Memory_Leak__new_array_int_82
{

void CWE401_Memory_Leak__new_array_int_82_bad::action(int * data)
{
    delete[] data;
}

}
#endif