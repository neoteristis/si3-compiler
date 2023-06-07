%include        "io.asm"
section .bss
sinput: resb    255     ;reserve a 255 byte space in memory for the users input string
v$a:    resd    1
section .text
global _start
_start:
        push    ebp                              ; réserve espace pour variable
        mov     ebp,    esp                      ; réserve espace pour variable
        sub     esp,    8                        ; réserve espace pour variable
        push    5
        pop     eax
        mov     [ebp-4],        eax
        push    9
        pop     eax
        mov     [ebp-8],        eax
        mov     eax,    [ebp-4]
        push    eax
        mov     eax,    [ebp-8]
        push    eax
        pop     ebx                              ; dépile la seconde operande dans ebx
        pop     eax                              ; dépile la permière operande dans eax
        imul    ebx                              ; effectue l'opération eax * ebx et met le résultat dans eax
        push    eax                              ; empile le résultat
        pop     eax
        call    iprintLF
        mov     eax,    1                        ; 1 est le code de SYS_EXIT
        mov     ebx,    0                        ; 0 équivalent à exit(0)
        int     0x80                             ; exit