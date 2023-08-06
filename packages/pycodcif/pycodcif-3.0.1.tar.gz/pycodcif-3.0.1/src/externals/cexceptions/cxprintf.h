/*---------------------------------------------------------------------------*\
**$Author: saulius $
**$Date: 2011-03-08 20:45:40 +0200 (An, 08 kov. 2011) $ 
**$Revision: 1590 $
**$URL: svn+ssh://www.crystallography.net/home/coder/svn-repositories/cod-tools/tags/v3.0.1/src/externals/cexceptions/cxprintf.h $
\*---------------------------------------------------------------------------*/

#ifndef __CEX_REPORT_H
#define __CEX_REPORT_H

#include <stdarg.h>

const char* cxprintf( const char * format, ... );
const char* vcxprintf( const char * format, va_list args );

#endif
