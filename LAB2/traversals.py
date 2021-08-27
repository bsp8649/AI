"""
CSCI-603: Trees (week 10)
Author: Sean Strout @ RIT CS

This is an implementation of three recursive traversals
(preorder, inorder, postorder, on a binary tree composed of BTNode's.
"""

from btnode import BTNode

def preorder(node):
	"""
	A preorder traversal has a visitation order of parent,
	left and then right.
	:param node: The current node in the traversal (BTNode)
	:return: None
	"""
	if node != None:
		print(node.val, end=' ')
		preorder(node.left)
		preorder(node.right)

def inorder(node):
	"""
	An inorder traversal has a visitation order of left,
	parent and then right.
	:param node: The current node in the traversal (BTNode)
	:return: None
	"""
	if node != None:
		inorder(node.left)
		print(node.val, end=' ')
		inorder(node.right)

def postorder(node):
	"""
	A postorder traversal has a visitation order of left,
	right and then parent.
	:param node: The current node in the traversal (BTNode)
	:return: None
	"""
	if node != None:
		postorder(node.left)
		postorder(node.right)
		print(node.val, end=' ')

def traverse(node):
	"""
	A function that performs all three traversals
	:param node: The root of the tree (BTNode)
	:return: None
	"""
	print('Traversing...')
	print('preorder:', end= ' ')
	preorder(node)
	print()
	print('inorder:', end= ' ')
	inorder(node)
	print()
	print('postorder:', end= ' ')
	postorder(node)
	print()

def testTraversals():
	"""
	A function to test the traversals over different binary trees.
	:return: None
	"""
	# single node
#	traverse(BTNode(10))

	# A parent node (20), with left (10) and right (30) children
#	traverse(BTNode(20, BTNode(10), BTNode(30)))

	# from lecture notes: tree.png
	root = BTNode('A',
			BTNode('B',
				   None,
				   BTNode('D')),
			BTNode('C',
				   BTNode('E',
						  BTNode('G'),
						  None),
				   BTNode('F',
						  BTNode('H'),
						  BTNode('I'))))
	traverse(root)

if __name__ == '__main__':
	testTraversals()
