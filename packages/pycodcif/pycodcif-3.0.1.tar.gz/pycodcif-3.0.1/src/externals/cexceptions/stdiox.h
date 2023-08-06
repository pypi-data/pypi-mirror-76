/*---------------------------------------------------------------------------*\
** $Author: andrius $
** $Date: 2019-12-27 15:30:51 +0200 (Pn, 27 gruod. 2019) $ 
** $Revision: 7629 $
** $URL: svn+ssh://www.crystallography.net/home/coder/svn-repositories/cod-tools/tags/v3.0.1/src/externals/cexceptions/stdiox.h $
\*---------------------------------------------------------------------------*/

#ifndef _STDIOX_H
#define _STDIOX_H

#include <stdio.h>
#include <cexceptions.h>

extern void *stdiox_subsystem;

typedef enum {
  STDIOX_OK = 0,
  STDIOX_FILE_OPEN_ERROR,
  STDIOX_FILE_CLOSE_ERROR,
  STDIOX_FILE_MEMOPEN_ERROR,

  STDIOX_ERROR_last
} STDIOX_ERROR;

FILE *fopenx( const char *filename, const char *mode, cexception_t *ex );
void fclosex( FILE *file, cexception_t *ex );
FILE *fmemopenx( void *buf, size_t size, const char *mode, cexception_t *ex );

#endif
