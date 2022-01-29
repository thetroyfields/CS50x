#include "helpers.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            if (image[i][j].rgbtRed == image[i][j].rgbtBlue && image[i][j].rgbtBlue == image[i][j].rgbtGreen)   
            {
                    
            }
            else
            {
                int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
                image[i][j].rgbtBlue = average;
                image[i][j].rgbtGreen = average;
                image[i][j].rgbtRed = average;
            }
        }    
    }    
    return;
}
   
// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed;
    int sepiaBlue;
    int sepiaGreen;
    
    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
        {    
            sepiaRed = round(((image[i][j].rgbtRed * .393) + (image[i][j].rgbtGreen * .769) + (image[i][j].rgbtBlue * .189)));
            if (sepiaRed >= 255)
            {
                sepiaRed = 255;
            }  
            
            sepiaBlue = round(((image[i][j].rgbtRed * .272) + (image[i][j].rgbtGreen * .534) + (image[i][j].rgbtBlue * .131)));
            if (sepiaBlue >= 255)
            {
                sepiaBlue = 255;
            }  
            
            sepiaGreen = round(((image[i][j].rgbtRed * .349) + (image[i][j].rgbtGreen * .686) + (image[i][j].rgbtBlue * .168)));
            if (sepiaGreen >= 255)
            {
                sepiaGreen = 255;
            }
            
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
        }   

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    for (int i = 0; i < height; i++)
        for (int j = 0; j < width / 2; j++)
        {
            int opp = width - 1 - j;
            temp = image[i][j];
            image[i][j] = image[i][opp];
            image[i][opp] = temp;
        }
        
    return;
}

// Blur image
           
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE blur[height][width];
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sum_green = 0;
            int sum_blue = 0;
            int sum_red = 0;
            float count = 0.0;
            for (int row = -1; row < 2; row++)
            {
                if (i + row < 0 || i + row > height - 1)
                {
                    continue;
                }
                
                for (int column = -1; column < 2; column++)
                {
                    if (j + column < 0 || j + column > width - 1)
                    {
                        continue;
                    }
                    
                    sum_green += image[i + row][j + column].rgbtGreen;
                    sum_blue += image[i + row][j + column].rgbtBlue;
                    sum_red += image[i + row][j + column].rgbtRed;
                    count++;
                }    
            }
            blur[i][j].rgbtBlue = round(sum_blue / count);
            blur[i][j].rgbtGreen = round(sum_green / count);
            blur[i][j].rgbtRed = round(sum_red / count);
        }    
    }
    for (int i = 0; i < height; i++)
        for (int j = 0; j < width; j++)
        {
            image[i][j] = blur[i][j];
        }

}
