#ifndef OMITBAD

#include <iostream>
#include <memory>

namespace CWE762_Mismatched_Memory_Management_Routines__delete_array_char_calloc_81
{

void CWE762_Mismatched_Memory_Management_Routines__delete_array_char_calloc_81_bad::action(char * data) const
{
    std::unique_ptr<char[]> dataPtr = std::make_unique<char[]>(strlen(data));
    strcpy(dataPtr.get(), data);
    delete [] dataPtr.release();
}

}
#endif