static char SccsId[] = "@(#)chord.c	3.6\t Mar. 1995";
static char copyright[] = "Copyright 1991-1995 by Martin Leclerc & Mario Dorion";

#include "chord.h"

struct toc_struct *so_toc = NULL;
struct toc_struct *cur_toc_entry;

extern char title1;
extern int v_pages;
extern int pagination;
extern float scale;
extern int number_all;
extern int song_pages;
extern int text_size;
extern int vpos;
extern float top, bottom, l_margin, width;

struct toc_struct *toc_ptr;
struct sub_title_struct **sub_ptr_handle;

/* --------------------------------------------------------------------------------*/
void print_toc_entry (toc_ptr)
struct toc_struct *toc_ptr;
{
struct sub_title_struct *sub_ptr;
fprintf (stderr, "+++\n");
if ( toc_ptr != NULL )
	{
	fprintf (stderr, "*%s\n %d\n", toc_ptr->title, toc_ptr->page_label);
	sub_ptr = toc_ptr->sub_titles;

	while (sub_ptr != NULL)
		{
		fprintf(stderr, "%s\n", sub_ptr->sub_title);
		sub_ptr = sub_ptr->next_sub;
		}
	}
else
	fprintf (stderr, "Pointer is NULL\n");
fprintf (stderr, "---\n");
}
/* --------------------------------------------------------------------------------*/
void print_toc_entries()
{
struct toc_struct *dummy;

dummy=so_toc;
while (dummy != NULL )
	{
	print_toc_entry (dummy);
	dummy=dummy->next;
	}
}
/* --------------------------------------------------------------------------------*/
void add_title_to_toc (title, page_label)
char *title;
int page_label;
{
       struct toc_struct **prev_ptr_handle, *new_toc_entry;
static struct toc_struct dummy_toc;

debug ("start of add_title_to_toc");

new_toc_entry = (struct toc_struct *)malloc (sizeof (dummy_toc));
new_toc_entry->page_label=page_label;
new_toc_entry->title = malloc (strlen (title)+1);
new_toc_entry->sub_titles = NULL;
sub_ptr_handle = &new_toc_entry->sub_titles;
strcpy (new_toc_entry->title, title);

toc_ptr = so_toc;
prev_ptr_handle = &so_toc;

while (  ( toc_ptr != NULL) && (strcmp (title, toc_ptr->title) >= 0 ))
	{
	prev_ptr_handle = &(toc_ptr->next);
	toc_ptr=toc_ptr->next;
	}

new_toc_entry->next = toc_ptr;
*prev_ptr_handle = new_toc_entry;
cur_toc_entry = new_toc_entry;

}

/* --------------------------------------------------------------------------------*/
void add_subtitle_to_toc (sub_title)
char *sub_title;
{

static struct sub_title_struct dummy_sub_title_struct;
       struct sub_title_struct *new_sub = NULL;
       char *tmp_string;

debug ("start of add_subtitle_to_toc");

new_sub = (struct sub_title_struct *)malloc (sizeof (dummy_sub_title_struct));
tmp_string = (char *)malloc (strlen (sub_title) + 1);
new_sub->sub_title = tmp_string;
new_sub->next_sub = NULL;
strcpy (new_sub->sub_title, sub_title);
*sub_ptr_handle = new_sub;
sub_ptr_handle = &(new_sub->next_sub);
new_sub = NULL;
}
/* --------------------------------------------------------------------------------*/
void build_ps_toc()
	{
	char line[MAXTOKEN];
	struct toc_struct *toc_ptr;
	struct sub_title_struct *sub_ptr;

	debug("Debut de build_ps_toc");
	/* print_toc_entries(); */

	strcpy (&title1, "Index");

	if (v_pages % pagination)
		do_end_of_page(TRUE);
				
	if (pagination == 4) 
		{
		pagination = 1;
		scale = 1.0;
		}

	v_pages=0;
	do_start_of_page();
	number_all= FALSE;
	song_pages= 0;
	set_text_font (text_size+10);
	use_text_font();
	printf ("(");
	ps_puts (&title1);
	printf (") dup stringwidth pop 2 div\n");
	printf ("%f 2 div exch sub %d moveto\n", width, vpos);
	printf ("show\n");
	advance(text_size);

	toc_ptr = so_toc;

	while (toc_ptr != NULL)
		{

		/* title */
		if ( vpos < bottom + 3 * text_size)
			{
			advance (vpos);
			song_pages= 0;
			}
		advance(text_size+8);
		set_text_font(text_size + 5);
		use_text_font();
		printf("72 %d moveto\n", vpos);
		printf("(");
		debug ("Setting title\n");
		ps_puts(toc_ptr->title);
		printf(") show\n");
		printf("500 %d moveto\n", vpos);
		debug ("Setting page_label\n");
		printf("(%d) show\n", toc_ptr->page_label);

		/* sub titles */
		sub_ptr=toc_ptr->sub_titles;

		while (sub_ptr != NULL)
			{
			advance(text_size);
			set_text_font(text_size);
			use_text_font();
			printf ("108 %d moveto\n", vpos);
			printf("(");
			ps_puts(sub_ptr->sub_title);
			printf(") show\n");
			sub_ptr = sub_ptr->next_sub;
			}
		toc_ptr= toc_ptr->next;
		}

	vpos = vpos - text_size - 5;
	set_text_font (text_size);
	}

/* --------------------------------------------------------------------------------*/
