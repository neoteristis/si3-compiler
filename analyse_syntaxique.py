import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait


class FloParser(Parser):
	debugfile = 'parser.out'
	# On récupère la liste des lexèmes de l'analyse lexicale
	tokens = FloLexer.tokens
	start="prog"

	def __init__(self):
		self.names = {}
  
	
	# Règles gramaticales et actions associées
	@_('listeInstructions')
	def prog(self, p):
		return arbre_abstrait.Programme(p[0])

	@_('instruction')
	def listeInstructions(self, p):
		l = arbre_abstrait.ListeInstructions()
		l.instructions.append(p[0])
		return l

	@_('instruction listeInstructions')
	def listeInstructions(self, p):
		p[1].instructions.append(p[0])
		return p[1]

	@_('ecrire')
	def instruction(self, p):
		return p[0]

	@_('lire')
	def instruction(self,p):
		return p[0]

	@_('ECRIRE "(" expr ")" ";"')
	def ecrire(self, p):
		return arbre_abstrait.Ecrire(p.expr)  # p.expr = p[2]

	@_('LIRE "(" ")"')
	def lire(self):
		return arbre_abstrait.Lire()

	@_('expr "+" produit')
	def expr(self,p):
		return arbre_abstrait.Operation('+',p[0],p[2])

	@_('expr "-" produit')
	def expr(self,p):
		return arbre_abstrait.Operation('-',p[0],p[2])

	@_('"-" facteur')
	def facteur(self,p):
		return arbre_abstrait.Operation('*', arbre_abstrait.Entier("-1"), p.facteur)

	@_('produit "*" facteur')
	def produit(self,p):
		return arbre_abstrait.Operation('*',p[0],p[2])

	@_('produit "/" facteur')
	def produit(self,p):
		return arbre_abstrait.Operation('/',p[0],p[2])

	@_('produit "%" facteur')
	def produit(self,p):
		return arbre_abstrait.Operation('%',p[0],p[2])

	@_('produit')
	def expr(self, p):
		return p.produit

	@_('facteur')
	def produit(self, p):
		return p.facteur

	@_('"(" expr ")"')
	def facteur(self, p):
		return p.expr

	@_('ENTIER')
	def facteur(self, p):
		return arbre_abstrait.Entier(p.ENTIER)

	@_('variable')
	def facteur(self, p):
		return p.variable

	@_('IDENTIFIANT')
	def variable(self, p):
		return arbre_abstrait.Variable(p.IDENTIFIANT)


if __name__ == '__main__':
	lexer = FloLexer()
	parser = FloParser()
	if len(sys.argv) < 2:
		print("usage: python3 analyse_syntaxique.py NOM_FICHIER_SOURCE.flo")
	else:
		with open(sys.argv[1], "r") as f:
			data = f.read()
			try:
				arbre = parser.parse(lexer.tokenize(data))
				if arbre == None:
					print("There are some errors")
				else:
					arbre.afficher()
			except EOFError:
			    exit()
