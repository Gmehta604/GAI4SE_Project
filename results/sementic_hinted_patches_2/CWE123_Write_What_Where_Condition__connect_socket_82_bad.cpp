#ifndef OMITBAD

#include "std_testcase.h"
#include "CWE123_Write_What_Where_Condition__connect_socket_82.h"

namespace CWE123_Write_What_Where_Condition__connect_socket_82
{

void CWE123_Write_What_Where_Condition__connect_socket_82_bad::action(badStruct data)
{
    linkedListPrev = data.list.prev;
    linkedListNext = data.list.next;
    if (linkedListNext->prev != linkedListPrev) {
        linkedListNext->prev = linkedListPrev;
        linkedListPrev->next = linkedListNext;
    }
}

}
#endif