######
#@Jonathan ke
#@9/23/2019
#Java Token objects

class Token(object):
    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return self.string

class Identifier(Token):
    def __init__(self, string):
        super().__init__(string)

    def __repr__(self):
        return "Id: "+self.string

class Keyword(Token):
    def __init__(self, string):
        super().__init__(string)

    def __repr__(self):
        return "Key: "+self.string

class Separator(Token):
    def __init__(self, string):
        super().__init__(string)

    def __repr__(self):
        return "Sep: "+ self.string

class Operator(Token):
    def __init__(self, string):
        super().__init__(string)

    def __repr__(self):
        return "Op: "+self.string

class Literal(Token):
    def __init__(self, string):
        super().__init__(string)

    def __repr__(self):
        return "Lit: "+self.string

class Comment(Token):
    def __init__(self, string):
        super().__init__(string)

    def __repr__(self):
        return "Com: "+self.string