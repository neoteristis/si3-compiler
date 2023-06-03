import arbre_abstrait

VAR=100
FUNCTION=101
INT="entier"
BOOL="booleen"
VOID=None
OPERATION="operation"

class Context:
    def __init__(self):
        self.variables=[]
        self.functions=[]
        self.current_function=[]
    def addFunction(self, name, params, returnType):
        self.functions.append([name, params, returnType])
    def addVariables(self, name, type):
        self.variables.append([name,type])
    def setCurrentFunction(self, name, returnType):
        self.current_function=[name,returnType]
    def extend(self, context):
        self.variables.extend(context.variables)
        self.functions.extend(context.functions)
        if self.current_function==[]:
            self.current_function=context.current_function

class BorrowChecker:
    def __init__(self, tree):
        self.tree=tree
        self.forbbiden_op = {
            "entier" : ["=", "and", "or", "!"],
            "booleen" : ["=", "+", "-" , "*", "/", "%", ">", "<", ">=", "<="],
            "operation" : ["="]
        }
        self.return_op = {
            "=" : None,
            "+" : "entier",
            "-" : "entier",
            "/" : "entier",
            "*" : "entier",
            "%" : "entier",
            "and" : "booleen",
            "or" : "booleen",
            ">" : "booleen",
            "<" : "booleen",
            ">=" : "booleen",
            "<=" : "booleen",
            "!" : "booleen",
            "==" : "booleen",
            '!=' : "booleen"
        }
        self.compatible_op = {
            "=" : ["entier", "booleen"],
            "+" : ["entier"],
            "-" : ["entier"],
            "/" : ["entier"],
            "*" : ["entier"],
            "%" : ["entier"],
            "and" : ["booleen"],
            "or" : ["booleen"],
            ">" : ["entier"],
            "<" : ["entier"],
            ">=" : ["entier"],
            "<=" : ["entier"],
            "!" : ["booleen"],
            "==" : ["entier", "booleen"],
            "!=" : ["entier", "booleen"]
        }
    def check(self):
        try:
            context_parent = self.installStandardLib()
            context_parent.setCurrentFunction("main", VOID)
            self.checkListInstructions(context_parent,Context(),self.tree.listeInstructions.instructions)
        except Exception as e:
            print("Error: " + str(e))
            return False
        return True
    def checkListInstructions(self, context_parent, context, instructions):
        context.extend(context_parent)
        for instruction in instructions:
            if arbre_abstrait.DeclareOperation == type(instruction):
                expr=instruction.expr
                typeExpr=self.checkExpression(context, expr)
                if typeExpr!=instruction.type:
                    raise Exception("Bad type expression for " + instruction.name)
                context.addVariables(instruction.name,instruction.type)
            elif arbre_abstrait.LoopOperation == type(instruction):
                expr=instruction.expr
                if self.checkExpression(context, expr) != BOOL:
                    raise Exception("Loop condition must be a bool expression")
                self.checkListInstructions(context,Context(),instruction.statement.instructions)
            elif arbre_abstrait.ConditionalOperation == type(instruction):
                expr=instruction.expr
                statement1=instruction.statement
                statement2=instruction.statement2
                if self.checkExpression(context, expr) != BOOL:
                    raise Exception("If condition must be a bool expression")
                if statement1!=None and type(statement1)!=arbre_abstrait.NoneOperation:
                    self.checkListInstructions(context,Context(),statement1.instructions)
                if statement2!=None and type(statement2)!=arbre_abstrait.NoneOperation:
                    if type(statement2) == arbre_abstrait.ConditionalOperation:
                        self.checkListInstructions(context,Context(),[statement2])
                    else:
                        self.checkListInstructions(context,Context(),statement2.instructions)
            elif arbre_abstrait.Function == type(instruction):
                args=instruction.args.declarations
                sub_context=Context()
                for arg in args:
                    sub_context.addVariables(arg.name,arg.type)
                sub_context.setCurrentFunction(instruction.name, instruction.return_type)
                context.addFunction(instruction.name,instruction.args,instruction.return_type)
                if type(instruction.instructions) != arbre_abstrait.NoneOperation:
                    self.checkListInstructions(context,sub_context,instruction.instructions.instructions)
            elif arbre_abstrait.Operation == type(instruction):
                self.checkExpression(context, instruction)
            elif arbre_abstrait.FunctionOperation == type(instruction):
                self.checkFunction(context, instruction)
            elif arbre_abstrait.ReturnOperation == type(instruction):
                if context.current_function[0]=="main":
                    raise Exception("None of return operation allowed here")
                typeR=self.checkExpression(context, instruction.expr)
                if typeR!=context.current_function[1]:
                    raise Exception("Bad return type !")
    def checkExpression(self, context_parent, expr):
        if type(expr) == arbre_abstrait.Operation:
            return self.checkOperation(context_parent, expr)
        elif type(expr) == arbre_abstrait.FunctionOperation:
            return self.checkFunction(context_parent, expr)
        elif type(expr)==arbre_abstrait.Entier:
            return INT
        elif type(expr)==arbre_abstrait.Boolean:
            return BOOL
        elif type(expr)==arbre_abstrait.Variable:
            if not self.checkContext(context_parent, VAR, expr.name, None):
                raise Exception(expr.name +" not found in the scope") 
            return self.getTypeOfVar(context_parent, expr.name)
    def checkOperation(self, context_parent, expr):
        op=expr.op
        expr1=expr.exp1
        expr2=expr.exp2
        if type(expr1)==arbre_abstrait.Variable:
            if not self.checkContext(context_parent, VAR, expr1.name, None):
                raise Exception(expr1.name +" not found in the scope")
            if type(expr2)==arbre_abstrait.Variable:
                if not self.checkContext(context_parent, VAR, expr2.name, None):
                    raise Exception(expr2.name +" not found in the scope")
                if not self.checkMatchVariable(context_parent,expr1.name,expr2.name):
                    raise Exception(expr1.name +" is incompatible type with " + expr2.name)
            elif type(expr2)==arbre_abstrait.Entier:
                if self.getTypeOfVar(context_parent,expr1.name)!=INT:
                    raise Exception(expr1.name +" is incompatible type with " + str(expr2.valeur))
            elif type(expr2)==arbre_abstrait.Boolean:
                if self.getTypeOfVar(context_parent,expr1.name)!=BOOL:
                    raise Exception(expr1.name +" is incompatible type with " + str(expr2.valeur))
            else:
                typeE=self.checkExpression(context_parent, expr2)
                if self.getTypeOfVar(context_parent,expr1.name)!=typeE:
                    raise Exception(expr1.name + " is incompatible with type of right expression")
        elif type(expr1)==arbre_abstrait.Entier:
            if not self.checkOp(INT, op):
                raise Exception("Forbidden operation between a number and a expression")
            if type(expr2)==arbre_abstrait.Variable:
                if not self.checkContext(context_parent, VAR, expr2.name, None):
                    raise Exception(expr2.name +" not found in the scope")
                if self.getTypeOfVar(context_parent, expr2.name)!=INT:
                    raise Exception(str(expr1.valeur) + " is incompatible with variable " + expr2.name)
            elif type(expr2)==arbre_abstrait.Entier:
                pass
            elif type(expr2)==arbre_abstrait.Boolean:
                raise Exception(str(expr1.valeur) +" incompatible type with " + str(expr2.valeur))
            else:
                typeE=self.checkExpression(context_parent, expr2)
                if INT!=typeE:
                    raise Exception(str(expr1.valeur) + " is incompatible with type of right expression")
        elif type(expr1)==arbre_abstrait.Boolean:
            if not self.checkOp(BOOL, op):
                raise Exception("Forbidden operation between a number and a expression")
            if type(expr2)==arbre_abstrait.Variable:
                if not self.checkContext(context_parent, VAR, expr2.name, None):
                    raise Exception(expr2.name +" not found in the scope")
                if self.getTypeOfVar(context_parent, expr2.name)!=BOOL:
                    raise Exception(str(expr1.valeur) + " is incompatible with variable " + expr2.name)
            elif type(expr2)==arbre_abstrait.Entier:
                raise Exception(str(expr1.valeur) +" incompatible type with " + str(expr2.valeur))
            elif type(expr2)==arbre_abstrait.Boolean:
                pass
            else:
                typeE=self.checkExpression(context_parent, expr2)
                if BOOL!=typeE:
                    raise Exception(str(expr1.valeur) + " is incompatible with type of right expression")
        elif type(expr1)==arbre_abstrait.Operation:
            if not self.checkOp(OPERATION, op):
                raise Exception("Forbidden operation between two expression")
            typeE=self.checkExpression(context_parent, expr1)
            if not self.checkTypeOp(op, typeE):
                raise Exception("Forbidden operation between two expression")
            if type(expr2)==arbre_abstrait.Variable:
                if not self.checkContext(context_parent, VAR, expr2.name, None):
                    raise Exception(expr2.name +" not found in the scope")
                if self.getTypeOfVar(context_parent,expr2.name)!=typeE:
                    raise Exception(str(expr2.name)+ " is incompatible with type of left expression")
            elif type(expr2)==arbre_abstrait.Entier:
                if typeE != INT:
                    raise Exception(str(expr2.valeur)+ " is incompatible with type of left expression")
            elif type(expr2)==arbre_abstrait.Boolean:
                if typeE != BOOL:
                    raise Exception(str(expr2.valeur) + " is incompatible with type of left expression")
            else:
                typeE2 = self.checkExpression(context_parent, expr2)
                if typeE != typeE2:
                    raise Exception("Two expressions are incompatible with type of left expression")
        return self.getTypeReturnOp(op)
    
    def checkFunction(self, context_parent, expr):
        name=expr.name
        listParam=expr.listeParameters
        if not self.checkContext(context_parent, FUNCTION, name, None):
            raise Exception("Function " + name + " not find !")
        if not self.checkParams(context_parent, name, listParam):
            raise Exception("Parameters not match")
        return self.getFunctionReturnType(context_parent, name)
            
    def checkContext(self, context, type, name ,rtype):
        array=[]
        if type==VAR:
            array=context.variables
        else:
            array=context.functions
        for item in array:
            if item[0] == name:# and context[2] == rtype:
                return True
        return False
    def checkMatchVariable(self, context, name1, name2):
        var1=None
        for item in context.variables:
            if item[0] == name1:
                var1=item
        for item in context.variables:
            if item[0] == name2:
                if var1[1] != item[1]:
                    return False
        return True
    def getTypeOfVar(self, context, name):
        for item in context.variables:
            if item[0] == name:
                return item[1]
        return None
    def checkOp(self, type, op):
        if op in self.forbbiden_op[type]:
            return False
        return True
    def getTypeReturnOp(self, op):
        return self.return_op[op]
    def checkTypeOp(self, op, typeE):
        types=self.compatible_op[op]
        return typeE in types
    def getFunctionParams(self, context, name_function):
        for item in context.functions:
            if item[0] == name_function:
                return item[1]
        return None
    def getFunctionReturnType(self, context, name_function):
        for item in context.functions:
            if item[0] == name_function:
                return item[2]
        return None
    def checkParams(self, context, name_function, param):
        params=self.getFunctionParams(context, name_function)
        if len(params.declarations) != len(param.parameters):
            return False
        for p in param.parameters:
            find=False
            for p2 in params.declarations:
                typeVar=self.checkExpression(context, p)
                if typeVar == p2.type:
                    find=True
            if not find:
                return False
        return True
    def installStandardLib(self):
        context=Context()
        context.addFunction("lire", arbre_abstrait.ListeDeclarations(), INT)
        ecrire_parameter=arbre_abstrait.ListeDeclarations()
        ecrire_parameter.declarations.append(arbre_abstrait.DeclareOperation(INT, "msg"))
        context.addFunction("ecrire", ecrire_parameter, VOID)
        return context