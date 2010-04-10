static char SccsId[] = "@(#)common.c	3.6\t Mar. 1995";
static char copyright[] = "Copyright 1991-1995 by Martin Leclerc & Mario Dorion";

#include <stdio.h>
#include "chord.h"

extern char *current_file;
extern char *command_name;
extern char *mesg;
extern int  in_chordrc;
extern int  first_time_in_chordrc;

/* --------------------------------------------------------------------------------*/
char *tolower_str(str)
char *str;
{
	static char	temp_str[MAXLINE];
	char	*ptr;

	strcpy(temp_str, str);
	ptr=temp_str;

	while (*ptr=(char) tolower((int) *ptr)) 
		ptr++;

	return(temp_str);
}

/* --------------------------------------------------------------------------------*/
char *toupper_str(str)
char *str;
{
	static char	temp_str[MAXLINE];
	char	*ptr;

	strcpy(temp_str, str);
	ptr=temp_str;

	while (*ptr=(char) toupper((int) *ptr)) 
		ptr++;

	return(temp_str);
}


/* --------------------------------------------------------------------------------*/
void error(err_str)
char *err_str;
{
	extern int n_lines;

       	 	fprintf(stderr, "WARNING: %s\n",err_str);
       		fprintf(stderr, "         in file \"%s\", line %d\n\n", current_file,n_lines+1);
}

/* --------------------------------------------------------------------------------*/
void error_rt(err_str)
char *err_str;
{
	extern int n_lines;
       	 	fprintf(stderr, "WARNING: %s defined as a run-time option\n\n",err_str);
}

/* --------------------------------------------------------------------------------*/
void debug(dbg_str)
char *dbg_str;
{
	extern int debug_mode;

        if ( debug_mode )
                fprintf (stderr, "Debug: %s\n", dbg_str);
}

/* --------------------------------------------------------------------------------*/
void print_version()
{

        char *version = VERSION;
        char *patch_level = PATCH_LEVEL;
        
        printf ("%s version %s, patchlevel %s\n", command_name, version, patch_level);
}

/* --------------------------------------------------------------------------------*/
/* read the file passed as argument */
void read_input_file(source, source_fd)
char source[];
FILE *source_fd;
        {
	sprintf (mesg , "start of read_input_file on [%s]", source);
	debug (mesg);
        current_file = source; 

        source_fd = fopen (source, "r");

        if (source_fd == NULL)
                {
                fprintf(stderr, "Unable to open \"%s\"\n", source);
                exit (1);
                }

        process_file(source_fd);
        fclose(source_fd);
        }

