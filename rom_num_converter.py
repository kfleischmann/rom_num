#!/usr/bin/env python

################################### LICENSE ####################################
#
# Copyright (C) 2014 Fleischmann, Kay
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################ DOCUMENTATION #################################
# RULE BASED DECIMAL TO ROMAN CONVERTER
#
# This converter takes an decimal number and converts it to an roman numeral.
#
# first step convert the decimal number to roman numeral without a subtraction rule
# second inner loop try to apply the subtraction rule
#
################################################################################


from itertools import repeat
import mark_pilgrim_roman_converter as t

# helper: repeat a specific string n-times
def rep(s,n):
	return ''.join(list(repeat(s,n)))

# helper: takes the first element of a list
def head(xs): return xs[0]

#Define exceptions
class RomanError(Exception): pass
class OutOfRangeError(RomanError): pass
class NotIntegerError(RomanError): pass
class InvalidRomanNumeralError(RomanError): pass

# helper: executes an flatten operator on a list
def flatten(A):
	rt = []
	for i in A:
		if isinstance(i,list):
			rt.extend(flatten(i))
		else:
			rt.append(i)
	return rt


#define digit mapping (character, decimal-representation, subtraction-rule )
roman_dictionary = (('M', 1000, ()),
					('D', 500, ()),
					('C', 100, ('D', 'M')),
					('L', 50, ()),
					('X', 10, ('L', 'C')),
					('V', 5, ()),
					('I', 1, ('V', 'X')))


# construct subtraction rule space (x,y,z) => e.g (III => IV, order)
def subtraction_rules():
	def find_rule(ch):
		return head(filter(lambda x: x[0] == ch, roman_dictionary))
	def roman_digit(ch):
		return find_rule(ch)[1]
	replacements = \
		flatten(map(lambda x: [(rep(x[0],4), x[0]+x[2][0], roman_digit(x[2][0]) ), ( x[2][0]+rep(x[0],4), x[0]+x[2][1], roman_digit(x[2][1])) ],
			   filter( lambda a: len(a[2])>0,roman_dictionary) ))
	# replace priority
	return sorted(replacements, key=lambda x: x[2], reverse=True)


# convert decimal number to roman numerials
def to_roman(n, ignore_substraction=False):
	"""convert integer to Roman numeral"""
	if not (0 < n < 4000):
		raise OutOfRangeError, "number out of range (must be 1..3999)"
	if int(n) != n:
		raise NotIntegerError, "decimals can not be converted"

	roman=''
	for digit, ch in enumerate(str(n)):
		exp = int(len(str(n))-digit-1)
		decimal = int(ch)*pow(10, exp)
		rules = subtraction_rules()
		while(decimal>0):
			# find the best one suitable
			r=head(filter(lambda (r_ch, r_val, f): r_val <= decimal, roman_dictionary))
			# do the transformation
			decimal = decimal - r[1]
			roman += r[0]
			# try to apply rules if possible
			if not ignore_substraction:
				for r in rules:
					roman = roman.replace(r[0], r[1])
	return roman


# test the code
def test():
	errors=0
	for x in range(1,3999):
		r1=t.toRoman(x)
		r2=to_roman(x)
		if r1!=r2:
			errors+=1
			print "error convert "+str(x)+" to roman number "+r1+" "
	if errors == 0:
		return True
	else:
		return False

# main Code
if __name__ == "__main__":
	if test():
		print "test succeed"
	else:
		print "test failed"
	print "1984 => " + to_roman(1984,True) + " (no substraction rule)"
	print "1984 => " + to_roman(1984)
	print "3991 => " + to_roman(3991)
	print "399 => " + to_roman(399)
