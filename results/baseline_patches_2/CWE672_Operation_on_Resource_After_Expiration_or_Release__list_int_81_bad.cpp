#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE672_Operation_on_Resource_After_Expiration_or_Release__list_int_81.h"

namespace CWE672_Operation_on_Resource_After_Expiration_or_Release__list_int_81
{

void CWE672_Operation_on_Resource_After_Expiration_or_Release__list_int_81_bad::action(const list<int>& data) const
{
    {
        list<int>::const_iterator i;
        cout << "The list contains: ";
        for (i = data.begin(); i != data.end(); i++)
        {
            if (!*i)
            {
                break;
            }
            
            cout << " " << *i;
        }
        cout << endl;
    }
}

}
#endif