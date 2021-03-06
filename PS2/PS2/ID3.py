from node import Node
import math, copy
	
def ID3(examples,default):
# if examples are empty, return a Node with label default
 	if not examples:
 		ret = Node()
 		ret.label = default
 		return ret

 	# Use first example to check if all are same

 	first = examples[0]
 	allSameClass = True
 	allSameAttVector = True
 	attributeVector = first.copy()
 	attributeVector.pop("Class")

 	classCounts = {}

 	# tracks if all examples are the same Class
 	for example in examples:
 		if (allSameClass and example["Class"] != first["Class"]):
 			allSameClass = False

 		#if attribute vectors have all been the same so far
 		if(allSameAttVector):
 			currentAttributeVector = example.copy()
 			currentAttributeVector.pop("Class")

 			# check if attribute vector is different
 			for key in attributeVector:
 				if (key in currentAttributeVector):
 					if (attributeVector[key] != currentAttributeVector[key]):
 						allSameAttVector = False
 				else:
 					allSameAttVector = False

 		# Track how many of each class there are
 		if example["Class"] in classCounts:
 			classCounts[example["Class"]] += 1
 		else:
 			classCounts[example["Class"]] = 1

 	# Set mode to highest occurence of Class attribute. Max is the number of occurences
 	max = 0
 	for key in classCounts:
 		if classCounts[key] > max:
 			mode = key
 			max = classCounts[key]

 	# if examples are all the same classification return, return it
 	if (allSameClass):
 		ret = Node()
 		ret.label = examples[0]["Class"]
 		return ret


 	# if all examples have the same attribute vector, return the most common class
 	if (allSameAttVector):
 		ret = Node()
 		ret.label = mode
 		return ret

 	# Branch on best attribute
 	best = ChooseAttribute(examples)

 	#decision tree with best as root
 	tree = Node()
 	tree.label = best
 	tree.modeResponse = getModeResponse(examples, best)

 	# bestVals has a key for each value of best
 	# and holds examples where example[best] = key
 	bestVals = {}
 	for example in examples:
 		# Adds each example ( - best ) to the appropriate bucket in bestVals
 		currentExample = example.copy()
 		if currentExample[best] not in bestVals:
 			currentExample.pop(best)
 			bestVals[example[best]] = [currentExample]
 		else:
 			currentExample.pop(best)
 			bestVals[example[best]].append(currentExample)

 	# add a child to root for each value of best
 	for val in bestVals:
 		subtree = ID3(bestVals[val], mode)
 		tree.children[val] = subtree

 	return tree
	
def markRoot(tree,root):
	tree.root = root
	if not tree.children:
		return tree
	for childKey in tree.children:
		markRoot(tree.children[childKey],root)
	return tree

def prune(node, examples):
	'''
	Takes in a trained tree and a validation set of examples.  Prunes nodes in order
	to improve accuracy on the validation data; the precise pruning strategy is up to you.
	'''
	return pruneRecurse(node,node,examples)
	
	
	
def pruneRecurse(root, node, examples):
	#Reduced Error Pruning Implementation
	
	#if current node is a leaf return it
	if not node.children:
		return node
	
	#prune children first
	for childKey in node.children:
		node.children[childKey] = pruneRecurse(root,node.children[childKey],examples)
	
	originalAccuracy = test(root,examples)
	
	#cache label and children
	label = node.label	
	children = node.children
	
	
	#make node a leaf
	node.label = getModeNode(node)
	node.children = {}
	
	
	#if the prunedTree is less accurate than the master tree restore children
	if(test(root, examples) < originalAccuracy):		
		node.label = label
		node.children = children
			
	#else return pruned node
	return node
	
def getModeNode(node):
	if not node.children:
		return node.label
	return getModeNode(node.children[node.modeResponse])

	
def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  num_correct = 0
  
  for example in examples:
    result = evaluate(node, example)
    num_correct += (result == example["Class"])

  return float(num_correct)/len(examples)


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

    if response not in node.children:
    	return evaluate(node.children[node.modeResponse], example)

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
        p = float(counts[key])/total_num
        e = p*math.log(p, 2)
        result -= p * e

    return result

# Gets the mode of responses to a given attribute
def getModeResponse(examples,attribute):
	# counts is a dictionary that holds the number of each result
    counts = {}
    for example in examples:
    	if example[attribute] not in counts:
    		counts[example[attribute]] = 1
    	else:
    		counts[example[attribute]] += 1

    mode = None
    max = 0

    for key in counts:
    	if counts[key] > max:
    		max = counts[key]
    		mode = key

    return mode