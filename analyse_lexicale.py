import sys
from sly import Lexer

class FloLexer(Lexer):
	# Noms des lexèmes (sauf les litéraux). En majuscule. Ordre non important
	tokens = { IDENTIFIANT, ENTIER, BOOLEAN, INFERIEUR_OU_EGAL,SUPERIEUR_OU_EGAL,
			   DIFFERENT, EQUAL, ET, OU, NON, SI, SINON, TANTQUE, RETOURNER , AFFECT, SEPARATOR,  INT,BOOL}

	#Les caractères litéraux sont des caractères uniques qui sont retournés tel quel quand rencontré par l'analyse lexicale. 
	#Les litéraux sont vérifiés en dernier, après toutes les autres règles définies par des expressions régulières.
	#Donc, si une règle commence par un de ces littérals (comme INFERIEUR_OU_EGAL), cette règle aura la priorité.
	literals = {'+', '-' , '*', '(', ')', ';', "{", "}", "%", "/", '<', '>'}
	
	# chaines contenant les caractère à ignorer. Ici espace et tabulation
	ignore = ' \t'

	# Expressions régulières correspondant au différents Lexèmes par ordre de priorité
	INFERIEUR_OU_EGAL= r'<='
	SUPERIEUR_OU_EGAL= r'>='
	DIFFERENT = r'!='
	EQUAL = r'=='

	AFFECT = r'='
	SEPARATOR = r','

	# opérateur booléen
	ET = r'et'
	OU = r'ou'
	NON = r'non'
	
	@_(r'0|[1-9][0-9]*')
	def ENTIER(self, t):
		t.value = int(t.value)
		return t

	@_(r'Vrai|Faux')
	def BOOLEAN(self, t):
		if t.value=="Vrai":
			t.value=True
		else:
			t.value=False
		return t

    	# cas général
	IDENTIFIANT = r'[a-zA-Z][a-zA-Z0-9_]*' #en général, variable ou nom de fonction

	# cas spéciaux:
	IDENTIFIANT['si'] = SI
	IDENTIFIANT['sinon'] = SINON
	IDENTIFIANT['tantque'] = TANTQUE
	IDENTIFIANT['retourner'] = RETOURNER
	IDENTIFIANT['entier'] = INT
	IDENTIFIANT['booleen'] = BOOL
	#Syntaxe des commentaires à ignorer
	ignore_comment = r'\#.*'

	# Permet de conserver les numéros de ligne. Utile pour les messages d'erreurs
	@_(r'\n+')
	def ignore_newline(self, t):
		self.lineno += t.value.count('\n')

	# En cas d'erreur, indique où elle se trouve
	def error(self, t):
		print(f'Ligne{self.lineno}: caractère inattendu "{t.value[0]}"')
		self.index += 1

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("usage: python3 analyse_lexicale.py NOM_FICHIER_SOURCE.flo")
	else:
		with open(sys.argv[1],"r") as f:
			data = f.read()
			lexer = FloLexer()
			for tok in lexer.tokenize(data):
				print(tok)
