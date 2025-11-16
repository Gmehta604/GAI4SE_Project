#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE415_Double_Free__malloc_free_char_81.h"

namespace CWE415_Double_Free__malloc_free_char_81
{

void CWE415_Double_Free__malloc_free_char_81_bad::action(char * data) const
{
    free(data);
}

}
#endif 
