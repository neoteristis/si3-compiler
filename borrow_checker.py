import arbre_abstrait

VAR=100
FUNCTION=101

class BorrowChecker:
    def __init__(self, tree):
        self.tree=tree
    def check(self):
        self.checkListInstructions([],[],self.tree.listeInstructions.instructions)
    def checkListInstructions(self, context_parent, context, instructions):
        context.extend(context_parent)
        for instruction in instructions:
            if arbre_abstrait.DeclareOperation == type(instruction):
                print("Declare:" + instruction.name)
                context.append([VAR,instruction.name,instruction.type])
            elif arbre_abstrait.LoopOperation == type(instruction):
                expr=instruction.expr
                self.checkListInstructions(context,[],instruction.statement.instructions)
            elif arbre_abstrait.ConditionalOperation == type(instruction):
                expr=instruction.expr
                statement1=instruction.statement
                statement2=instruction.statement2
                if statement1!=None and type(statement1)!=arbre_abstrait.NoneOperation:
                    self.checkListInstructions(context,[],statement1.instructions)
                if statement2!=None and type(statement2)!=arbre_abstrait.NoneOperation:
                    if type(statement2) == arbre_abstrait.ConditionalOperation:
                        self.checkListInstructions(context,[],[statement2])
                    else:
                        self.checkListInstructions(context,[],statement2.instructions)
            elif arbre_abstrait.Function == type(instruction):
                args=instruction.args.declarations
                sub_context=[]
                for arg in args:
                    sub_context.append([VAR,arg.name,arg.type])
                context.append([FUNCTION,instruction.name,instruction.return_type])
                if type(instruction.instructions) != arbre_abstrait.NoneOperation:
                    self.checkListInstructions(context,sub_context,instruction.instructions.instructions)
            elif arbre_abstrait.Operation == type(instruction):
                self.checkExpression(context, instruction)
    def checkExpression(self, context_parent, expr):
        op=expr.op
        expr1=expr.exp1
        expr2=expr.exp2
        if type(expr1)==arbre_abstrait.Variable:
            if not self.checkContext(context_parent, VAR, expr1.name, None):
                raise Exception(expr1.name +" not found in the scope")
            if type(expr2)==arbre_abstrait.Variable:
                if not self.checkMatchVariable(context_parent,expr1.name,expr2.name):
                    raise Exception(expr1.name +" incompatible type with " + expr2.name)
    def checkContext(self, context, type, name ,rtype):
        for item in context:
            if item[0] == type and item[1] == name:# and context[2] == rtype:
                return True
        return False
    def checkMatchVariable(self, context, name1, name2):
        var1=None
        for item in context:
            if item[0] == VAR and item[1] == name1:
                var1=item
        for item in context:
            if item[0] == VAR and item[1] == name2:
                if var1[2] != item[2]:
                    return False
        return True