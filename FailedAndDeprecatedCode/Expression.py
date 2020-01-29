from Token import *

class Expr(object):

    def __init__(self, expr):
        self.expr = expr

class Block(object):

    def __init__(self, block):
        self.statements = block

class Statement(object):

    def __init__(self, statement):
        self.statement = statement

class AssignState(Statement):
    def __init__(self, statement):
        super.__init__(statement)
        self.id = self.statement[0]
        self.op = self.statement[1]
        self.expr = self.statement[2:-1]
        self.sep = self.statement[-1]

class IncrementState(Statement):
    def __init__(self, statement):
        super.__init__(statement)
        self.id = self.statement[0]
        self.op = self.statement[1]
        self.sep = self.statement[2]

class InvocationState(Statement):
    def __init__(self, statement):
        super().__init__(statement)
        self.expr = self.statement


class ObjCreateState(Statement):
    def __init__(self, statement):
        super().__init__(statement)
        self.cast = self.statement[0]
        self.id = self.statement[1]




        

class BinOp(Expr):

    def __init__(self, expr1, op, expr2):
        self.expr1 = expr1
        self.op = op
        self.expr2 = expr2



    



