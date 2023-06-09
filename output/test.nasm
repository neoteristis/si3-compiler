%include        "io.asm"
section .bss
sinput: resb    255     ;reserve a 255 byte space in memory for the users input string
v$a:    resd    1
section .text
global _start
_start:
        push    ebp                              ; réserve espace pour variable
        mov     ebp,    esp                      ; réserve espace pour variable
        sub     esp,    4                        ; réserve espace pour variable
        push    0
        pop     eax
        mov     [ebp-4],        eax
        push    9
        pop     eax
        call    iprintLF
        pop     eax
        cmp     eax,    0
        jne     e1
        jmp     e0
        e1:
        mov     eax,    0
        e0:
        push    eax
        mov     eax,    1                        ; 1 est le code de SYS_EXIT
        mov     ebx,    0                        ; 0 équivalent à exit(0)
        int     0x80                             ; exit