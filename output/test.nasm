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
f:
	push	ebp				 ; réserve espace pour variable
	mov	ebp,	esp			 ; réserve espace pour variable
	sub	esp,	0			 ; réserve espace pour variable
	push	3		
	mov	esp,	ebp			 ; dépile les variables locales
	pop	ebp				 ; dépile le pointeur de pile de la fonction appelante
	ret					 ; retourne à la fonction appelante
	pop	eax		
	call	iprintLF		
	mov	eax,	1			 ; 1 est le code de SYS_EXIT
	mov	ebx,	0			 ; 0 équivalent à exit(0)
	int	0x80				 ; exit
