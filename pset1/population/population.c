#include <cs50.h>
#include <stdio.h>

int main(void)
{
   //get data from user
   int starting_population;
   do
   {
       starting_population = get_int("starting Population: ");
   }
   while (starting_population < 9);


   int ending_population;
   do
   {
       ending_population = get_int("Ending Population: ");
   }
   while (ending_population < starting_population);

   //solve for how many years
   int years = 0;
   while (starting_population < ending_population)
   {
      starting_population = starting_population + (starting_population / 3) - (starting_population / 4);
      years++;
   }
   printf("Years: %i", years);
}