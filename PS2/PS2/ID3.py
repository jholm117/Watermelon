from node import Node
import math

def ID3(examples, default):
 '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
	

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  num_correct = 0
  total_num = len(examples)
  for example in examples:
  	result = evaluate(node, example)
  	num_correct += (result == example[Class])

  return num_correct/total_num


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''


def infoGain(xi, examples):
	# returns purity of xi

	result = 0
	
	# values is an array of the values of xi from each example
	values = [example[xi] for example in examples]
	total_num = len(values)

	# counts is a dictionary that holds the number of each result
	counts = {}
	for value in values:
		if value in counts:
			counts[value] += 1
		else:
			counts[value] = 1

	# info gain
	for key in counts:
		p = counts[key]/total_num
		e = p*math.log(p, 2)
		result -= p * e

	return result