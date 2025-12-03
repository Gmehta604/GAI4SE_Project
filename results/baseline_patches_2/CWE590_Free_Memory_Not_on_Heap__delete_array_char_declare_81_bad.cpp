#ifndef OMITBAD

#include <iostream>
#include <new>

namespace CWE590_Free_Memory_Not_on_Heap__delete_array_char_declare_81
{

void CWE590_Free_Memory_Not_on_Heap__delete_array_char_declare_81_bad::action(char * data) const
{
    std::cout << data << std::endl;
    
    // FIX: Free memory on the heap using delete []
    delete [] data;
}

}
#endif