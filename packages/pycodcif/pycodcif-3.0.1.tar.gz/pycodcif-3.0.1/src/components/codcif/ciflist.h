/*-------------------------------------------------------------------------*\
* $Author: antanas $
* $Date: 2019-11-15 20:06:25 +0200 (Pn, 15 lapkr. 2019) $ 
* $Revision: 7424 $
* $URL: svn+ssh://www.crystallography.net/home/coder/svn-repositories/cod-tools/tags/v3.0.1/src/components/codcif/ciflist.h $
\*-------------------------------------------------------------------------*/

#ifndef __CIFLIST_H
#define __CIFLIST_H

#include <stdio.h>
#include <cexceptions.h>

typedef struct CIFLIST CIFLIST;

#include <cifvalue.h>

CIFLIST *new_list( cexception_t *ex );
void delete_list( CIFLIST *list );
void list_dump( CIFLIST *list );

void list_push( CIFLIST *list, CIFVALUE *value, cexception_t *ex );
void list_unshift( CIFLIST *list, CIFVALUE *value, cexception_t *ex );

size_t list_length( CIFLIST *list );
CIFVALUE *list_get( CIFLIST *list, int index );
CIFVALUE **list_get_values( CIFLIST *list );

int list_contains_list_or_table( CIFLIST *list );
char *list_concat( CIFLIST *list, char separator, cexception_t *ex );

#endif
