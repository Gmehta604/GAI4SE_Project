#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle__fopen_82.h"

namespace CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle__fopen_82
{

void CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle__fopen_82_bad::action(FILE * data)
{
    
    FILE *fp;
    fp = fopen("BadSink_fopen.txt", "w+");
    if (fp == NULL)
    {
        return;
    }
    
    fclose(fp);
}

}
#endif