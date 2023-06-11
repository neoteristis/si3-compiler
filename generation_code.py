import sys

import arbre_abstrait
import borrow_checker
from analyse_lexicale import FloLexer
from analyse_syntaxique import FloParser

num_etiquette_courante = -1  # Permet de donner des noms différents à toutes les étiquettes (en les appelant e0, e1,e2,...)

afficher_table = False
afficher_nasm = False

delay_stack=[]


def getContextVar(symbolTable, function, name):
    variables = symbolTable[function].variables
    for variable in variables:
        if variable[0] == name:
            return variable
    return None


def gen_ebp_stack(symbolTable, function, name):
    variable = getContextVar(symbolTable, function, name)
    index = (int(variable[2]) * 4) + 4
    return "[ebp-" + str(index) + "]"

def delay_execute(function, arguments):
    delay_stack.append([function, arguments])
    
def execute_stack():
    for stack in delay_stack:
        stack[0](*stack[1])

"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""


def printifm(*args, **kwargs):
    if afficher_nasm:
        print(*args, **kwargs)


"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""


def printift(*args, **kwargs):
    if afficher_table:
        print(*args, **kwargs)


"""
Fonction locale, permet d'afficher un commentaire dans le code nasm.
"""


def nasm_comment(comment):
    if comment != "":
        printifm(
            "\t\t ; " + comment)  # le point virgule indique le début d'un commentaire en nasm. Les tabulations sont là pour faire jolie.
    else:
        printifm("")


"""
Affiche une instruction nasm sur une ligne
Par convention, les derniers opérandes sont nuls si l'opération a moins de 3 arguments.
"""


def nasm_instruction(opcode, op1="", op2="", op3="", comment=""):
    if op2 == "":
        printifm("\t" + opcode + "\t" + op1 + "\t\t", end="")
    elif op3 == "":
        printifm("\t" + opcode + "\t" + op1 + ",\t" + op2 + "\t", end="")
    else:
        printifm("\t" + opcode + "\t" + op1 + ",\t" + op2 + ",\t" + op3, end="")
    nasm_comment(comment)


"""
Retourne le nom d'une nouvelle étiquette
"""


def nasm_nouvelle_etiquette():
    global num_etiquette_courante
    num_etiquette_courante += 1
    return "e" + str(num_etiquette_courante)


"""
Affiche le code nasm correspondant à tout un programme
"""


def gen_programme(programme, symbolTable):
    printifm('%include\t"io.asm"')
    printifm('section\t.bss')
    printifm('sinput:	resb	255	;reserve a 255 byte space in memory for the users input string')
    printifm('v$a:	resd	1')
    printifm('section\t.text')
    printifm('global _start')
    printifm('_start:')
    gen_memory("main", symbolTable)
    gen_listeInstructions("main", programme.listeInstructions, symbolTable)
    nasm_instruction("mov", "eax", "1", "", "1 est le code de SYS_EXIT")
    nasm_instruction("mov", "ebx", "0", "", "0 équivalent à exit(0)")
    nasm_instruction("int", "0x80", "", "", "exit")
    execute_stack()


def gen_memory(function, symbolTable):
    variables = symbolTable[function].variables
    nasm_instruction("push", "ebp", "", "", "réserve espace pour variable")
    nasm_instruction("mov", "ebp", "esp", "", "réserve espace pour variable")
    nasm_instruction("sub", "esp", str(len(variables) * 4), "", "réserve espace pour variable")


"""
Affiche le code nasm correspondant à une suite d'instructions
"""


def gen_listeInstructions(function, listeInstructions, symbolTable):
    for instruction in listeInstructions.instructions:
        gen_instruction(function, instruction, symbolTable)


"""
Affiche le code nasm pour gérer les conditions
"""

def gen_condition(symbolTable, function, instruction: arbre_abstrait.ConditionalOperation):
    etiquette_if = nasm_nouvelle_etiquette()
    etiquette_else = nasm_nouvelle_etiquette()
    etiquette_fin = nasm_nouvelle_etiquette()

    gen_expression(symbolTable,function,instruction.expr)

    nasm_instruction("pop", "eax")
    nasm_instruction("cmp", "eax", "0")
    nasm_instruction("je", etiquette_else)

    nasm_instruction("jmp", etiquette_if)

    nasm_instruction("mov", "eax", "0")

    nasm_instruction(etiquette_if + ":")
    gen_expression(symbolTable, function, instruction.statement)
    nasm_instruction("push", "eax")
    nasm_instruction("jmp", etiquette_fin)

    nasm_instruction(etiquette_else + ":")
    if isinstance(instruction.statement2, arbre_abstrait.ListeInstructions):
        gen_expression(symbolTable, function, instruction.statement2)

    nasm_instruction(etiquette_fin + ":")


"""
Affiche le code nasm correspondant à une boucle TANT QUE
"""


def gen_boucle(symbolTable, function, instruction: arbre_abstrait.LoopOperation):
    etiquette_debut = nasm_nouvelle_etiquette()
    etiquette_fin = nasm_nouvelle_etiquette()

    nasm_instruction(etiquette_debut + ":")
    gen_expression(symbolTable, function, instruction.expr)
    nasm_instruction("pop", "eax")
    nasm_instruction("cmp", "eax", "0")
    nasm_instruction("je", etiquette_fin)

    if isinstance(instruction.statement, arbre_abstrait.ListeInstructions):
        gen_expression(symbolTable, function, instruction.statement)

    nasm_instruction("jmp", etiquette_debut)
    nasm_instruction(etiquette_fin + ":")
    nasm_instruction("mov", "eax", "0")
    nasm_instruction("push", "eax")


# ====================================================================================================
# THIS IS CURRENTLY NOT WORKING AND IN PROGRESS
# ====================================================================================================

"""
Affiche le code nasm correspondant à une fonction
"""


def gen_fonction(symbolTable, instruction: arbre_abstrait.Function):
    # Entête de la fonction
    nasm_instruction("_"+instruction.name + ":")
    # Génération du code pour les instructions de la fonction
    gen_listeInstructions(instruction.name, instruction.instructions, symbolTable)


"""
Affiche le code nasm pour gérer les opérations de retour
"""


def gen_return(symbolTable, function, instruction: arbre_abstrait.ReturnOperation):
    gen_expression(symbolTable, function, instruction.expr)
    nasm_instruction("pop", "eax", "", "", "")
    nasm_instruction("ret", "", "", "", "")


"""
Affiche le code nasm correspondant à une function operation
"""


def gen_functionOperation(symbolTable, function, instruction: arbre_abstrait.FunctionOperation):
    if instruction.name == "ecrire":
        gen_ecrire(symbolTable, function, instruction)
    elif instruction.name == "lire":
        gen_lire(symbolTable, function)
    else:
        variables = symbolTable[instruction.name].variables
        nasm_instruction("push","ebp","","","")
        nasm_instruction("mov","esi","esp","","")
        for param in instruction.listeParameters.parameters:
            gen_expression(symbolTable, function, param)
            nasm_instruction("push","eax","","","")
        nasm_instruction("mov","ebp","esi","","")
        nasm_instruction("sub","esp" , str(len(variables) * 4), "", "")
        nasm_instruction("call", "_"+instruction.name, "", "", "")
        nasm_instruction("add", "esp" , str(len(variables) * 4),"","")
        nasm_instruction("pop","ebp", "","","")
        nasm_instruction("push" ,"eax","","","")


# ====================================================================================================

"""
Affiche le code nasm correspondant à une instruction
"""


def gen_instruction(function, instruction, symbolTable):
    if type(instruction) == arbre_abstrait.FunctionOperation:
        if instruction.name == "ecrire":
            gen_ecrire(symbolTable, function, arbre_abstrait.Ecrire(instruction.listeParameters.parameters[0]))
        if instruction.name == "lire":
            gen_lire(symbolTable, function)
    elif type(instruction) == arbre_abstrait.DeclareOperation:
        gen_declaration(function, instruction, symbolTable)
    elif type(instruction) == arbre_abstrait.Operation:
        gen_operation(symbolTable, function, instruction)
    elif type(instruction) == arbre_abstrait.ConditionalOperation:
        gen_condition(symbolTable, function, instruction)
    elif type(instruction) == arbre_abstrait.ListeInstructions:
        gen_listeInstructions(function, instruction, symbolTable)
    elif type(instruction) == arbre_abstrait.LoopOperation:
        gen_boucle(symbolTable, function, instruction)
    # CURRENTLY NOT WORKING
    elif type(instruction) == arbre_abstrait.Function:
        delay_execute(gen_fonction, [symbolTable,instruction])
    elif type(instruction) == arbre_abstrait.ReturnOperation:
        gen_return(symbolTable, function, instruction)
    elif type(instruction) == arbre_abstrait.FunctionOperation:
        gen_functionOperation(symbolTable, function, instruction)
    # ====================================================================================================
    else:
        print("type instruction inconnu", type(instruction))
        exit(0)


def gen_declaration(function, instruction, symbolTable):
    if type(instruction.expr) == arbre_abstrait.NoneOperation:
        return
    gen_expression(symbolTable, function, instruction.expr)
    nasm_instruction("pop", "eax", "", "", "")
    nasm_instruction("mov", gen_ebp_stack(symbolTable, function, instruction.name), "eax")


"""
Affiche le code nasm correspondant au fait d'envoyer la valeur entière d'une expression sur la sortie standard
"""


def gen_ecrire(symbolTable, function, ecrire):
    gen_expression(symbolTable, function, ecrire.exp)  # on calcule et empile la valeur d'expression
    nasm_instruction("pop", "eax", "", "", "")  # on dépile la valeur d'expression sur eax
    nasm_instruction("call", "iprintLF", "", "", "")  # on envoie la valeur d'eax sur la sortie standard
    
def gen_lire(symbolTable, function):
    nasm_instruction("call", "readline", "","","")
    nasm_instruction("push", "eax", "", "", "")


"""
Affiche le code nasm pour calculer et empiler la valeur d'une expression
"""


def gen_expression(symbolTable, function, expression):
    if type(expression) == arbre_abstrait.Operation:
        gen_operation(symbolTable, function, expression)  # on calcule et empile la valeur de l'opération
    elif type(expression) == arbre_abstrait.Entier:
        nasm_instruction("push", str(expression.valeur), "", "", "");  # on met sur la pile la valeur entière
    elif type(expression) == arbre_abstrait.Boolean:
        if expression.valeur == True:
            nasm_instruction("push", str(1), "", "", "");  # on met sur la pile la valeur entière
        else:
            nasm_instruction("push", str(0), "", "", "");  # on met sur la pile la valeur entière
    elif type(expression) == arbre_abstrait.Variable:
        nasm_instruction("mov", "eax", gen_ebp_stack(symbolTable, function, expression.name), "", "")
        nasm_instruction("push", "eax", "", "", "")
    elif type(expression) == arbre_abstrait.NoneOperation:
        nasm_instruction("push", "0", "", "", "")
    elif type(expression) == arbre_abstrait.ConditionalOperation:
        gen_condition(symbolTable, function, expression)
    elif type(expression) == arbre_abstrait.ListeInstructions:
        gen_listeInstructions(function, expression, symbolTable)
    # CURRENTLY NOT WORKING
    elif type(expression) == arbre_abstrait.LoopOperation:
        gen_boucle(symbolTable, function, expression)
    elif type(expression) == arbre_abstrait.FunctionOperation:
        gen_functionOperation(symbolTable, function, expression)
    # ====================================================================================================
    else:
        print("type d'expression inconnu", type(expression))
        exit(0)


"""
Affiche le code nasm pour calculer l'opération et la mettre en haut de la pile
"""


def gen_operation(symbolTable, function, operation):
    op = operation.op

    if op == "=":
        gen_expression(symbolTable, function, operation.exp2)
        nasm_instruction("pop", "eax", "", "", "")
        nasm_instruction("mov", gen_ebp_stack(symbolTable, function, operation.exp1.name), "eax", "", "")
        return

    gen_expression(symbolTable, function, operation.exp1)  # on calcule et empile la valeur de exp1
    gen_expression(symbolTable, function, operation.exp2)  # on calcule et empile la valeur de exp2

    nasm_instruction("pop", "ebx", "", "", "dépile la seconde operande dans ebx")
    nasm_instruction("pop", "eax", "", "", "dépile la permière operande dans eax")

    code = {"+": "add", 
            "-": "sub", 
            "*": "imul", 
            "/": "idiv", 
            "%": "idiv",
            "et": "and", 
            "ou": "or",
            "non": "not",
            ">=": "jge",  # saut si inférieur ou égal
        	"<=": "jle",  # saut si supérieur ou égal
        	"<": "jl",  # saut si inférieur
        	">": "jg",  # saut si supérieur
			"==" :"je",
        	"!=": "jne"  # saut si différent
    }
    # Un dictionnaire qui associe à chaque opérateur sa fonction nasm

    # Voir: https://www.bencode.net/blob/nasmcheatsheet.pdf
    if op in ['+', "-"]:
        nasm_instruction(code[op], "eax", "ebx", "",
                         "effectue l'opération eax " + op + " ebx et met le résultat dans eax")
        nasm_instruction("push", "eax", "", "", "empile le résultat")
    elif op in ['*', "/"]:
        nasm_instruction("mov", "edx", "0", "", "")
        nasm_instruction(code[op], "ebx", "", "", "effectue l'opération eax " + op + " ebx et met le résultat dans eax")
        nasm_instruction("push", "eax", "", "", "empile le résultat")
    elif op in ["et", "ou"]:
        nasm_instruction(code[op], "eax", "ebx", "",
                         "effectue l'opération eax " + op + " ebx et met le résultat dans eax")
        nasm_instruction("push", "eax", "", "", "empile le résultat")
    elif op == "non":
        nasm_instruction("xor", "ebx", "1", "", "")
        nasm_instruction("mov", "eax","ebx","","")
        nasm_instruction("push", "eax", "", "", "empile le résultat")
    elif op == "%":
        nasm_instruction("mov", "edx", "0", "", "")
        nasm_instruction(code[op], "ebx", "", "", "effectue l'opération eax " + op + " ebx et met le résultat dans eax")
        nasm_instruction("mov", "eax", "edx", "", "")
        nasm_instruction("push", "eax", "", "", "empile le résultat")
    elif op in ['>', '<', '>=', '<=', '==', '!=']:
        true_label = nasm_nouvelle_etiquette()  # Étiquette pour le cas où la condition est vraie
        end_label = nasm_nouvelle_etiquette()  # Étiquette pour la fin de la comparaison

        nasm_instruction("cmp", "eax", "ebx", "", "compare eax et ebx")

        # Effectuer le saut en fonction de l'opérateur de comparaison
        nasm_instruction(code[op], true_label, "", "", "saut si la condition est vraie")
        nasm_instruction("push", "0", "", "", "empile 0 (faux)")
        nasm_instruction("jmp", end_label, "", "", "saut à la fin de la comparaison")
        nasm_instruction(true_label + ":", "", "", "", "étiquette pour le cas où la condition est vraie")
        nasm_instruction("push", "1", "", "", "empile 1 (vrai)")
        nasm_instruction(end_label + ":", "", "", "", "étiquette pour la fin de la comparaison")

if __name__ == "__main__":
    afficher_nasm = True
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 3 or sys.argv[1] not in ["-nasm", "-table"]:
        print("usage: python3 generation_code.py -nasm|-table NOM_FICHIER_SOURCE.flo")
        exit(0)
    if sys.argv[1] == "-nasm":
        afficher_nasm = True
    else:
        afficher_tableSymboles = True
    verbose = True
    with open(sys.argv[2], "r") as f:
        data = f.read()
        try:
            arbre = parser.parse(lexer.tokenize(data))
            if arbre == None or parser.errorFlag:
                if verbose:
                    print("There are some errors")
                    exit(1)
            else:
                borrowChecher = borrow_checker.BorrowChecker(arbre)
                if borrowChecher.check():
                    if verbose:
                        pass
                    #arbre.afficher()
                    gen_programme(arbre, borrowChecher.symbolTable)
                    exit(0)
                else:
                    if verbose:
                        print("Error detected !")
                    exit(1)
        except EOFError:
            exit()
