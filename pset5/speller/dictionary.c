// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdint.h>

#include "dictionary.h"


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 80000;

// Hash table
node *table[N];

//global word count variable
int word_count = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int index = hash(word);
    
    for (node *n = table[index]; n != NULL; n = n->next)
    {
        if (strcasecmp(n->word, word) == 0)
        {
            return true;
        }    
    }
    
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;
    
    while ((c = tolower(*word++)))
    {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }
    
    return hash % N;
    //Dan, Bernstein (1991) comp.lang.c <source code>. https://theartincode.stanis.me/008-djb2/
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    //open dictionary and check address
    FILE *text = fopen(dictionary, "r");
    
    if (dictionary == NULL)
    {
        return false;
    }    

    char buffer[LENGTH + 1];
    word_count = 0;
    
    //create a new node and store the scanned word
    while (fscanf(text, "%s", buffer) != EOF)
    {    
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }
        
        strcpy(n->word, buffer);
        
        //insert node into the hash table
        int index = hash(buffer);
        
        n->next = table[index];
        table[index] = n;
        
        word_count++;
    }

    fclose(text);
    
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *n = table[i];
        
        while ((n != NULL))
        {  
            node *tmp = n;
            n = n->next;
            free(tmp);
        }
        
        if (n == NULL && i == N - 1)
        {    
            return true;
    
        }    
    }
    
    return false;
}


