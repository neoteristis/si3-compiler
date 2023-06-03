import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait
import borrow_checker
import inspect

DEBUG=False

def print_debug(msg):
    if DEBUG:
        print(msg)


class FloParser(Parser):
	debugfile = 'parser.out'
	# On récupère la liste des lexèmes de l'analyse lexicale
	tokens = FloLexer.tokens 
	start="prog"

	def __init__(self):
		pass

	@_('statement_list')
	def prog(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Programme(p[0])

	@_('IDENTIFIANT')
	def primary_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Variable(p.IDENTIFIANT)

	@_('BOOLEAN')
	def primary_expression(self,p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Boolean(p.BOOLEAN)

	@_('ENTIER')
	def primary_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Entier(p.ENTIER)

	@_("'(' expression ')'")
	def primary_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.expression

	@_('primary_expression')
	def postfix_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.primary_expression

	@_('function_call')
	def postfix_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.function_call

	@_('postfix_expression')
	def unary_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.postfix_expression

	@_('unary_operator cast_expression')
	def unary_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation(p[0].op,p[0].hidden,p[1])

	@_("'-'")
	def unary_operator(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.UnaryOperator("*",arbre_abstrait.Entier(-1))

	@_('unary_expression')
	def cast_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.unary_expression

	@_('cast_expression')
	def multiplicative_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.cast_expression

	@_("multiplicative_expression '*' cast_expression")
	def multiplicative_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("*", p.multiplicative_expression, p.cast_expression)

	@_("multiplicative_expression '/' cast_expression")
	def multiplicative_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("/", p.multiplicative_expression, p.cast_expression)

	@_("multiplicative_expression '%' cast_expression")
	def multiplicative_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("%", p.multiplicative_expression, p.cast_expression)

	@_("multiplicative_expression")
	def additive_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.multiplicative_expression

	@_("additive_expression '+' multiplicative_expression")
	def additive_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("+", p.additive_expression, p.multiplicative_expression)

	@_("additive_expression '-' multiplicative_expression")
	def additive_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("+", p.additive_expression, p.multiplicative_expression)

	@_("additive_expression")
	def relational_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.additive_expression

	@_("relational_expression '<' additive_expression")
	def relational_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("<", p.relational_expression, p.additive_expression)

	@_("relational_expression '>' additive_expression")
	def relational_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation(">", p.relational_expression, p.additive_expression)

	@_("relational_expression INFERIEUR_OU_EGAL additive_expression")
	def relational_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("<=", p.relational_expression, p.additive_expression)

	@_("relational_expression SUPERIEUR_OU_EGAL additive_expression")
	def relational_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation(">=", p.relational_expression, p.additive_expression)

	@_("relational_expression")
	def equality_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.relational_expression

	@_("equality_expression EQUAL relational_expression")
	def equality_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("==", p.equality_expression, p.relational_expression)

	@_("equality_expression DIFFERENT relational_expression")
	def equality_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("!=", p.equality_expression, p.relational_expression)

	@_("equality_expression")
	def logical_and_expression(self,p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.equality_expression

	@_("logical_and_expression ET equality_expression")
	def logical_and_expression(self,p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("and", p.logical_and_expression, p.equality_expression)

	@_("logical_and_expression")
	def logical_or_expression(self,p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.logical_and_expression

	@_("logical_or_expression OU logical_and_expression")
	def logical_or_expression(self,p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("or", p.logical_or_expression, p.logical_and_expression)

	@_("logical_or_expression")
	def logical_not_expression(self,p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.logical_or_expression

	@_("NON logical_or_expression")
	def logical_not_expression(self,p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("not", arbre_abstrait.NoneOperation(), p.logical_or_expression)

	@_("logical_or_expression NON logical_or_expression")
	def logical_not_expression(self,p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation("not", p[0], p[1])

	@_("logical_not_expression")
	def conditional_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.logical_not_expression

	@_("primary_expression assignment_operator conditional_expression")
	def assignment_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Operation(p[1].op,p[0],p[2])

	@_("conditional_expression")
	def assignment_expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.conditional_expression

	@_("AFFECT")
	def assignment_operator(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.UnaryOperator("=")

	@_("assignment_expression")
	def expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.assignment_expression

	@_("expression ',' assignment_expression")
	def expression(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Entier(0)

	@_('jump_statement')
	def statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.jump_statement

	@_('compound_statement')
	def statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.compound_statement

	@_('expression_statement')
	def statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.expression_statement

	@_('selection_statement')
	def statement(self, p):
		return p.selection_statement

	@_('iteration_statement')
	def statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.iteration_statement

	@_('declaration_statement')
	def statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.declaration_statement

	@_('function_declaration_statement')
	def statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.function_declaration_statement

	@_("'{' '}'")
	def compound_statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.NoneOperation()

	@_("'{' statement_list '}'")
	def compound_statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.statement_list

	@_("declaration ';'")
	def declaration_statement(self, p):
		return p.declaration

	@_("type IDENTIFIANT")
	def declaration(self, p):
		return arbre_abstrait.DeclareOperation(p.type,p.IDENTIFIANT)

	@_("type IDENTIFIANT AFFECT additive_expression")
	def declaration(self, p):
		return arbre_abstrait.DeclareOperation(p.type,p.IDENTIFIANT,p.additive_expression)

	@_("type IDENTIFIANT '(' ')' compound_statement")
	def function_declaration_statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Function(p.IDENTIFIANT,p.type,arbre_abstrait.ListeDeclarations(),p.compound_statement)

	@_("type IDENTIFIANT '(' arguments_list_opt ')' compound_statement")
	def function_declaration_statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.Function(p.IDENTIFIANT,p.type,p.arguments_list_opt,p.compound_statement)

	@_("IDENTIFIANT '(' ')'")
	def function_call(self , p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.FunctionOperation(p.IDENTIFIANT, arbre_abstrait.ListeParameters())

	@_("IDENTIFIANT '(' parameters_list_opt ')'")
	def function_call(self , p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.FunctionOperation(p.IDENTIFIANT, p.parameters_list_opt)

	@_("INT")
	def type(self, p):
		return "entier"

	@_("BOOL")
	def type(self, p):
		return "booleen"

	@_("declarations_list")
	def arguments_list_opt(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.declarations_list

	@_("declaration")
	def declarations_list(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		l = arbre_abstrait.ListeDeclarations()
		l.declarations.append(p[0])
		return l

	@_("declarations_list SEPARATOR declaration")
	def declarations_list(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		p[0].declarations.append(p.declaration)
		return p[0]

	@_("parameters_list")
	def parameters_list_opt(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.parameters_list

	@_("assignment_expression")
	def parameters_list(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		l = arbre_abstrait.ListeParameters()
		l.parameters.append(p[0])
		return l

	@_("parameters_list SEPARATOR assignment_expression")
	def parameters_list(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		p[0].parameters.append(p.assignment_expression)
		return p[0]

	@_("statement")
	def statement_list(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		l = arbre_abstrait.ListeInstructions()
		l.instructions.append(p[0])
		return l

	@_("statement_list statement")
	def statement_list(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		p[0].instructions.append(p[1])
		return p[0]

	@_("';'")
	def expression_statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.NoneOperation()

	@_("expression ';'")
	def expression_statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return p.expression

	@_("SI '(' expression ')' statement")
	def selection_statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.ConditionalOperation(p.expression, p.statement)

	@_("SI '(' expression ')' statement SINON statement")
	def selection_statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.ConditionalOperation(p.expression, p.statement0, p.statement1)

	@_("TANTQUE '(' expression ')' statement")
	def iteration_statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.LoopOperation(p.expression, p.statement)

	@_("RETOURNER ';'")
	def jump_statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.ReturnOperation(arbre_abstrait.NoneOperation())

	@_("RETOURNER expression ';'")
	def jump_statement(self, p):
		print_debug(inspect.stack()[0][3]+":"+str(inspect.stack()[0][2]))
		return arbre_abstrait.ReturnOperation(p.expression)

if __name__ == '__main__':
	lexer = FloLexer()
	parser = FloParser()
	if len(sys.argv) < 2:
		print("usage: python3 analyse_syntaxique.py NOM_FICHIER_SOURCE.flo")
	else:
		verbose=True
		if len(sys.argv)>2:
			if sys.argv[2]=="-v":
				verbose=False
		with open(sys.argv[1], "r") as f:
			data = f.read()
			try:
				arbre = parser.parse(lexer.tokenize(data))
				if arbre == None:
					if verbose:
						print("There are some errors")
					exit(1)
				else:
					borrowChecher=borrow_checker.BorrowChecker(arbre)
					if borrowChecher.check():
						if verbose:
							arbre.afficher()
						exit(0)
					else:
						if verbose:
							arbre.afficher()
							print("Error detected !")
						exit(1)
			except EOFError:
			    exit()
