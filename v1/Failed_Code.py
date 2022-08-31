# if len(sys.argv) > 1:
#     file_information = open(sys.argv[1], "r")
#     text = file_information.read()
#     text = text.strip()  # remove trailing spaces
#     lexer = Lexer(text)
#     tokens = lexer.lex()
#     parser = Parser(tokens)
#     tokens = parser.parse()
#     translate = Interpreter(tokens)
#     translate.run()






# if curr_token.t_type == "PUSH":
# 	if self.__Tokens[self.pos-1].t_type in [INT, FLOAT]:
# 		Execute_buffer.append(PUSH_Node(self.__Tokens[self.pos-1]))
# 	else:
# 		raise SyntaxError("Push Comm not following a number")





# class PUSH_Node:
# 	def __init__(self, value):
# 		self.value = value

# 	def __repr__(self) -> str:
# 		return f'PUSH({self.value})'






# class Parser(Position):
# 	def __init__(self, token_str) -> None:
# 		super().__init__(len(token_str))
# 		self.__Tokens = token_str

# 	def parse(self):
		
# 		while not self.finished:
# 			curr_token = self.__Tokens[self.pos]

# 			if curr_token.t_type == INT:
# 				if self.advancePos(True):
# 					if self.__Tokens[self.pos+1].t_type == "PUSH":
# 						self.advancePos()
# 					else:
# 						raise Exception("Syntax Error: No push token")
# 				else:
# 					raise Exception("Syntax Error: No push token")


# 			elif curr_token.t_type == "PUSH":
# 				raise Exception("Syntax Error: Push token without number")

# 			self.advancePos()

# 		for idx, token in enumerate(self.__Tokens):
# 			if token.t_type == "PUSH":
# 				del self.__Tokens[idx]

# 		return self.__Tokens





# for idx, token in enumerate(token_str):
# 	if token.t_type == "PUSH":
# 		del token_str[idx]





# def build_statement(self, Exec_order, n):
# 	print(f'{n}: {self.stack} - {Exec_order}')

# 	if type(Exec_order) == OP_Node:
# 		self.stack.push(self.build_statement(Exec_order.left, n+1))
# 		self.stack.push(self.build_statement(Exec_order.right, n+1))

# 		match Exec_order.op_type:
# 			case "PLUS":
# 				self.PLUS()
# 				return
# 			case "MINUS":
# 				self.MINUS()
# 				return
# 			case "MUL":
# 				self.MUL()
# 				return
# 			case "DIV":
# 				self.DIV()
# 				return

# 	elif type(Exec_order) == TOKEN:
# 		return Exec_order.t_value

# 	elif type(Exec_order) == OUTPUT_Node:
# 		self.stack.push(self.build_statement(Exec_order.branch, n+1))
# 		#print(self.stack)

# 	# elif type(Exec_order) == PUSH_Node:
# 	# 	self.stack.push(Exec_order.value)

# 	else:
# 		print(type(Exec_order))


# def run(self):
    
# 	while not self.finished:
# 		curr_exec = self.__Exec_buff[self.pos]

# 		self.build_statement(curr_exec, 0)

# 		#for i in range(self.stack.length()): self.stack.pop()
# 		#print(self.stack)

# 		self.advancePos()