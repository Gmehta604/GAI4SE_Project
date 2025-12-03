#include "std_testcase.h"
#include "CWE321_Hard_Coded_Cryptographic_Key__w32_char_82.h"

#include <windows.h>
#include <wincrypt.h>


#pragma comment (lib, "Advapi32")

namespace CWE321_Hard_Coded_Cryptographic_Key__w32_char_82
{

void CWE321_Hard_Coded_Cryptographic_Key__w32_char_82_goodG2B::action(char * cryptoKey)
{
    {
        HCRYPTPROV hCryptProv;
        HCRYPTKEY hKey;
        HCRYPTHASH hHash;
        char toBeEncrypted[] = "String to be encrypted";
        DWORD encryptedLen = strlen(toBeEncrypted)*sizeof(char);
        BYTE encrypted[200];    
        memcpy(encrypted, toBeEncrypted, encryptedLen);
        if(!CryptAcquireContext(&hCryptProv, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, 0))
        {
            if(!CryptAcquireContext(&hCryptProv, NULL, MS_ENHANCED_PROV, PROV_RSA_AES, CRYPT_NEWKEYSET))
            {
                printLine("Error in acquiring cryptographic context");
                exit(1);
            }
        }
       
        if(!CryptCreateHash(hCryptProv, CALG_SHA_256, 0, 0, &hHash))
        {
            printLine("Error in creating hash");
            exit(1);
        }
        
        if(!CryptHashData(hHash, (BYTE *) cryptoKey, strlen(cryptoKey)*sizeof(char), 0))
        {
            printLine("Error in hashing cryptoKey");
            exit(1);
        }
        
        if(!CryptDer