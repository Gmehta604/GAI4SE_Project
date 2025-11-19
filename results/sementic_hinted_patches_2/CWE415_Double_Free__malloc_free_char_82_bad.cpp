#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE415_Double_Free__malloc_free_char_82.h"

namespace CWE415_Double_Free__malloc_free_char_82
{

void CWE415_Double_Free__malloc_free_char_82_bad::action(char * data)
{
    if (data != NULL)
    {
        free(data);
    }
}

}
#endif