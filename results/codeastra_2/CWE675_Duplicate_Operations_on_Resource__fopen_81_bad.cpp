#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE675_Duplicate_Operations_on_Resource__fopen_81.h"

namespace CWE675_Duplicate_Operations_on_Resource__fopen_81
{

void CWE675_Duplicate_Operations_on_Resource__fopen_81_bad::action(FILE * data) const
{
    if (data != NULL) {
        fclose(data);
    }
}

}
#endif 
```
The vulnerability was caused by calling `fclose` multiple times on the same file pointer, which can lead to unpredictable behavior or crashes. To fix this issue, we added a check to ensure that the file pointer is not null before closing it.