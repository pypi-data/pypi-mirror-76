/*---------------------------------------------------------------------------*\
**$Author: saulius $
**$Date: 2015-04-05 12:26:36 +0300 (Sk, 05 bal. 2015) $ 
**$Revision: 3216 $
**$URL: svn+ssh://www.crystallography.net/home/coder/svn-repositories/cod-tools/tags/v3.0.1/src/externals/cexceptions/stringx.c $
\*---------------------------------------------------------------------------*/

/* exports: */
#include <stringx.h>

/* uses: */
#include <string.h>
#include <allocx.h>

#define merror( EX ) cexception_raise_in( EX, allocx_subsystem, \
					  ALLOCX_NO_MEMORY,     \
					  "Not enough memory" )

char *strdupx( const char *str, cexception_t *ex )
{
    void *s = strdup( str );
    if( !s ) merror( ex );
    return s;
}
