static char SccsId[] = "@(#)a2crd.c	3.6\t Mar. 1995";
static char copyright[] = "Copyright 1991-1995 by Martin Leclerc & Mario Dorion";

#include <stdio.h>
#include "chord.h"


FILE
	*source_fd;

int
	p_put,
	lchord,
	ltext,
	lbuf,
	c,
	debug_mode = 0,
	dirty_chord=0,
	dirty_text=0,
	in_header,
	in_title=0,
	in_subtitle=0,
	n_lines,
	in_chorus=0;

char
	chord_line[MAXLINE],
	text_line[MAXLINE],
	buf[MAXLINE],
	*command_name,
	source[MAXTOKEN],
	*current_file,
	mesgbuf[MAXLINE],
	*mesg;

float
	spaces=0,
	not_space=0;

double 
	ratio=1.0;

extern char *optarg;
extern int optind, opterr;

/* --------------------------------------------------------------------------------*/
void print_2lines(chord_line, text_line)
char chord_line[], text_line[];

{
int i, mini=0, max=0;
int p_out=0;

max = (ltext > lchord) ? ltext : lchord;

sprintf (mesg, "   print_2lines text_line=[%s]", text_line); debug(mesg);
sprintf (mesg, "   print_2lines chord_line=[%s]", chord_line); debug(mesg);


for (i = 0; i < max ; i++)
	{
	if ( (i <= lchord) && ( chord_line[i] != ' ' )
		&& (chord_line[i] != '\0') && ( i >= mini ) )
		{
		printf ("[");
		for (mini=i; (chord_line[mini] != ' ') && (mini<lchord); mini++)
			{
			printf("%c", chord_line[mini]);
			p_out++;
			}
		printf ("]");
		p_out += 2;
		}
	if (i < ltext)
		{
		printf ("%c", text_line[i]);
		p_out++;
		}
	}

printf("\n");
p_out=0;


ltext=0;
dirty_text=0;
for (i=0;i<MAXLINE;i++)
	text_line[i]='\0';

lchord=0;
dirty_chord=0;
for (i=0;i<MAXLINE;i++)
	chord_line[i]='\0';
}

/* --------------------------------------------------------------------------------*/
void do_help (command)
char *command;
        {
        fprintf (stderr, "Usage: %s [options] file\n", command);
        fprintf (stderr, "Options:\n");
        fprintf (stderr, "      -D                 : Debug mode\n");
	exit(0);
        }
 
/* --------------------------------------------------------------------------------*/
void do_sig()
	{
	char sig_file[MAXTOKEN];
	FILE *sig_fd;

	strcpy (sig_file, getenv ("HOME"));
	strcat (sig_file,"/.a2crdsig\0");

	sig_fd = fopen (sig_file, "r");
	if (sig_fd != NULL)
		{
		while ((c=getc(sig_fd)) != EOF)
			printf("%c", c);
		fclose(sig_fd);
		}
	}

/* --------------------------------------------------------------------------------*/
void process_file(source_fd)
FILE *source_fd;
{

int i;

do_sig();

debug ("start of process_file");
n_lines=0;
lbuf=0;

while ((c=getc(source_fd)) != EOF)
	{

	switch (c)
		{
	
		case '\n':
	
		n_lines++;
		buf[lbuf]='\0';

		/* Handle exceptions */
		if ( n_lines == 1)
			{
			if (! strncmp(text_line, "From ", 5))
				in_header = TRUE;
			else    in_title  = TRUE;
			}

		if ( in_header && lbuf == 0)
			in_header = FALSE;

		if (in_header )
			printf ("# %s\n", text_line);

		else if (not_space != 0)
			{
sprintf (mesg, "   space=%d not_space=%d", (int)spaces,(int)not_space); debug(mesg);
	
			if ( ((spaces / not_space) > ratio) || ((spaces==0) && (lbuf<3)) )

			/* this must be a chord line */
				{
sprintf (mesg, "chord is \"%s\"",buf); debug(mesg);
	
				if (dirty_chord)
					{
					print_2lines (chord_line, text_line);
					}
	
				strcpy (chord_line, buf);
				lchord=lbuf;
				dirty_chord++;
				in_title=0; in_subtitle=0;
				}
			else
			/* so it is a text line ! */
				{
	
sprintf (mesg, "text is \"%s\"",buf); debug(mesg);
	
				if (dirty_text)
					{
					print_2lines (chord_line, text_line);
					}
	

				if (in_title)
					{
					printf("{title:%s}\n", buf);
					in_title=FALSE;
					in_subtitle=TRUE;
					}
				else
					if (in_subtitle)
						{
						printf("{subtitle:%s}\n", buf);
						}
					else 
						{
						strcpy(text_line, buf);
						ltext=lbuf;
						dirty_text++;
						}
	
				}
						
			lbuf=0;
			spaces=0;
			not_space=0;
			}
		else
			{
			if (dirty_chord || dirty_text)
				print_2lines(chord_line, text_line);
			printf ("\n");
			if (in_chorus)
				{
				printf("{end_of_chorus}\n");
				in_chorus=0;
				}
			in_subtitle=FALSE;
			in_title=FALSE;
			}

		for (i=0;i<MAXLINE;i++)
			buf[i]='\0';
		break;
	
		case '{':
			if (lbuf == 0)
			/* directive */
				{
				debug("got a directive");
				if (dirty_chord || dirty_text)
					{
					debug("FLUSHING");
					print_2lines(chord_line, text_line);
					}
				buf[0]='{';
				for (lbuf=1; (c=getc(source_fd)) != '\n'; lbuf++)
					buf[lbuf]=c;
				strcpy(text_line, buf);
				ltext=lbuf;
				print_2lines(chord_line, text_line);
				lbuf=0;
				}
			break;

		case '#':
			if (lbuf == 0)
			/* comment */
				{
				debug("got a comment");
				if (dirty_chord || dirty_text)
					{
					debug("FLUSHING");
					print_2lines(chord_line, text_line);
					}
				buf[0]='#';
				for (lbuf=1; (c=getc(source_fd)) != '\n'; lbuf++)
					buf[lbuf]=c;
				strcpy(text_line, buf);
				ltext=lbuf;
				print_2lines(chord_line, text_line);
				lbuf=0;
				}
			break;

		case '\t':
			for (i=0; (i<8) && (lbuf % 8 != 0); i++)
				buf[lbuf++] = ' ';
			spaces += 8;
			break;
			
	
		case '|':
		case ' ':
			spaces++;
			buf[lbuf++] = ' ';
			break;
	
		default:
			not_space++;
			buf[lbuf++] = c;
			break;
		}
	}
if (dirty_chord || dirty_text)
	print_2lines(chord_line, text_line);
chord_line[0]='\0';
text_line[0]='\0';
buf[0]='\0';
}
/* --------------------------------------------------------------------------------*/

void main (argc, argv)
int argc;
char **argv;

{
double f;

command_name=argv[0];
mesg=&mesgbuf[0];

while (( c = getopt(argc, argv, "Dr:o:")) != -1)
	switch (c) {

	case 'D':
		debug_mode++;
		break;
	
	case 'r':
		f=atof(optarg);
			if (f ==0)
				error ("Invalid value for ratio");
			else
				ratio=f;
			break;

	case 'o':
		if ( freopen(optarg, "w", stdout) == NULL)
			{
			fprintf (stderr, "Unable to open \"%s\" for output\n", optarg);
			exit(1);
			}
		break;
		
	
	case '?':
		do_help (argv[0]);
		break;
	}
	

        if (optind  == argc)
                {
                debug ("Reading stdin");
                strcpy(source, "stdin");
                process_file (stdin);
                }
        else
                {
                for ( ; optind < argc; optind++ )
                        {
			sprintf (mesg, "Ready to process file \"%s\"\n", argv[optind]);
                        debug (mesg);

                        strcpy(source, argv[optind]);

			sprintf (mesg, "Calling read_input_file on \"%s\"\n", source);
                        debug (mesg);

                        read_input_file(source, source_fd);
                        }
                }


}
