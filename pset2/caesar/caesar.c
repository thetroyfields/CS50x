#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        return 1;
    }
    int key = 0;
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (isdigit(argv[1][i]))
        {
            key = atoi(argv[1]);
        }
        else
        {
            printf("usage: ./caesar key\n");
        }
    }
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isalpha(plaintext[i]) && isupper(plaintext[i]))
        {
            char c = (((((char)plaintext[i] - 'A') + key) % 26) + 'A');
            printf("%c", c);
        }
        else if (isalpha(plaintext[i]) && islower(plaintext[i]))
        {
            char c = (((((char)plaintext[i] - 'a') + key) % 26) + 'a');
            printf("%c", c);
        }
        else
        {
            char c = (char)plaintext[i];
            printf("%c", c);
        }
    }
    printf("\n");
}

