"""
Affiche une chaine de caractère avec une certaine identation
"""
def afficher(s,indent=0):
	print(" "*indent+s)
	
class Programme:
	def __init__(self,listeInstructions):
		self.listeInstructions = listeInstructions
	def afficher(self,indent=0):
		afficher("<programme>",indent)
		self.listeInstructions.afficher(indent+1)
		afficher("</programme>",indent)
  
class Function:
	def __init__(self,name,return_type,args,instructions):
		self.name=name
		self.return_type=return_type
		self.args=args
		self.instructions=instructions
	def afficher(self,indent=0):
		afficher("<function>",indent)
		afficher("[Name:"+str(self.name)+"]",indent+1)
		afficher("[Return Type:"+str(self.return_type)+"]",indent+1)
		afficher("<Arguments>",indent+1)
		self.args.afficher(indent+2)
		afficher("</Arguments>",indent+1)
		self.instructions.afficher(indent+1)
		afficher("</function>",indent)
    

class ListeInstructions:
	def __init__(self):
		self.instructions = []
	def afficher(self,indent=0):
		afficher("<listeInstructions>",indent)
		for instruction in self.instructions:
			instruction.afficher(indent+1)
		afficher("</listeInstructions>",indent)
  
class ListeParameters:
    def __init__(self):
        self.parameters = []
    def afficher(self,indent=0):
        afficher("<listeParameters>", indent)
        for parameter in self.parameters:
            parameter.afficher(indent +1)
        afficher("</listeParametes>", indent)
  
class ListeDeclarations:
	def __init__(self):
		self.declarations = []
	def afficher(self,indent=0):
		afficher("<listeDeclarations>", indent)
		for declaration in self.declarations:
			declaration.afficher(indent+1)
		afficher("</listeDeclarations>", indent)

class Ecrire:
	def __init__(self,exp):
		self.exp = exp
	def afficher(self,indent=0):
		afficher("<ecrire>",indent)
		self.exp.afficher(indent+1)
		afficher("</ecrire>",indent)
  
class NoneOperation:
	def __init__(self):
		pass
	def afficher(self, indent=0):
		afficher("<none_operation>",indent)
		afficher("</none_operation>",indent)
  
class ConditionalOperation:
	def __init__(self, expr, statement, statement2=None):
		self.expr=expr
		self.statement=statement
		self.statement2=statement2
	def afficher(self, indent=0):
		afficher("<conditional_operation>",indent)
		self.expr.afficher(indent+1)
		self.statement.afficher(indent+1)
		if self.statement2!=None:
			self.statement2.afficher(indent+1)
		afficher("</conditional_operation>",indent)

class LoopOperation:
	def __init__(self, expr, statement):
		self.expr=expr
		self.statement=statement
	def afficher(self, indent=0):
		afficher("<loop_operation>",indent)
		afficher("<condition>",indent+1)
		self.expr.afficher(indent+2)
		afficher("</condition>",indent+1)
		self.statement.afficher(indent+1)
		afficher("</loop_operation>",indent)        

class Operation:
	def __init__(self,op,exp1,exp2):
		self.exp1 = exp1
		self.op = op
		self.exp2 = exp2
	def afficher(self,indent=0):
		afficher("<operation>",indent)
		afficher(self.op,indent+1)
		self.exp1.afficher(indent+1)
		self.exp2.afficher(indent+1)
		afficher("</operation>",indent)
  
class ReturnOperation:
    def __init__(self,expr):
        self.expr=expr
    def afficher(self,indent=0):
        afficher("<return_operation>", indent)
        self.expr.afficher(indent=indent+1)
        afficher("</return_operation>", indent)
        
  
class DeclareOperation:
	def __init__(self,type,name,expr=NoneOperation()):
		self.type=type
		self.name=name
		self.expr=expr
	def afficher(self,indent=0):
		afficher("<declare_operation>",indent)
		afficher("[Type:"+str(self.type)+"]",indent+1)
		afficher("[Name:"+self.name+"]",indent+1)
		afficher("<value>",indent+1)
		self.expr.afficher(indent=indent+2)
		afficher("</value>",indent+1)
		afficher("</declare_operation>",indent)
  
class FunctionOperation:
    def __init__(self,function_name,listeParameters):
        self.name=function_name
        self.listeParameters=listeParameters
    def afficher(self, indent=0):
        afficher("<function_operation>", indent)
        afficher("[Name:"+self.name+"]",indent+1)
        self.listeParameters.afficher(indent+1)
        afficher("</function_operation>", indent)
        
class UnaryOperator:
	def __init__(self, op, hidden=NoneOperation()):
		self.op=op
		self.hidden=hidden
	def afficher(self,indent=0):
		afficher("<unary_operator>",indent)
		afficher("[Operator:"+str(self.op)+"]",indent+1)
		self.hidden.afficher(indent+1)
		afficher("</unary_operator>",indent)

        

class Entier:
	def __init__(self,valeur):
		self.valeur = valeur
	def afficher(self,indent=0):
		afficher("[Entier:"+str(self.valeur)+"]",indent)
  
class Boolean:
	def __init__(self,valeur):
		self.valeur = valeur
	def afficher(self,indent=0):
		afficher("[Boolean:"+str(self.valeur)+"]",indent)
  
class Variable:
    def __init__(self, name):
        self.name=name
    def afficher(self,indent=0):
        afficher("[Variable:"+self.name+"]", indent)