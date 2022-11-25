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
                    #########
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
        
        
        pass 
    
    def serachPath(self, T, m, key, stack) : 
        if (stack == None) or (len(stack) == 0) : 
            stack = []
        self.x = T 
        
        while True : 
            i = 0
            while ((i <= self.x.n) and (key > self.x.K[i])) : 
                i += 1
            if (i <= self.x.n) and (key == self.x.K[i]) : 
                return True, stack
            stack.append(self.x) 
            self.x = self.x.P[i-1]
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
        self.x.P[i+1] = self.y 
        self.x.n = self.x.n+1
        
        return 
    
    def splitNode(self, T, m, x, y, newKey) : 
        
        self.insertKey(T, m, x , y, newKey)
        self.tempNode = copy.deepcopy(self.x)
        self.centerKey = self.tempNode.K[self.tempNode.n // 2 ]
        
        ##
        self.x = self.getNode(m)
        self.x.n = 0 
        i = 0
        
        
        while(self.tempNode.K[i] < self.centerKey) : 
            self.x.K[i] = self.tempNode.K[i]
            self.x.P[i-1] = self.tempNode.P[i-1]
            i += 1
            self.x.n += 1
        self.x.P[i-1] = self.tempNode.P[i-1]
        
        self.newNode = self.getNode(m)
        i += 1
        
        ### 여기 로직 다시 짜야할 듯
        q = 0 
        while(i < self.tempNode.n) : 
            self.newNode.K[q] = self.tempNode.K[i]
            self.newNode.P[q-1] = self.tempNode.P[i-1]
            i += 1
            self.newNode.n += 1
            
        self.newNode.P[i-1] = self.tempNode.P[i-1]
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
        i = 0
        while True :
            if T == None or i == m : 
                return 
            if T.P[i] != 0 : 
                self.inorderBT(T.P[i], m)
            print(f"{T.K[i]} -> ")
            i += 1
            
        
            
        
        
        
    
    

Test = B_Tree()
Test.insertBT(Test, 3, 1)
Test.insertBT(Test, 3, 2)
Test.insertBT(Test, 3, 3)
Test.insertBT(Test, 3, 4)
a = 2