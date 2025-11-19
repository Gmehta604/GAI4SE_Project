#ifndef OMITBAD

#include <iostream>
#include <memory>

namespace CWE762_Mismatched_Memory_Management_Routines__delete_array_char_calloc_82
{

void CWE762_Mismatched_Memory_Management_Routines__delete_array_char_calloc_82_bad::action(char * data)
{
    std::unique_ptr<char[]> dataPtr = std::make_unique<char[]>(strlen(data));
    strcpy(dataPtr.get(), data);
    delete [] dataPtr;
}

}
#endif