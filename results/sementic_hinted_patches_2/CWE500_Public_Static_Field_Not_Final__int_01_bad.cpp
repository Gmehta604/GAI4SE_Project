#include "std_testcase.h"

using namespace std;

namespace CWE500_Public_Static_Field_Not_Final__int_01
{

#ifndef OMITBAD

class BadClass 
{
    public:
        
        static const int ONE_HUNDRED;
};
    

const int BadClass::ONE_HUNDRED = 100;

void bad()
{
    printIntLine(BadClass::ONE_HUNDRED);
}

#endif

}