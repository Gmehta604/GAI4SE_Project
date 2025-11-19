#ifndef OMITBAD

#include <iostream>
#include <memory>

namespace CWE590_Free_Memory_Not_on_Heap__delete_array_char_alloca_81
{

void CWE590_Free_Memory_Not_on_Heap__delete_array_char_alloca_81_bad::action(char * data) const
{
    std::unique_ptr<char[]> heapData = std::make_unique<char[]>(strlen(data) + 1);
    strcpy(heapData.get(), data);
    printLine(heapData.get());
}

}
#endif