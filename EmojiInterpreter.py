from lark.visitors import Interpreter
from lark.tree import Tree
# import lark
from lark import Token


class SymbolTable:
    def __init__(self) -> None:
        self.table = []

    def addScope(self):
        self.table.append({})

    def addSymbol(self, symbol, value=None):
        if(symbol in self.table[-1]):
            raise Exception(f"Redeclaration In Same Scope of '{symbol}'")
        self.table[-1][symbol] = value

    def doesSymbolExist(self, symbol) -> int:
        for i in range(len(self.table) - 1, -1, -1):
            if symbol in self.table[i]:
                return i
        return -1

    def updateSymbol(self, symbol, value):
        tableId = self.doesSymbolExist(symbol)
        if(tableId == -1):
            raise Exception(f"assignment of undeclared variable '{symbol}'")
        self.table[tableId][symbol] = value

    def getValue(self, symbol):
        tableId = self.doesSymbolExist(symbol)
        if(tableId == -1):
            raise Exception(f"{symbol} is undeclared")
        return self.table[tableId][symbol]

    def removeScope(self):
        if len(self.table) == 0:
            raise Exception("Internal exception: No scope to remove")
        self.table.pop()


class EmojiLangInterpeter(Interpreter):
    def __init__(self, parseTree: Tree) -> None:
        super().__init__()
        self.sTable = SymbolTable()
        self.parseTree = parseTree
        self.isAssignmentDeclaration = False

    def start(self):
        self.visit(self.parseTree)

    def stmt(self, tree):
        # print(tree)
        self.visit_children(tree)

    def assignment_stmt(self, tree):
        self.visit_children(tree)

    def name(self, tree: Tree):
        return 1
        return self.sTable.getValue(tree.children[0].value)
        # return self.sTable.getValue()

    def number(self, tree: Tree):
        # print(tree.children[0].value)
        return int(tree.children[0].value)

    def exp(self, tree: Tree):
        value = self.visit(tree.children[0])
        # print(value)
        # print(tree.children[0].type)
        for i in range(1, len(tree.children)):
            if tree.children[i] == '+':
                value += self.visit(tree.children[i+1])
            elif tree.children[i] == '-':
                value -= self.visit(tree.children[i+1])
        # print(value)
        return value

    def multiplyexp(self, tree: Tree):
        value = self.visit(tree.children[0])
        for i in range(1, len(tree.children)):
            if tree.children[i] == '*':
                value *= self.visit(tree.children[i+1])
            elif tree.children[i] == '/':
                value /= self.visit(tree.children[i+1])
        return value

    def test(self, tree: Tree):
        value = str(self.visit(tree.children[0]))
        for i in range(1, len(tree.children)):
            if tree.children[i] in [">", "<", ">=", "<=", "==", "!="]:
                value += tree.children[i]
            else:
                value += str(self.visit(tree.children[i]))
        return 1 if eval(value) else 0

    def print_stmt(self, tree: Tree):
        value = self.visit(tree.children[0])
        print(value)
    
    def assignment_stmt(self, tree: Tree):
        pass
        if self.isAssignmentDeclaration:
            self.sTable.addSymbol()
