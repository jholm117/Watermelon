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
	affiliation = firstPerson["Class"]
	AllSameClass = True
	
	AllSameAttVector = True	
	AttributeVector = firstPerson.values()
	AttributeVector.remove(firstPerson["Class"])
	
	for congressman in examples:
		
		#if affiliation of current iteration is different from last
		if(AllSameClass and congressman["Class"] != affiliation):
			AllSameClass = False
			
		#if attribute vectors have all been the same so far
		if(AllSameAttVector):
			
			#attribute vector is dict.values without Class value
			currentAttributeVector = congressman.values()
			currentAttributeVector.remove(congressman["Class"])

			#if attribute vector differs			
			if(AttributeVector != currentAttributeVector):				
				AllSameAttVector = False
			
		# increase appropriate counters	
		if(congressman["Class"] == "democrat":
			demos+=1
		else:
			repubs+=1		
		
	#MODE
	if(demos >= repubs):
			MODE = "demos"
		else:
			MODE = "republican"
	
#if examples all the same classification return it			
	if(AllSameClass):
		return affiliation

	
#if all examples have the same attribute vector return most common class
	elif(AllSameAttVector):
		return MODE
			
	else:
		#attribute to split over
		best = ChooseAttribute()
		
		#decision tree with best as root
		tree = Node()
		tree.label = best
		
		#need to change this to work for general case
		indieVariables = ["y","n","?"]
		
		for v in indieVariables :
		
			#elements of examples with best = v
			examples1 = []
			for congressman in examples:
			
				#if the congressman had the same response as v add them to examples1
				if (congressman[best] == v):
					examples1.append(congressman)
			
			subtree = ID3(examples1, MODE)
			
			# add sub tree to root with v=key indicating branch to node of new attribute 
			tree.children[v] = subtree
			
		return tree

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
	if 
