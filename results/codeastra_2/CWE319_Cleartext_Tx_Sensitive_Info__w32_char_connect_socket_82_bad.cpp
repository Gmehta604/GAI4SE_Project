To fix the vulnerability, you should replace the `connect_socket` function with a secure communication protocol such as SSL/TLS or SSH. Here's an example using SSL/TLS:
```c
#include <openssl/ssl.h>

// ...

SSL_CTX* ctx = SSL_CTX_new(TLS_client_method());
SSL* ssl = SSL_new(ctx);

// Connect to the server
if (SSL_connect(ssl) == 1)
{
    // Send the password over the secure connection
    SSL_write(ssl, password, strlen(password));

    // Receive the response from the server
    char buffer[1024];
    SSL_read(ssl, buffer, sizeof(buffer));

    // Print the response
    printf("%s\n", buffer);

    // Close the connection
    SSL_shutdown(ssl);
    SSL_free(ssl);
    SSL_CTX_free(ctx);
}
else
{
    printf("Error connecting to the server.\n");
}
```
Note that this is just an example and you will need to modify it to fit your specific use case. Also, make sure to include the necessary headers and libraries for OpenSSL.