#ifndef OMITBAD

#include <stdlib.h>
#include <stdio.h>

namespace CWE415_Double_Free__malloc_free_char_81
{

void CWE415_Double_Free__malloc_free_char_81_bad::action(char * data) const
{
    free(data);
}

}
#endif