#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE843_Type_Confusion__char_82.h"

namespace CWE843_Type_Confusion__char_82
{

void CWE843_Type_Confusion__char_82_bad::action(void * data)
{
    if (typeid(data) == typeid(int)) {
        printIntLine(*((int*)data));
    } else {
        printCharLine(*((char*)data));
    }
}

}
#endif