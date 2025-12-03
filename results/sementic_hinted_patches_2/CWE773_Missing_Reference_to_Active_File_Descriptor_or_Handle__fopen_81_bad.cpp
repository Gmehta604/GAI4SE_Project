#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle__fopen_81.h"

namespace CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle__fopen_81
{

void CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle__fopen_81_bad::action(FILE * data) const
{
    
    FILE *fp = fopen("BadSink_fopen.txt", "w+");
    if (fp != NULL)
    {
        fclose(fp);
    }
}

}
#endif