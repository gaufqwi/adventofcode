from aocpython.problem import AOCProblem
from math import trunc

class VariableModulus(Exception):
    pass

class Node:
    def __init__(self, op=None, lterm=None, rterm=None, constant=None, variable=None):
        if variable != None:
            self.variable = variable
        elif constant != None:
            self.constant = constant
        elif hasattr(lterm, 'constant') and hasattr(rterm, 'constant'):
            if op in ['*', '+', '%']:
                self.constant = eval(f'{lterm.constant}{op}{rterm.constant}')
            elif op == '/':
                self.constant = trunc(lterm.constant / rterm.constant)
            elif op == '=':
                self.constant = int(lterm.constant == rterm.constant)
        elif op == '+':
            if hasattr(lterm, 'constant') and lterm.constant == 0:
                self.absorb(rterm)
            elif hasattr(rterm, 'constant') and rterm.constant == 0:
                self.absorb(lterm)
            else:
                self.op, self.lterm, self.rterm = op, lterm, rterm
        elif op == '*':
            if hasattr(lterm, 'constant'):
                if lterm.constant == 0:
                    self.constant = 0
                elif lterm.constant == 1:
                    self.absorb(rterm)
                else:
                    self.op, self.lterm, self.rterm = op, lterm, rterm
            elif hasattr(rterm, 'constant'):
                if rterm.constant == 0:
                    self.constant = 0
                elif rterm.constant == 1:
                    self.absorb(lterm)
                else:
                    self.op, self.lterm, self.rterm = op, lterm, rterm
            else:
                self.op, self.lterm, self.rterm = op, lterm, rterm
        elif op == '/':
            if hasattr(lterm, 'constant') and lterm.constant == 0:
                self.constant = 0
            elif hasattr(rterm, 'constant') and rterm.constant == 1:
                self.absorb(lterm)
            else:
                self.op, self.lterm, self.rterm = op, lterm, rterm
        elif op == '%':
            if hasattr(lterm, 'constant') and lterm.constant == 0:
                self.constant = 0
            elif hasattr(rterm, 'constant') and rterm.constant == 1:
                self.absorb(lterm)
            else:
                self.op, self.lterm, self.rterm = op, lterm, rterm
        elif op == '=':
            if hasattr(lterm, 'variable') and hasattr(rterm, 'constant') and rterm.constant not in range(1,10):
                self.constant = 0
            elif hasattr(rterm, 'variable') and hasattr(lterm, 'constant') and lterm.constant not in range(1,10):
                self.constant = 0
            else:
                self.op, self.lterm, self.rterm = op, lterm, rterm

    def __repr__(self):
        if hasattr(self, 'constant'):
            return str(self.constant)
        elif hasattr(self, 'variable'):
            return f'V{self.variable}'
        else:
            return f'({self.lterm}{self.op}{self.rterm})'

    def get_possible_values(self):
        try:
            return self.possible_values
        except AttributeError:
            pass
        if hasattr(self, 'constant'):
            self.possible_values = {self.constant}
        elif hasattr(self, 'variable'):
            self.possible_values = set(range(1,10))
        elif self.op == '=':
            l = self.lterm.get_possible_values()
            r = self.rterm.get_possible_values()
            if len(l.intersection(r)) == 0:
                return {0}
            elif len(l) == 1 and len(r) == 1 and len(l.intersection(r)) == 1:
                self.possible_values = {1}
            else:
                self.possible_values = {0, 1}
        elif self.op in ['*', '+']:
            self.possible_values = set()
            for l in self.lterm.get_possible_values():
                for r in self.rterm.get_possible_values():
                    self.possible_values.add(eval(f'{l}{self.op}{r}'))
        elif self.op == '/':
            self.possible_values = set()
            for l in self.lterm.get_possible_values():
                for r in self.rterm.get_possible_values():
                    try:
                        self.possible_values.add(trunc(l / r))
                    except ZeroDivisionError:
                        pass
        elif self.op == '%':
            try:
                m = self.rterm.constant
            except AttributeError:
                raise VariableModulus
            self.possible_values = set()
            for l in self.lterm.get_possible_values():
                self.possible_values.add(l % m)
                if len(self.possible_values) == m:
                    break
        return self.possible_values

    def absorb(self, other):
        attributes = ['op', 'lterm', 'rterm', 'constant', 'variable', 'possible_values']
        for a in attributes:
            try:
                setattr(self, a, getattr(other, a))
            except AttributeError:
                pass
            
class Problem(AOCProblem):
    def common(self):
        self.instructions = []
        for line in self.data:
            instruction = line.strip().split()
            if len(instruction) == 3:
                try:
                    instruction = (instruction[0], instruction[1], int(instruction[2]))
                except ValueError:
                    pass
            self.instructions.append(instruction)

    def simplify(self, expression):
        if expression[0] == '-':
            print(expression)
        if expression[0] != '(':
            return expression
        if 'D' not in expression:
            try:
                return str(int(eval(expression)))
            except SyntaxError:
                pass
        pcount = 0
        for i in range(len(expression)):
            c = expression[i]
            if c == '(':
                pcount += 1
            elif c == ')':
                pcount -= 1
            elif pcount == 1 and c in ['*', '+', '/', '%', '=']:
                lop = expression[1:i]#self.simplify(expression[1:i])
                rop = expression[i+1:-1]#self.simplify(expression[i+1:-1])
                break
        if c == '*':
            if lop == '0' or rop == '0':
                return '0'
            elif lop == '1':
                return rop
            elif rop == '1':
                return lop
        elif c == '+':
            if lop == '0':
                return rop
            elif rop == '0':
                return lop
        elif c == '/':
            if lop == '0':
                return '0'
            elif rop == '1':
                return lop
        elif c == '%':
            if lop == '0':
                return '0'
            elif rop == '1':
                return lop
        elif c == '=':
            if lop == rop:
                return '1'
            elif lop[0] == 'D' and rop not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return '0'
            elif rop[0] == 'D' and lop not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return '0'
        return f'({lop}{c}{rop})'

    def run(self, n):
        n = list(str(n))
        alu = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        for instruction in self.instructions:
            op = instruction[0]
            dest = instruction[1]
            if op != 'inp':
                if type(instruction[2]) == int:
                    val = instruction[2]
                else:
                    val = alu[instruction[2]]
            if op == 'inp':
                alu[dest] = int(n.pop(0))
            elif op == 'add':
                alu[dest] = alu[dest] + val
            elif op == 'mul':
                alu[dest] = alu[dest] * val
            elif op == 'div':
                alu[dest] = trunc(alu[dest] / val)
            elif op == 'mod':
                alu[dest] = alu[dest] % val
            elif op == 'eql':
                alu[dest] = int(alu[dest] == val)
        return alu

    def run_symbol_node(self, bindings={}):
        varno = 0
        alu = {'w': Node(constant=0), 'x': Node(constant=0), 'y': Node(constant=0), 'z': Node(constant=0)}
        for j, instruction in enumerate(self.instructions):
            op = instruction[0]
            dest = instruction[1]
            if op != 'inp':
                if type(instruction[2]) == int:
                    val = Node(constant=instruction[2])
                else:
                    val = alu[instruction[2]]
            if op == 'inp':
                if varno in bindings:
                    alu[dest] = Node(constant=bindings[varno])
                else:
                    alu[dest] = Node(variable=varno)
                varno += 1
            elif op == 'add':
                alu[dest] = Node(op='+', lterm=alu[dest], rterm=val)
            elif op == 'mul':
                alu[dest] = Node(op='*', lterm=alu[dest], rterm=val)
            elif op == 'div':
                alu[dest] = Node(op='/', lterm=alu[dest], rterm=val)
            elif op == 'mod':
                alu[dest] = Node(op='%', lterm=alu[dest], rterm=val)
            elif op == 'eql':
                alu[dest] = Node(op='=', lterm=alu[dest], rterm=val)
        return alu

    def part1(self):
        pos = 0
        bindings = {}
        done = False
        while not done:
            bindings[pos] = bindings.get(pos, 10) - 1
            z = self.run_symbol_node(bindings)['z']
            if 0 in z.get_possible_values():
                pos += 1
                if pos == 14:
                    done = True
            else:
                while bindings[pos] == 1:
                    del bindings[pos]
                    pos -= 1
        n = ''
        for i in range(14):
            n += str(bindings[i])
        print(f'Greatest serial number is {n}')

    def part2(self):
        pos = 0
        bindings = {}
        done = False
        while not done:
            bindings[pos] = bindings.get(pos, 0) + 1
            z = self.run_symbol_node(bindings)['z']
            if 0 in z.get_possible_values():
                pos += 1
                if pos == 14:
                    done = True
            else:
                while bindings[pos] == 9:
                    del bindings[pos]
                    pos -= 1
                #bindings[pos] -= 1
        n = ''
        for i in range(14):
            n += str(bindings[i])
        print(f'Least serial number is {n}')
