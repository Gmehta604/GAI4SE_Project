#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE672_Operation_on_Resource_After_Expiration_or_Release__list_int_82.h"

namespace CWE672_Operation_on_Resource_After_Expiration_or_Release__list_int_82
{

void CWE672_Operation_on_Resource_After_Expiration_or_Release__list_int_82_bad::action(list<int>  data)
{
    {
        list<int> ::iterator i;
        cout << "The list contains: ";
        for( i = data.begin(); i != data.end(); i++)
        {
            if (!*i)
            {
                data.clear();
            }
            
            cout << " " << *i;
        }
        cout << endl;
    }
}

}
#endif 
