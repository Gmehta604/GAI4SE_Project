#ifndef OMITBAD

#include <string>

namespace CWE665_Improper_Initialization__char_cat_81
{

void CWE665_Improper_Initialization__char_cat_81_bad::action(char * data) const
{
    std::string source = "Hello";
    
    strcat(data, source.c_str());
    printLine(data);
}

}
#endif