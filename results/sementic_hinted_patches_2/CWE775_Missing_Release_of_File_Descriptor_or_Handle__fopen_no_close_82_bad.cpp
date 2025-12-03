#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE775_Missing_Release_of_File_Descriptor_or_Handle__fopen_no_close_82.h"

namespace CWE775_Missing_Release_of_File_Descriptor_or_Handle__fopen_no_close_82
{

void CWE775_Missing_Release_of_File_Descriptor_or_Handle__fopen_no_close_82_bad::action(FILE * data)
{
    fclose(data);
}

}
#endif