#ifndef OMITBAD

#include <assert.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

namespace CWE617_Reachable_Assertion__connect_socket_81
{

void CWE617_Reachable_Assertion__connect_socket_81_bad::action(int data) const
{
    if (data > ASSERT_VALUE)
    {
        assert(data > ASSERT_VALUE);
    }
}

}
#endif