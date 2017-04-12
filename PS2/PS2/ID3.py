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
		return default

	#set up refernces to first congressman
	firstPerson = examples[0]
	affiliation = firstPerson[Class]
	AllSameClass = True
	
	AllSameAttVector = True	
	AttributeVector = firstPerson.values()
	AttributeVector.remove(firstPerson[Class])
	
	for congressman in examples:
		
		#if affiliation of current iteration is different from last
		if(AllSameClass and congressman[Class] != affiliation):
			AllSameClass = False
			
		#if attribute vectors have all been the same so far
		if(AllSameAttVector):
			
			#attribute vector is dict.values without Class value
			currentAttributeVector = congressman.values()
			currentAttributeVector.remove(congressman[Class])

			#if attribute vector differs			
			if(AttributeVector != currentAttributeVector):				
				AllSameAttVector = False
				
			#else increase appropriate counters
			else:
				if(congressman[Class] == "democrat":
					demos+=1
				else:
					repubs+=1		
		
#if examples all the same classification return it			
	if(AllSameClass):
		return affiliation

	
#if all examples have the same attribute vector return most common class
	elif(AllSameAttVector):
		if(demos >= repubs)
			return "democrat"
		else
			return "republican"
	
 

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


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
