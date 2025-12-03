

#include "std_testcase.h"

namespace CWE563_Unused_Variable__unused_class_member_value_01
{

#ifndef OMITBAD

class BadClass
{
    public:
        BadClass()
        {
            id = 22;
        }
        
        void printMembers() 
        {
            printIntLine(id);
        }
        
    private:
        int id; 
};

void bad()
{
    BadClass badClassObject;
    badClassObject.printMembers();
}

#endif

} 
   
#ifdef INCLUDEMAIN

using namespace CWE563_Unused_Variable__unused_class_member_value_01; 

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
