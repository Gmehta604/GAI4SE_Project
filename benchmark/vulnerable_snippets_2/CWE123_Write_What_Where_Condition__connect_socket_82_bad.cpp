/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE123_Write_What_Where_Condition__connect_socket_82_bad.cpp
Label Definition File: CWE123_Write_What_Where_Condition.label.xml
Template File: sources-sink-82_bad.tmpl.cpp
*/
/*
 * @description
 * CWE: 123 Write-What-Where Condition
 * BadSource: connect_socket Overwrite linked list pointers using a connect socket (client side)
 * GoodSource: Don't overwrite linked list pointers
 * Sinks:
 *    BadSink : Remove element from list
 * Flow Variant: 82 Data flow: data passed in a parameter to an virtual method called via a pointer
 *
 * */
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
#endif /* OMITBAD */
