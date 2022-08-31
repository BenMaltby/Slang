import os


class MissingFile:
	def __init__(self, fn) -> None:
		self.fn = fn

	def __repr__(self) -> str:
		return f'{os.getcwd()} - Cannot find file named {self.fn}'


class IncorrectFileExtension:
	def __init__(self, fn) -> None:
		self.fn = fn
	
	def __repr__(self) -> str:
		return f'The file "{self.fn}" needs extension of type ".afl"'