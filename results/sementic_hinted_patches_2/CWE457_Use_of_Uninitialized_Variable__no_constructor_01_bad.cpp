#include "std_testcase.h"

namespace CWE457_Use_of_Uninitialized_Variable__no_constructor_01
{

#ifndef OMITBAD

class BadClass 
{
    public:
        int intOne = 0;        
};

void bad()
{
    BadClass * badClassObject = new BadClass;
    printIntLine(badClassObject->intOne);
}

#endif 

}