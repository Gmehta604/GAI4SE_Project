#ifndef OMITBAD

#include <stdio.h>
#include <stdlib.h>

namespace CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle__fopen_82
{

void CWE773_Missing_Reference_to_Active_File_Descriptor_or_Handle__fopen_82_bad::action(FILE *& data)
{
    
    data = fopen("BadSink_fopen.txt", "w+");
    
    if (data != NULL)
    {
        fclose(data);
    }
}

}
#endif