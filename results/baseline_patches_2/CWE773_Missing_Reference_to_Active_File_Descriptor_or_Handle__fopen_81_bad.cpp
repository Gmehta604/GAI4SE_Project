#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle__fopen_81.h"

namespace CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle__fopen_81
{

void CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle__fopen_81_bad::action(FILE *& data) const
{
    
    data = fopen("BadSink_fopen.txt", "w+");
    
    if (data != NULL)
    {
        fclose(data);
    }
}

}
#endif