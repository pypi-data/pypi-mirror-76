"""
Element-wise elementary arithmetic operations for sequence types
"""
import builtins, math
from itertools import zip_longest
from typing import TypeVar, Union, List, Tuple, Iterable

_Num = Union[int, float, complex]

def negation(operand: Iterable[_Num])->Iterable[_Num]:
	"""
	Roughly, returns the additive inverse of the provided operand. 
	More specifically, returns a structure that is the same type as the operand,
	(if the result of the negation can be cast to that type through a constructor),
	but with each element the result of taking the additive inverse of the operand's
	same-indexed element.

	Example:

	negation([1, 2, 1j]) -> [-1, -2, (-0-1j)]
	(Python's result for -(1j) is an artifact of how it handles floats)

	Args:

	operand (iterable of numbers): The structure to iteratively additively invert,
	and whose type to format the output as
	"""

	#Negate each element of the operand generatively
	negated = (-x for x in operand)

	#Ensure the type of the result matches the operand's
	if type(negated)!=type(operand):
		try:
			negated = type(operand)(negated)
		except TypeError:
			pass
	return negated

def reciprocal(operand: Iterable[_Num])->Iterable[_Num]:
	"""
	Roughly, returns the multiplicative inverse of the provided operand.
	More specifically, returns a structure that is the same type as the operand,
	(if the reciprocal can be cast to that type through a constructor),
	but with each element the result of taking the multiplicative inverse of the operand's
	same-indexed element.

	Example:

	negation([1, -4, 1-2j]) -> [1.0, -0.25, (0.2+0.4j)]
	(Python's result for -(1j) is an artifact of how it handles floats)

	Args:

	operand (iterable of numbers): The structure to iteratively additively invert,
	and whose type to format the output as
	"""

	#Negate each element of the operand generatively
	reciprocal = (1/x for x in operand)

	#Ensure the type of the result matches the operand's
	if type(reciprocal)!=type(operand):
		try:
			reciprocal = type(operand)(reciprocal)
		except TypeError:
			pass
	return reciprocal

def sum(augend: Iterable[_Num], *addends : Iterable[_Num]) -> Iterable[_Num]:
	"""
	Returns a structure that is the same type of the augend
	(if the reciprocal can be cast to that type through a constructor), but with the
	*addends added element-wise sequentially to it. Returns just the augend
	if no other parameters are given.

	Example:
	
	sum([1, 2], (3, 1j, 6), (0, 1)) -> [4, (3+1j)]

	Args:

	augend: (iterable of numbers): The structure to be added to, and whose type
	to format the output as

	addends: (iterables of numbers): The sequences of numbers to sequentially
	add to the augend elementally for each of the augend's elements
	"""

	#Sequentially adds the members of addends to augend
	#zipped = zip_longest(augend, *addends, fillvalue=0)
	zipped = zip(augend, *addends)
	summed = (builtins.sum(x) for x in zipped)

	#Ensure the type of the result matches the augend's
	if type(summed)!=type(augend):
		try:
			summed = type(augend)(summed)
		except TypeError:
			pass
	return summed

def difference(minuend: Iterable[_Num], subtrahend: Iterable[_Num]) -> Iterable[_Num]:
	"""
	Returns a structure that is the same type as the minuend
	(if the difference can be cast to that type through a constructor),
	but with the subtrahend subtracted element-wise from it. Returns just the minuend
	if no other parameters are given.

	Example:
	
	difference([1, 2], (3, 1j, 6)) -> [-2, (2-1j)]

	Args:

	minuend: (sequence of numbers): The structure to be subtracted from, and whose type
	to format the output as

	subtrahend: (sequences of numbers): The sequence of numbers to subtract
	element-wise from the minuend for each of the minuend's elements
	"""
	return sum(minuend, negation(subtrahend))

def product(multiplier: Iterable[_Num], 
			*multiplicands : Iterable[_Num]) -> Iterable[_Num]:
	"""
	Returns a structure that is the same type of the multiplier
	(if the product can be cast to that type through a constructor), but with
	the multiplicands multiplied element-wise sequentially by it. Returns just the 
	multiplier if no other parameters are given.

	Example:
	
	product([1, 2], (3, 1j, 6), (0, 1)) -> [0, 2j]

	Args:

	multiplier: (sequence of numbers): The structure by which to sequentially
	multiply the multiplicands, and whose type to format the output as

	multiplicands: (sequences of numbers): The sequences of numbers to 
	sequentially multiply by the multiplier elementally for each of the multiplier's
	elements
	"""

	#Sequentially multiplies by the multiplier (or the previous multiplication
	#	result) the multiplicands
	zipped = zip(multiplier, *multiplicands)
	multiplied = (math.prod(x) for x in zipped)

	#Ensure the type of the result matches the multiplier's
	if type(multiplied)!=type(multiplier):
		try:
			multiplied = type(multiplier)(multiplied)
		except TypeError:
			pass
	return multiplied

def quotient(dividend: Iterable[_Num], divisor: Iterable[_Num]) -> Iterable[_Num]:
	"""
	Returns a structure that is the same type of the dividend
	(if the quotient can be cast to that type through a constructor), but with the
	each element divided element-wise by those of the divisor. Returns just the dividend
	if no other parameters are given.

	Example:
	
	quotient([1, 2], (3, 1j, 6)) -> [0.3333333333333333, -2j]

	Args:

	dividend: (sequence of numbers): The structure to be divided from, and whose type
	to format the output as

	divisor: (sequences of numbers): The sequence of numbers to divide
	element-wise the dividend by for each of the the dividend's elements
	"""
	return product(dividend, reciprocal(divisor))

# Unimplemented - decisions need to be made between %, fmod, and IEEE 754 remainder,
#    as well as complex numbers.
# def remainder(dividend: Iterable[_Num], divisor: Iterable[_Num]) -> Iterable[_Num]:
# 	"""
# 	Returns a structure that is the same type/shape of the dividend, but with the
# 	each element the remainder of dividing the dividend by the divisor element-wise.
# 	Returns a structure of zeros if the dividend is the only element that is given.

# 	Example:
	
# 	remainder([1, 2], (3, 1j, 6)) -> [-2, (2-1j)]

# 	Args:

# 	dividend: (sequence of numbers): The structure to be divided from, and whose type
# 	to format the output as

# 	divisor: (sequences of numbers): The sequence of numbers to divide
# 	element-wise the dividend by for each of the the dividend's elements
# 	"""
# 	zipped = zip(dividend, divisor)
# 	remainder = (math.fmod(dividend, divisor) for dividend, divisor in zipped)
# 	#Ensure the type of the result matches the dividend's
# 	if type(remainder)!=type(dividend):
# 		remainder = type(dividend)(remainder)
# 	return remainder