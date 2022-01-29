#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // get height of pyramid //
    int height;
    do
    {
        height = get_int("pyramid height: ");
    }

    while (height < 1 || height > 8);

    // print out pyramid //
    for (int rows = 1; rows <= height; rows++)
    {
        for (int align = height - rows; align >= 1 ; align--)

        {
            printf(" ");
        }

        for (int columns = 1; columns <= rows; columns++)

        {
            printf("#");
        }

        printf("\n");
    }
}
