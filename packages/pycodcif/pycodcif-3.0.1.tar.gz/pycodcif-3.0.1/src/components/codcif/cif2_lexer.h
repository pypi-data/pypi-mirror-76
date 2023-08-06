/*---------------------------------------------------------------------------*\
**$Author: antanas $
**$Date: 2020-07-20 16:43:00 +0300 (Pr, 20 liep. 2020) $ 
**$Revision: 8230 $
**$URL: svn+ssh://www.crystallography.net/home/coder/svn-repositories/cod-tools/tags/v3.0.1/src/components/codcif/cif2_lexer.h $
\*---------------------------------------------------------------------------*/

#ifndef __CIF2_LEXER_H
#define __CIF2_LEXER_H

#include <stdio.h>
#include <unistd.h> /* for ssize_t */
#include <cif_compiler.h>

int cif2lex( void );
void cif2restart( void );

void cif2_lexer_set_compiler( CIF_COMPILER *ccc );

int cif2_lexer_set_report_long_tags( int flag );
int cif2_lexer_report_long_tags( void );
size_t cif2_lexer_set_tag_length_limit( size_t max_length );

extern int cif2error( const char *message );

#endif
