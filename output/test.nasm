%include	"io.asm"
section	.bss
sinput:	resb	255	;reserve a 255 byte space in memory for the users input string
v$a:	resd	1
section	.text
global _start
_start:
	push	ebp				 ; réserve espace pour variable
	mov	ebp,	esp			 ; réserve espace pour variable
	sub	esp,	0			 ; réserve espace pour variable
type instruction inconnu <class 'arbre_abstrait.Function'>
