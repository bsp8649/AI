#Author: Brett Peters <bsp8649>
#HW2-P for class Intro to AI
import random
def swap(n1, n2, nums):
    temp = nums[n1]
    nums[n1] = nums[n2]
    nums[n2] = temp

def change(s1, op, ops):
    ops[s1] = op

def add(n1, n2):
    return n1 + n2

def subtract(n1, n2):
    return n1 - n2

def mult(n1, n2):
    return n1 * n2

def divide(n1, n2):
    if(n2 != 0):
        return n1 / float(n2)
    return n1

def randOps(ops):
    arith = ['+', '-', '*', '/']
    for i in range(0, len(ops) - 1): 
        num = random.randint(0, 3)
        ops[i] = arith[num]

def findTotal(nums, ops):
    total = nums[0]
    numindex = 0
    opindex = 0
    while opindex < (len(ops) - 1):
        if ops[opindex] == '+':
            total = add(total, nums[numindex + 1])
        if ops[opindex] == '-':
            total = subtract(total, nums[numindex + 1])
        if ops[opindex] == '+':
            total = mult(total, nums[numindex + 1])
        if ops[opindex] == '/':
            total = divide(total, nums[numindex + 1])
        numindex += 1
        opindex += 1
    return total

def mathString(nums, ops):
    line = ""
    numindex = 0
    opindex = 0
    while numindex < (len(nums) - 1):
        if(opindex < len(ops) - 1):
            line += (str(nums[numindex]) + str(ops[opindex]))
        else:
            line += str(nums[numindex])
        numindex += 1
        opindex += 1
    return line

def targetDistance(total, target):
    distance = total - target
    if (distance < 0):
        distance *= -1
    return distance

def printState(nums, ops, distance, flag):
    if flag == 0:
        print("S0 "+ str(mathString(nums, ops)))
    if flag == 1:
        print("Best State " + str(mathString(nums, ops)))
    print("Distance From Target "+ str(distance)+"\n")

def hillClimb(nums, ops, target):
    lowest = -1
    flag = 0
    randOps(ops)
    random.shuffle(nums)
    while(True):
        total = findTotal(nums, ops)
        distance = targetDistance(total, target)
        if distance == 0:
            print("Solution: "+mathString(nums, ops))
            break
        elif (lowest == -1) or (distance < lowest):
            lowest = distance
            printState(nums, ops, distance, flag)
            flag = 1
            mod = random.randint(0, 1)
            if mod == 0:
                r1 = random.randint(0, len(nums) - 1)
                r2 = random.randint(0, len(nums) - 1)
                while (r1 == r2):
                    r2 = random.randint(0, len(nums -1))
                swap(r1, r2, nums)
            if mod == 1:
                arith = ['+', '-', '*', '/']
                r1 = random.randint(0, 3)
                r2 = random.randint(0, len(ops) - 1)
                change(r2, arith[r1], ops)
        else:
            mod = random.randint(0, 1)
            if mod == 0:
                r1 = random.randint(0, len(nums) - 1)
                r2 = random.randint(0, len(nums) - 1)
                while (r1 == r2):
                    r2 = random.randint(0, len(nums) - 1)
                swap(r1, r2, nums)
            if mod == 1:
                arith = ['+', '-', '*', '/']
                r1 = random.randint(0, 3)
                r2 = random.randint(0, len(ops) - 1)
                change(r2, arith[r1], ops)
            continue

if __name__ == '__main__':
    nums = [3, 3, 7, 3, 3, 4, 6, 7, 3, 5, 8, 2, 7, 6, 4, 4, 1, 2, 2, 8, 3, 2, 3, 0, 2, 3, 3, 7, 7, 3, 2, 9, 0, 2, 0, 4, 3, 0, 2, 7, 1, 3, 7, 1, 7, 0, 7, 8, 4, 1, 9, 9, 2, 3, 5, 0, 4, 9, 1, 4, 6, 0, 1, 1, 4, 5, 1, 9, 7, 4, 5, 3, 7, 2, 9, 7, 2, 0, 1, 8, 1, 4, 3, 9, 3, 5, 3, 6, 6, 8, 9, 7, 7, 9, 4, 6, 7, 1, 6, 6]
    target = 3127
    ops = [''] *99
    print("Number Set: " + str(nums))
    print("Target: " + str(target))
    n = 1
    while(n <= 3):
        print("***************************************")
        print("RR Iteration: "+str(n))
        hillClimb(nums, ops, target)
