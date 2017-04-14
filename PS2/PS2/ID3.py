from node import Node
import math

def ID3(examples, default):
 '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''

	#if examples empty 
	if not examples:
		ret = Node()
		ret.label = default
		return ret

	#set up refernces to first example
	firstPerson = examples[0]
	Class = firstPerson["Class"]
	allSameClass = True
	
	allSameAttVector = True	
	attributeVector = firstPerson.values()
	attributeVector.remove(firstPerson["Class"])
	
	# counts is a dictionary that holds the number of each Class
	ClassCounts = {}
	
	for example in examples:
		
		#if Class of current iteration is different from last
		if(allSameClass and example["Class"] != Class):
			allSameClass = False
			
		#if attribute vectors have all been the same so far
		if(allSameAttVector):
			
			#attribute vector is dict.values without Class value
			currentAttributeVector = example.values()
			currentAttributeVector.remove(example["Class"])
			
			#if attribute vector differs
			commonPairs = attributeVector.items() & currentAttributeVector.items()
			if(commonPairs.len() != attributeVector.len()):					
				allSameAttVector = False
			
		# increase count of each Class
		if example["Class"] in ClassCounts:
			ClassCounts[example["Class"]] += 1
		else:
			ClassCounts[example["Class"]] = 1	
				

	max =0
	#Set mode to highest occurence of Class attribute
	for key in ClassCounts:
		if ClassCounts[key] > max:
			mode = key
			max = ClassCounts[key]
	
	#if examples all the same classification return it			
	if(allSameClass):
		ret = Node()
		ret.label = Class
		return ret

	#if all examples have the same attribute vector return most common class
	elif(allSameAttVector):
		ret = Node()
		ret.label = mode
		return ret
			
	else:
		best = ChooseAttribute(examples)
		
		#decision tree with best as root
		tree = Node()		
		
		for v in ClassCounts :
			#elements of examples with best = value
			examples1 = []
			for example in examples:
			
				#if the example had the same response as v add them to examples1
				if (example[best] == v):
					examples1.append(example)
			
			subtree = ID3(examples1, mode)
			
			# add sub tree to root?
			tree.children[v] = subtree
			
		return tree
	

def prune(node, examples):
	'''
	Takes in a trained tree and a validation set of examples.  Prunes nodes in order
	to improve accuracy on the validation data; the precise pruning strategy is up to you.
	'''
	#Reduced Error Pruning Implementation
	
	#recursion end case: if leaf return 
	if not node.children:
		return node

	masterTree = node
	masterTreeAccuracy = test(node,examples)


	for child in masterTree.children:

		#if the child is not a leaf
		if masterTree[child].children:
			#copy masterTree to test pruned tree 
			prunedTree = masterTree
			
			#make child a leaf
			prunedTree[child].children = {}
			
			#test accuracy
			prunedAccuracy = test(prunedTree,examples)
			
			#update master tree if pruned tree is more accurate
			if(prunedAccuracy > masterTreeAccuracy):
				masterTree = prunedTree
				masterTreeAccuracy = prunedAccuracy
			
		#run prune on child
		masterTree.children[child] = prune(masterTree.children[child],examples)
	
	#return final pruned tree
	return masterTree

	
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
	#attribute the tree splits over
	attribute = node.label
	
	#if bottom of tree, return predicted Class
	if not node.children:
		return attribute
	
	# get response for attribute to split over
	response = example[attribute]
	
	#recurse til end of tree
	return evaluate(node.children[response],example)

# finds the best attribute based on infoGain
def ChooseAttribute(examples):
	best = (1000000000, None)
	for xi in examples[0]:
		if xi != "Class":
			ig = infoGain(xi, examples)
			if (ig < best[0]):
				best = (ig, xi)

	return best[1]


# returns purity of xi
def infoGain(xi, examples):
	result = 0
	
	# values is an array of the values of xi from each example
	values = [example[xi] for example in examples]
	total_num = len(values)

	# counts is a dictionary that holds the number of each result
	counts = {}
	for value in values:
		if value != "Class":
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