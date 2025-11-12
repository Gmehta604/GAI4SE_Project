/* TEMPLATE GENERATED TESTCASE FILE
Filename: CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_84_goodG2B.cpp
Label Definition File: CWE121_Stack_Based_Buffer_Overflow__CWE129.label.xml
Template File: sources-sinks-84_goodG2B.tmpl.cpp
*/
/*
 * @description
 * CWE: 121 Stack Based Buffer Overflow
 * BadSource: fscanf Read data from the console using fscanf()
 * GoodSource: Larger than zero but less than 10
 * Sinks:
 *    GoodSink: Ensure the array index is valid
 *    BadSink : Improperly check the array index by not checking the upper bound
 * Flow Variant: 84 Data flow: data passed to class constructor and destructor by declaring the class object on the heap and deleting it after use
 *
 * */
#ifndef OMITGOOD

#include "std_testcase.h"
#include "CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_84.h"

namespace CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_84
{
CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_84_goodG2B::CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_84_goodG2B(int dataCopy)
{
    data = dataCopy;
    /* POTENTIAL FLAW: Read data from the console using fscanf() */
    fscanf(stdin, "%d", &data);
}

CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_84_goodG2B::~CWE121_Stack_Based_Buffer_Overflow__CWE129_fscanf_84_goodG2B