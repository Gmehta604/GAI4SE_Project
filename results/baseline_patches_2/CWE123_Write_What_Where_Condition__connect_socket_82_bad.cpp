#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE123_Write_What_Where_Condition__connect_socket_82.h"

namespace CWE123_Write_What_Where_Condition__connect_socket_82
{

void CWE123_Write_What_Where_Condition__connect_socket_82_bad::action(badStruct data)
{
    linkedListPrev = data.list.prev;
    linkedListNext = data.list.next;
    linkedListPrev->next = linkedListNext;
    linkedListNext->prev = linkedListPrev;
}

}
#endif