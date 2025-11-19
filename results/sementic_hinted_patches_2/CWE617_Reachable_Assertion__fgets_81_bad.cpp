#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE617_Reachable_Assertion__fgets_81.h"

namespace CWE617_Reachable_Assertion__fgets_81
{

void CWE617_Reachable_Assertion__fgets_81_bad::action(int data) const
{
    
    if (data <= ASSERT_VALUE) {
        // Handle error
        return;
    }

    assert(data > ASSERT_VALUE);
}

}
#endif