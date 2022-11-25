import copy
class Node : 
    def __init__(self, m) :
        self.K = [0 for _ in range(m)]
        self.n = 0
        self.P = [0 for _ in range(m+1)]
    
class B_Tree : 
    def __init__(self) : 
        self.root = None 
        return None 
    
    def insertBT(self, T, m, newKey) : 
        if self.root == None : 
            T = self.getNode(m) 
            T.K[0] = newKey 
            T.n = 1
            self.root = T 
            return self.root
        
        T = self.root 
        found, stack = self.serachPath(T, m, newKey, None)
        
        if found == True : 
            return self.root
        
        finished = False 
        self.x = stack.pop(-1)
        self.y = None 
        
        while True : 
            if self.x.n < m-1 : 
                self.insertKey(T, m, self.x, self.y, newKey) 
                finished = True 
            else : 
                newKey, self.y = self.splitNode(T, m, self.x, self.y, newKey)
                if len(stack) != 0 :
                    self.x = stack.pop(-1)
                else : 
                    T = self.getNode(m)
                    T.n = 1 
                    T.K[0] = newKey 
                    T.P[0] = self.x 
                    T.P[1] = self.y 
                    self.root = T 
                    finished = True 
            if finished == True : 
                break 
        return self.root 
    
    def serachPath(self, T, m, key, stack) : 
        if (stack == None) or (len(stack) == 0) : 
            stack = []
        self.x = T 
        
        while True : 
            i = 0
            
            while ((i < self.x.n) and (key > self.x.K[i])) : 
                i += 1
            if (i <= self.x.n) and (key == self.x.K[i]) : 
                return True, stack
            stack.append(self.x) 
            self.x = self.x.P[i]
            if self.x != 0 and self.x != None : 
                continue
            break 
        
        return False, stack 
    
    def insertKey(self, T, m, x, y, newKey) -> None : 
        i = self.x.n - 1 
        while ((i >= 0) and (newKey < self.x.K[i])) : 
            self.x.K[i+1] = self.x.K[i]
            self.x.P[i+2] = self.x.P[i+1]
            i = i-1
        self.x.K[i+1] = newKey 
        
        if self.y != None : 
            self.x.P[i+1] = self.relinkNode 
        self.x.P[i+2] = self.y 
        self.x.n = self.x.n+1
        return 
    
    def splitNode(self, T, m, x, y, newKey) : 
        self.insertKey(T, m, x , y, newKey)
        self.tempNode = copy.deepcopy(self.x)
        self.centerKey = self.tempNode.K[self.tempNode.n // 2 ]

        self.x = self.getNode(m)
        self.x.n = 0 
        i = 0
        
        while(self.tempNode.K[i] < self.centerKey) : 
            self.x.K[i] = self.tempNode.K[i]
            self.x.P[i] = self.tempNode.P[i]
            i += 1
            self.x.n += 1
        self.x.P[i] = self.tempNode.P[i]
        self.newNode = self.getNode(m)
        i += 1
        q = 0 
        
        while(i < self.tempNode.n) : 
            self.newNode.K[q] = self.tempNode.K[i]
            self.newNode.P[q] = self.tempNode.P[i]
            i += 1
            self.newNode.n += 1
            
        self.newNode.P[q+1] = self.tempNode.P[i]
        self.relinkNode = copy.deepcopy(self.x)
        return self.centerKey , self.newNode 
    
    def getNode(self, m) : 
        return Node(m) 
        
# ----------------------------------------------------------------
    def deleteBT(self, T, m, oldKey) : 
        pass 

    def deleteKey(self, T, m, x, oldKey) : 
        pass 
    
    def bestSibling(self, T, m, x, y) : 
        pass 
    
    def redistributeKeys(self, T, m, x, y, bestSibling) : 
        pass 
    
    def mergeNode(self, T, m, x, y, bestSibling) : 
        pass 
    
# ----------------------------------------------------------------
    def inorderBT(self, T, m) :
        pass
            
Test = B_Tree()
import random
numbers=[10,30,5,15,50,2,4,1]

'''
for i in range(1,100):
    number=random.randint(1,20)
    if number not in numbers : 
        numbers.append(number)
    if len(numbers) == 10 : 
        break 

'''

for i in numbers :
    Test.insertBT(Test,3,i)

pass 
