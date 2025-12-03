#include <iostream>

namespace CWE500_Public_Static_Field_Not_Final__int_01 {

#ifndef OMITBAD

class BadClass {
public:
    static const int ONE_HUNDRED;
};

const int BadClass::ONE_HUNDRED = 100;

void bad() {
    std::cout << BadClass::ONE_HUNDRED << std::endl;
}

#endif

} // namespace CWE500_Public_Static_Field_Not_Final__int_01

#ifdef INCLUDEMAIN

int main(int argc, char *argv[]) {
    srand((unsigned)time(NULL));
#ifndef OMITBAD
    printLine("Calling bad()...");
    bad();
    printLine("Finished bad()");
#endif
    return 0;
}

#endif