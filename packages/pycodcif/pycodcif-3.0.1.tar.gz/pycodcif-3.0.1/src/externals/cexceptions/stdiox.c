/*---------------------------------------------------------------------------*\
** $Author: andrius $
** $Date: 2019-12-27 15:30:51 +0200 (Pn, 27 gruod. 2019) $
** $Revision: 7629 $
** $URL: svn+ssh://www.crystallography.net/home/coder/svn-repositories/cod-tools/tags/v3.0.1/src/externals/cexceptions/stdiox.c $
\*---------------------------------------------------------------------------*/

/* exports: */
#include <stdiox.h>

/* uses: */
#include <cexceptions.h>
#include <cxprintf.h>
#include <errno.h>
#include <string.h>

void *stdiox_subsystem = &stdiox_subsystem;

FILE *fopenx( const char *filename, const char *mode, cexception_t *ex )
{
    FILE *f = fopen( filename, mode );

    if( f == NULL ) {
        cexception_raise_syserror
            ( ex, stdiox_subsystem, STDIOX_FILE_OPEN_ERROR,
              "could not open file", strerror( errno ));
    }

    return f;
}

void fclosex( FILE *file, cexception_t *ex )
{
    if( fclose( file ) != 0 ) {
        cexception_raise_syserror
            ( ex, stdiox_subsystem, STDIOX_FILE_CLOSE_ERROR,
              "could not close file", strerror( errno ));
    }
}

FILE *fmemopenx( void *buf, size_t size, const char *mode, cexception_t *ex )
{
    FILE *f = fmemopen( buf, size, mode );

    if( f == NULL ) {
        cexception_raise_syserror
            ( ex, stdiox_subsystem, STDIOX_FILE_MEMOPEN_ERROR,
              "could not open file in memory", strerror( errno ));
    }

    return f;
}
