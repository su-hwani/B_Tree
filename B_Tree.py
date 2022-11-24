class Node : 
    def __init__(self) :
        self.K = []
        self.n = 0
        self.P = []
    
class B_Tree : 
    def __init__(self) : 
        return None 
    
    def insertBT(self, T, m, newKey) : 
        if T == None : 
            T = self.getNode() 
            T.K[1] = newKey 
            T.n = 1
            return 
        
        found, stack = self.serachPath(T, m, newKey, None)
        if found == True : 
            return 
        
        pass 
    
    def serachPath(self, T, m, key, stack) : 
        if (stack == None) or (len(stack) == 0) : 
            stack = []
        self.x = T 
        
        while True : 
            i = 1 
            while ((i <= self.x.n) and (key > self.x.K[i])) : 
                i += 1
            if (i <= self.x.n) and (key == self.x.K[i]) : 
                return True, stack
            stack.append(self.x) 
            self.x = self.x.P[i-1]
            if self.x != None : 
                continue
            break 
        
        return False, stack 
    
    def insertKey(self, T, m, x, y, newKey) : 
        pass 
    
    def splitNode(self, T, m, x, y, newKey) : 
        pass 
    
    def getNode(self) : 
        return Node() 
        
    
    
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
    def inorderBT(self, m) : 
        pass 
        
        
        
    