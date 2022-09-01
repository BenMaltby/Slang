from Stack import Stack
import sys


# 🅲🅾🅽🆂🆃🅰🅽🆃🆂
NUMBERS = "0123456789"
COMMANDS = {
	"|" : "PUSH",
	"," : "POP",
	"'" : "OUTPUT"
}
OP_T = {
	"-" : "MINUS",
	"+" : "PLUS",
	"*" : "MUL",
	"/" : "DIV"
}
FLOAT = "FLOAT"
INT   = "INT"


class TOKEN:  
	"""defines all individual parts of expression"""
	def __init__(self, t_type, t_value=None) -> None:
		self.t_type  = t_type
		self.t_value = t_value

	def __repr__(self) -> str:
		return f'({self.t_type}, {self.t_value})'



class Position:
	"""Class to control header position through input analysis/lexing"""

	def __init__(self, length) -> None:
		self.pos = -1
		self.finished = False
		self.__length = length
		self.advancePos()

	def advancePos(self, check=False) -> bool:  # advances current character index position
		if self.pos+1 < self.__length:
			if check: return True
			self.pos += 1
		else:
			if check: return False
			self.finished = True



class Lexer(Position):
	"""Class to complete the lexical analysis stage of translation"""

	def __init__(self, text) -> None:
		super().__init__(len(text))
		self.__text = text


	def makeNumber(self) -> TOKEN:
		"""allows numbers of multiple digits and handles basic syntax catching"""
		number = ""
		decimal_point = False  # catches decimal point errors

		while self.__text[self.pos] in NUMBERS + ".":
			number += self.__text[self.pos]  # current character

			if self.__text[self.pos] == '.':
				if not decimal_point: decimal_point = True
				else: raise Exception("multiple decimal points")
			
			if self.advancePos(True):  # if not at end of expression
				if self.__text[self.pos+1] in NUMBERS + ".":
					self.advancePos()
				else: break  # break as number is complete
			else:
				raise Exception("Number on it's own fella")

		if decimal_point: return TOKEN(FLOAT, float(number))  # number is float if has point
		else: return TOKEN(INT, int(number))


	def lex(self):

		token_str = []

		while not self.finished:
			curr_char = self.__text[self.pos]

			if curr_char == ' ':  # ignore spaces
				pass

			elif curr_char in NUMBERS:
				token_str.append(self.makeNumber())

			elif curr_char in COMMANDS:
				token_str.append(TOKEN(COMMANDS[curr_char]))

			elif curr_char in OP_T:
				token_str.append(TOKEN(OP_T[curr_char]))

			else:
				raise SyntaxError("Unknown character error!")

			self.advancePos()

		return token_str


class OUTPUT_Node:  # specific for output node because they create new trees
	def __init__(self, branch=None):
		self.branch = branch

	def __repr__(self) -> str:
		return f'OUT({self.branch})'


class OP_Node:  # just for operations in OP_T dictionary
	def __init__(self, left, op_type, right):
			self.left  = left
			self.op_type = op_type
			self.right = right

	def __repr__(self) -> str:
		return f' {self.op_type}({self.left}, {self.right}) '


class Parser(Position):
	"""Creates syntax tree of calculations to be completed based on language rules"""
	def __init__(self, token_str) -> None:
		super().__init__(len(token_str))  # makes handling position much easier
		self.__Tokens = token_str

	def parse(self):
		
		parse_stack = Stack(-1)  # stack size of -1 means infinite
		Execute_buffer = []

		while not self.finished:
			curr_token = self.__Tokens[self.pos]  # makes code nicer to read

			if curr_token.t_type in [FLOAT, INT]:
				parse_stack.push(curr_token)

			elif curr_token.t_type == "OUTPUT":
				Execute_buffer.append(OUTPUT_Node(parse_stack.peek()))

			elif curr_token.t_type == "POP":
				parse_stack.pop()

			elif curr_token.t_type in OP_T.values():
				if parse_stack.length() >= 2:  # operations require 2 numbers to calculate
					right = parse_stack.pop()
					left  = parse_stack.pop()
					parse_stack.push(OP_Node(left, curr_token.t_type, right))

				else:  # if 0 or 1 num on stack
					raise Exception("Atleast 2 numbers on stack required to perform calculation")

			self.advancePos()

		return Execute_buffer



class Interpreter(Position):
	def __init__(self, Execute_buffer) -> None:
		super().__init__(len(Execute_buffer))
		self.__Exec_buff = Execute_buffer

		self.__operations = {"MINUS": self.MINUS,
					  "PLUS" : self.PLUS,
					  "MUL"  : self.MUL,
					  "DIV"  : self.DIV}

	def MINUS(self, left, right): return left - right

	def PLUS(self, left, right) : return left + right
	
	def MUL(self, left, right)  : return left * right
	
	def DIV(self, left, right):
		if right != 0: return left / right
		else: raise Exception("Division by Zero")


	def solve_operation_node(self, curr_op_node: OP_Node):

		if type(curr_op_node.left) == TOKEN and type(curr_op_node.right) == TOKEN:  # if evaluation possible
			return self.__operations[curr_op_node.op_type](curr_op_node.left.t_value, curr_op_node.right.t_value)  # breaking clause

		# Keep calling function until both branches are numbers
		if type(curr_op_node.left) == OP_Node and type(curr_op_node.right) == TOKEN:
			return self.__operations[curr_op_node.op_type](self.solve_operation_node(curr_op_node.left), curr_op_node.right.t_value)

		if type(curr_op_node.left) == TOKEN and type(curr_op_node.right) == OP_Node:
			return self.__operations[curr_op_node.op_type](curr_op_node.left.t_value, self.solve_operation_node(curr_op_node.right))

		if type(curr_op_node.left) == OP_Node and type(curr_op_node.right) == OP_Node:
			return self.__operations[curr_op_node.op_type](self.solve_operation_node(curr_op_node.left), self.solve_operation_node(curr_op_node.right))


	def run(self):

		for _, instruction in enumerate(self.__Exec_buff):  # look over each output instruction
			
			if type(instruction) == OUTPUT_Node: 

				if type(instruction.branch) == TOKEN:  # outputting a number
					if instruction.branch.t_type in [INT, FLOAT]: print(instruction.branch.t_value)

				elif instruction.branch == None: raise Exception("Not outputting anything")

				else:  # is an operation
					result = self.solve_operation_node(instruction.branch)
					if result: print(result)

			else:
				raise Exception("Somehow instruction is not of type OUTPUT_NODE")


def main(text, show_stages):

	if text:
		lexer = Lexer(text.strip())
		tokens = lexer.lex()

		parser = Parser(tokens)
		parse_tree = parser.parse()

		if show_stages:
			print("Tokens:", tokens)
			print("Tree:", parse_tree)

		translate = Interpreter(parse_tree)
		translate.run()


if __name__ == "__main__":

	show_stages = False
	if len(sys.argv) == 1:  # run command line interpreter
		while True:
			text = input(">>> ")

			if text == ":show_stages": show_stages = True if not show_stages else False
			else: main(text, show_stages)

	else:
		raise Exception("No external parameters accepted")
