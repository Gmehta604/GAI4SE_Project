#include "std_testcase.h"

namespace CWE457_Use_of_Uninitialized_Variable__no_constructor_01
{

#ifndef OMITBAD

class BadClass 
{
    public:
        int intOne;        

        BadClass() {
            intOne = 0;
        }
};

void bad()
{
    BadClass * badClassObject = new BadClass;
    printIntLine(badClassObject->intOne);
}

#endif 

} 

#ifdef INCLUDEMAIN

using namespace CWE457_Use_of_Uninitialized_Variable__no_constructor_01; 

int main(int argc, char * argv[])
{
    srand( (unsigned)time(NULL) );
#ifndef OMITBAD
    printLine("Calling bad()...");
    bad();
    printLine("Finished bad()");
#endif 
    return 0;
}

#endif