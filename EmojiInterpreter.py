from lark.exceptions import T
from lark.visitors import Interpreter
from lark.tree import Tree
# import lark
from lark import Token, logger


class SymbolTable:
    def __init__(self, isDebug) -> None:
        self.table = []
        self.isDebug = isDebug
    
    def debugSymbolTable(self):
        if self.isDebug:
            print(self.table)

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
            raise Exception(f"'{symbol}' is undeclared")
        return self.table[tableId][symbol]

    def removeScope(self):
        if len(self.table) == 0:
            raise Exception("Internal exception: No scope to remove")
        self.table.pop()


class EmojiLangInterpeter(Interpreter):
    def __init__(self, parseTree: Tree) -> None:
        super().__init__()
        self.sTable = SymbolTable(isDebug=False)
        self.parseTree = parseTree
        self.isAssignmentDeclaration = False   #used to provide declaration context

    def start(self):
        self.sTable.addScope() #set global scope before interpreter starts
        self.visit(self.parseTree)

    def stmt(self, tree):
        # print(tree)
        self.visit_children(tree)
        

    def assignment_stmt(self, tree):
        self.visit_children(tree)

    def name(self, tree: Tree):
        # return 1
        return self.sTable.getValue(tree.children[0].value)

    def number(self, tree: Tree):
        # print(tree.children[0].value)
        return int(tree.children[0].value)

    def exp(self, tree: Tree):
        value = self.visit(tree.children[0])
        for i in range(1, len(tree.children)):
            if tree.children[i] == '+':
                value += self.visit(tree.children[i+1])
            elif tree.children[i] == '-':
                value -= self.visit(tree.children[i+1])
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
        # print(eval(value))
        return int(eval(value))

    def print_stmt(self, tree: Tree):
        value = self.visit(tree.children[0])
        print(value)   #don't comment this, it is print logic
    
    def assignment_stmt(self, tree: Tree):
        symbol = tree.children[0].children[0].value
        value = self.visit(tree.children[1])
        if self.isAssignmentDeclaration:
            self.sTable.addSymbol(symbol, value)
        else:
            self.sTable.updateSymbol(symbol, value)
        self.sTable.debugSymbolTable()
        
    
    def declare_stmt(self, tree: Tree):
        self.isAssignmentDeclaration = True
        for child in tree.children:
            if child.data == 'name':
                # print(child.children[0].value)
                self.sTable.addSymbol(child.children[0].value)
            else: # else this is the assignment_stmt
                self.visit(child)
        self.isAssignmentDeclaration = False
        self.sTable.debugSymbolTable()
    
    def suite(self, tree: Tree):
        for i in range(len(tree.children)-1):
            if not isinstance(tree.children[i], Token):
                ret = self.visit(tree.children[i])
                if ret in ['break', 'continue']:
                    return ret
        return None

    def if_stmt(self, tree: Tree):
        # print(tree.pretty())
        for i in range(0, len(tree.children)):
            if tree.children[i] in ['if', 'elif']:
                cond = self.visit(tree.children[i+1])
                if cond: # if condition is true evaluate the suit and return
                    self.sTable.addScope() #if-else, while, runs in thier scope
                    ret = self.visit(tree.children[i+2])
                    self.sTable.removeScope()
                    # print(ret)
                    return ret
            elif tree.children[i] == 'else':
                return self.visit(tree.children[i+1])
                
    
    def while_stmt(self, tree: Tree):
        cond = self.visit(tree.children[0])
        while cond: # if condition is true evaluate the suit and return
            self.sTable.addScope() #if-else, while, runs in thier scope
            ret = self.visit(tree.children[1])
            self.sTable.removeScope()
            if ret == 'break':
                break               #see explanation in for section
            cond = self.visit(tree.children[0])

        return

    def for_stmt(self, tree: Tree):
        # for produces two new scopes one for implicit variable declarations
        # example-
        # for(decl a=5, b; a<10; a=a+1){
        #   decl d=10, g, h=8
        # }
        # in the above example outer scope is for a, b
        # and the inner scope is for d, g, h
        # outer scope persists between loop iterationis 
        # whereas for every iteration the d, g, h are redeclared and their values doesn't persist
        # print(tree.pretty())
        self.sTable.addScope() #outer scope
        self.visit(tree.children[0]) #visit for_declarations(for_decl)
        cond = self.visit(tree.children[1])
        # print(cond)
        while cond:
            self.sTable.addScope() #inner scope
            ret = self.visit(tree.children[3]) # loop body
            self.sTable.removeScope()
            if ret == 'break': #just break this loop also
                break           #also do nothing on the continue as the suit has alredy skipped the next statements and the loop will work as normal
            self.visit(tree.children[2]) # update statement
            cond = self.visit(tree.children[1]) #revaulate the condition after update
        self.sTable.removeScope()
        return
    
    # the below are separate from other similar rules becuase they can empty
    # we need to handle them accordingly

    def for_decl(self, tree: Tree):  
        self.visit_children(tree) #this is normal but can contain both declarations and assignments

    def for_test(self, tree: Tree):
        if len(tree.children) == 0:
            return True    #implies the loop is infite unless where
        return self.visit(tree.children[0])
    
    def for_updates(self, tree: Tree):
        self.visit_children(tree)
        return

    def flow_stmt(self, tree: Tree):
        # print(tree.pretty(), tree.children[0].data)
        return 'break' if tree.children[0].data == 'break_stmt' else 'continue'
        #this could be 'break' or 'continue' only
            


         



