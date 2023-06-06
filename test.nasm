%include "io.asm"
section	.bss
sinput:	resb	255	;reserve a 255 byte space in memory for the users input string
v$a:	resd	1
section	.text
global _start
_start:
	push	9		
	push	8		
	pop	ebx				 ; dÚpile la seconde operande dans ebx
	pop	eax				 ; dÚpile la permiÞre operande dans eax
	imul	ebx				 ; effectue l'opÚration eax*ebx et met le rÚsultat dans eax
	push	eax				 ; empile le rÚsultat
	pop	eax		
	call	iprintLF		
	mov	eax,	1			 ; 1 est le code de SYS_EXIT
	mov	ebx,	0			 ; 0 Úquivalent Ó exit(0)
	int	0x80				 ; exit