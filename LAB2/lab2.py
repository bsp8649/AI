#Lab 2 for Class CSCI 331 Intro to Artificial Intellegence
#Brett Peters

import math
import random
import sys
import pickle

class Tree:
    def ___init__(self, data):
        self.left = None
        self.right = None
        self.data = data

class Example:
    def __init__(self):
        self.lang = None
        self.words = []
        self.weight = 1

# For the purposes of testing if the averages of words have 5 or more letters.
def attriWL5(words):
    sum = 0
    for word in words:
        sum += len(word)
    if (sum/float(len(words)) > 5):
        return True
    return False

# For the purposes of testing if the word contains a letter)
def attriQ(words):
    for word in words:
        word = word.lower()
        for w in range(0, len(word)):
            if word[w] == 'q':
                return True
    return False

def attriE(words):
    for word in words:
        word = word.lower()
        for w in range(0, len(word)):
            if word[w] == 'e':
                return True
    return False

def attriThe(words):
    for word in words:
        word = word.lower()
        if word == "the":
            return True
    return False

def attriA(words):
    for word in words:
        word = word.lower()
        if word == "a":
            return True
    return False

def attriDe(words):
    for word in words:
        word = word.lower()
        if word == "de":
            return True
    return False

def attriEen(words):
    for word in words:
        word = word.lower()
        if word == 'een':
            return True
    return False

def attri2w(words):
    count = 0
    for word in words:
        word = word.lower()
        if word[0] == 'w':
            count += 1
            if count > 1:
                return True
    return False


def entropy(ptrue):
    pfalse = 1 - ptrue
    if ptrue == 0 or pfalse == 0:
        return 0
    else:
        etrue = ptrue * math.log2(ptrue)
        efalse = pfalse * math.log2(pfalse)
        return -1 * (etrue + efalse)

def importance(a, examples):
    true_count = 0
    count = 0
    for example in examples:
        if a(example.words) == True:
            true_count += 1
        count += 1
    prob = true_count/float(count) #probability that variable is true
    b = entropy(prob) #entropy of boolean random variable
    remain = remainder(a, examples)
    return b - remain

def remainder(a, examples):
    trues = []
    falses = []
    for e in examples:
        if a(e.words):
            trues.append(e)
        else:
            falses.append(e)
    pk = 0
    nk = 0
    pj = 0
    nj = 0
    for f in trues:
        if f.lang == "en":
            pk += f.weight
        else:
            nk += f.weight
    for f in falses:
        if f.lang == "en":
            pj += f.weight
        else:
            nj += f.weight
    p = pk + pj
    n = nk + nj
    if (p + n) > 0 and (pk+nk) > 0:
        first = ((pk + nk)/(p + n)) * entropy(pk/(pk+nk))
    else:
        first = 0
    if (p + n) > 0 and (pj+nj) > 0:
        second = ((pj + nj)/(p + n)) * entropy(pj/(pj+nj))
    else:
        second = 0
    return (first + second)


def repeated(examples):
    firstex = examples[0]
    language = firstex.lang
    for e in examples:
        if e.lang != language:
            return False
    return True

def plurality(examples):
    en = 0
    nl = 0
    for e in examples:
        if e.lang == "en":
            en += e.weight
        else:
            nl += e.weight
    if en > nl:
        return "en"
    elif nl > en:
        return "nl"
    else:
        rand = random.randint(0, 1)
        if rand == 0:
            return "en"
        else:
            return "nl"

def decisionTree(examples, attributes, parent_examples):
    root = Tree()
    if len(examples) == 0:
        root.data = plurality(parent_examples)
        root.left = None
        root.right = None
        return root
    elif repeated(examples):
        root.data = examples[0].lang
        root.left = None
        root.right = None
        return root
    elif len(attributes) == 0:
        root.data = plurality(examples)
        root.left = None
        root.right = None
        return root
    else:
        impA = 0 #importance of A
        attri = attributes[0] #Attribute to be tested
        for a in attributes:
            impor = importance(a, examples)
            if impor > impA:
                impA = impor
                attri = a
        root.data = attri
        trues = []
        falses = []
        for e in examples:
            if attri(e.words):
                trues.append(e)
            else:
                falses.append(e)
        attributes.remove(attri)
        root.left = decisionTree(trues, attributes[:], examples)
        root.right = decisionTree(falses, attributes[:], examples)
    return root

def adaboost(examples, attributes):
    bigK = 50
    h = [None] * bigK
    z = [None] * bigK
    bigN = (len(examples))
    weight = 1/float(bigN)
    for e in examples:
        e.weight = weight
    for k in range(0, bigK):
        h[k] = decisionTree(examples, attributes, None)
        err = 0
        for j in range(1, bigN):
            etree = h[k]
            e = examples[j]
            while (etree.data != "en" and etree.data != "nl"):
                attri = etree.data
                if attri(e.words):
                    left = etree.left
                    etree = left
                else:
                    right = etree.right
                    etree = right
            if(etree.data != e.lang):
                err = err + e.weight
        for f in range(1, bigN):
            etree = h[k]
            e = examples[f]
            while (etree.data != "en" and etree.data != "nl"):
                attri = etree.data
                if attri(e.words):
                    left = etree.left
                    etree = left
                else:
                    right = etree.right
                    etree = right
            if(etree.data == e.lang):
                e.weight = float(e.weight) * err/(1-err)
        wMax = examples[0].weight
        wMin = examples[0].weight
        for e in examples:
            if e.weight > wMax:
                wMax = e.weight
            if e.weight < wMin:
                wMin = e.weight
        for e in examples:
            e.weight = (e.weight - wMin)/(wMax - wMin)
        if(1-err) > 0:
            z[k] = math.log(1- err)/err
        else:
            z[k] = -10000
    bestZ = z[0]
    bestK = 0
    for n in range(1, bigK):
        if z[n] > bestZ:
            bestK = n
    return h[bestK]


def printTree(tree, n):
    if tree.left:
        printTree(tree.left, n+1)
    print(tree.data, n)
    if tree.right:
        printTree(tree.right, n+1)

def readTrain(trainFile):
    examples = []
    for line in trainFile:
        line = line.rstrip()
        texts = line.split(" ")
        words = []
        lang, word = texts[0].split('|')
        example = Example()
        example.lang = lang
        words.append(word)
        for w in range(1, len(texts)):
            words.append(texts[w])
        example.words = words
        examples.append(example)
    return examples

def train(trainFile, hypothesisOut, learningType):
    examples = readTrain(trainFile)
    attributes = [attriWL5, attriQ, attriE, attriThe, attriA, attriDe, attriEen, attri2w]
    if learningType == "dt":
        tree = decisionTree(examples, attributes, None)
        pickle.dump(tree, open(hypothesisOut, "wb"))
        return hypothesisOut
    elif learningType == "ada":
        tree = adaboost(examples, attributes)
        pickle.dump(tree, open(hypothesisOut, "wb"))
    else:
        print("Invald Type")
        return
    return hypothesisOut

def readPredict(predictFile):
    examples = []
    for line in predictFile:
        line = line.rstrip()
        texts = line.split(" ")
        example = Example()
        example.lang = None
        example.words = texts
        examples.append(example)
    return examples

def predict(hypothesis, predictFile):
    tree = pickle.load(open(hypothesis, "rb"))
    examples = readPredict(predictFile)
    for e in examples:
        etree = tree
        while (etree.data != "en" and etree.data != "nl"):
            attri = etree.data
            if attri(e.words):
                left = etree.left
                etree = left
            else:
                right = etree.right
                etree = right
        print(etree.data)
    return

def main():
    if sys.argv[1] == "train":
        trainFile = open(sys.argv[2], "r")
        hypothesis = sys.argv[3]
        learnType = sys.argv[4]
        hypoFile = train(trainFile, hypothesis, learnType)
        trainFile.close()
    elif sys.argv[1] == "predict":
        hypoFile = sys.argv[2]
        predictFile = open(sys.argv[3], "r")
        predict(hypoFile, predictFile)
        predictFile.close()
    return

if __name__ == "__main__":
    main()

