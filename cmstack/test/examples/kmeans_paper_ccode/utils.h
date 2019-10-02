#define _GNU_SOURCE
#include "pipe.h"
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <complex.h>

// Define values
#define THREADS 4
#define STRINGSIZE 1024

// Type definitions for pipes
typedef pipe_t* flow;
typedef pipe_producer_t* output;
typedef pipe_consumer_t* input;
typedef char string[STRINGSIZE];
typedef char* str;
// typedef char * string;

// Macros for queues
#define component void
#define OUTPUT_QUEUE(x) pipe_producer_new(x)
#define INPUT_QUEUE(x) pipe_consumer_new(x)
#define QUEUE(x) pipe_new(x, 0)

#define WRITE(x,data) pipe_push(x, data, 1)
#define READ(x,data) pipe_pop(x, data, 1)

#define FREE_OUTPUT_QUEUE(x) pipe_producer_free(x)
#define FREE_INPUT_QUEUE(x) pipe_consumer_free(x)
#define FREE_QUEUE(x) pipe_free(x)

// Macros for casting strings to datatypes
#define INT_CAST(x) atoi(x)
#define FLOAT_CAST(x) atof(x)
#define BOOL_CAST(x) ((bool) atoi(x) != 0)
#define COMPLEX_CAST(x) (cast_complex(x))
#define BINARY_CAST(x) (cast_binary(x))

//Macros for reading and writing
#define FREAD(path, sep, lineq, cols) parse_csv(path, sep, lineq, cols)
#define FWRITE(path, sep, lineq, cols, rows) parse_csv(path, sep, lineq, cols, rows)

// Utility function signatures
void parse_csv(char *, char *, int, output);
//void write_csv(char *, char *, output, int, int);
complex float cast_complex(char *);

char* cast_binary(char* s);

