#include "utils.h"



void parse_csv(char *path, char *sep, int num_cols, output _lines){

  FILE *fp;
  char *lines = NULL;
  char *line[num_cols];
  size_t len = 0;
  int col;
  char *tok;

  fp = fopen(path, "r");

  if (fp == NULL)
      exit(EXIT_FAILURE);
  while ((getline(&lines, &len, fp)) != -1) {
        col=0;
        while ((tok = strsep(&lines, sep))){
            line[col] =  tok;
            col++;
        }
        WRITE(_lines, &line);

  }
   free(lines);
   fclose(fp);

}

//void write_csv(char *path, char *sep, output _lines, int num_cols, int num_rows){
//
//  FILE *fp;
//  char *lines = NULL;
//  char *line[num_cols];
//  size_t len = 0;
//  int col;
//  char *tok;
//
//
//  fp = fopen(path, "w+");
//  for (int i=0;i<m;++i)
//    for(int )
//  if (fp == NULL)
//      exit(EXIT_FAILURE);
//  while ((getline(&lines, &len, fp)) != -1) {
//        col=0;
//        while ((tok = strsep(&lines, sep))){
//            line[col] =  tok;
//            col++;
//        }
//        WRITE(_lines, &line);
//
//  }
//   free(lines);
//   fclose(fp);
//   FREE_OUTPUT_QUEUE(_lines);
//
//}

complex float cast_complex(char *value) {
  char *tok;
  char *plus=malloc(sizeof(char) * strlen(value));
  strcpy(plus,value);

  float real;
  float imag;
  tok = strsep(&value, "+");
  if (strlen(tok) != strlen(plus)){
    real = atof(tok);
    imag = atof(strsep(&value, "+"));
    return (real + imag*I);
  }

  char *minus=malloc(sizeof(char) * strlen(plus));
  strcpy(minus,plus);
  tok = strsep(&plus, "-");

  if (strlen(tok) != strlen(minus)){
    real = atof(tok);
    imag = atof(strsep(&plus, "-"));
    return (real - imag*I);
  }
  return (atof(tok) + 0*I);

}

char* stringToBinary(char* s) {
    if(s == NULL) return 0; /* no input string */
    size_t len = strlen(s);
    char *binary = malloc(len*8 + 1); // each char is one byte (8 bits) and + 1 at the end for null terminator
    binary[0] = '\0';
    for(size_t i = 0; i < len; ++i) {
        char ch = s[i];
        for(int j = 7; j >= 0; --j){
            if(ch & (1 << j)) {
                strcat(binary,"1");
            } else {
                strcat(binary,"0");
            }
        }
    }
    return binary;
}
