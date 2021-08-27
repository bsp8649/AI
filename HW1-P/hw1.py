from collections import deque
import sys

def wordChain(dictionary, startWord, endWord):
    wordList = []
    queue = deque()
    queue.append(startWord)
    if(startWord != endWord):
        dictionary.remove(startWord)
    x = len(queue)
    while queue:
        for i in range(x):
            current = [j for j in queue.popleft()]
            wordList.append("".join(current))
            for letter in range(len(startWord)):
                xLet = current[letter]
                for k in range(ord('a'), ord('z')+1):
                    current[letter] = chr(k)
                    if ("".join(current) == endWord):
                        wordList.append(endWord)
                        return wordList
                    if("".join(current)not in dictionary):
                        continue
                    else:
                        dictionary.remove("".join(current))
                    queue.append("".join(current))
                current[letter] = xLet
    print("No Solution")
    return []



if __name__ == '__main__':
    wordFile = open(sys.argv[1], "r")
    allWords = []
    for line in wordFile:
        line = line.strip()
        allWords.append(line)
    wordFile.close()
    start = sys.argv[2]
    end = sys.argv[3]
    wordList = wordChain(allWords, start, end)
    for word in wordList:
        print(word)
