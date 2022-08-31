class Stack:
	def __init__(self, size):
		self.__size = size
		self.__data = []

	def __repr__(self):
		return f'Stack: {self.__data}'

	def push(self, value):
		if not self.isFull(): self.__data.insert(0, value)
		else: raise Exception (f'Stack Full :: {value}')

	def pop(self):
		value = self.__data[0]
		if not self.isEmpty(): del self.__data[0]
		else: print("Stack is Empty")
		return value

	def peek(self):
		return self.__data[0] if not self.isEmpty() else None

	def isEmpty(self):
		return True if len(self.__data) == 0 else False

	def isFull(self):
		return True if len(self.__data) == self.__size else False

	def length(self):
		return len(self.__data)
