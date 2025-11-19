#ifndef OMITBAD

#include <iostream>
#include <string>

namespace CWE476_NULL_Pointer_Dereference__char_81
{

void CWE476_NULL_Pointer_Dereference__char_81_bad::action(const char * data) const
{
    if (data == nullptr)
    {
        std::cout << "Data is NULL" << std::endl;
    }
    else
    {
        std::cout << "Data is not NULL" << std::endl;
    }
}

}
#endif