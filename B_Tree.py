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
                stack.append(self.x) 
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
        q = 0 
        i += 1
        while(i < self.tempNode.n) : 
            self.newNode.K[q] = self.tempNode.K[i]
            self.newNode.P[q] = self.tempNode.P[i]
            i += 1
            q += 1
            self.newNode.n += 1
            
        self.newNode.P[q] = self.tempNode.P[i]
        self.relinkNode = copy.deepcopy(self.x)
        return self.centerKey , self.newNode 
    
    def getNode(self, m) : 
        return Node(m) 
        
# ----------------------------------------------------------------
    def deleteBT(self, T, m, oldKey) : 
        T = self.root 
        found, stack = self.serachPath(T, m, oldKey, None)
        if found == False : 
            return 
        self.internal_Node = stack[-1]
        self.x = stack.pop(-1)
        self.oldKey_index = -1
        is_internal_Node = False 
        
        # 내부노드에서 발견한 경우
        for i in range(0,len(self.x.P)) : 
            if (self.x.P[i] != 0) and (self.x.P[i] != None) : 
                is_internal_Node = True
        
        if is_internal_Node : 
            
            for i in range(0,len(self.internal_Node.K)) : 
                if self.internal_Node.K[i] == oldKey : 
                    self.oldKey_index = i
            
            found2, stack = self.serachPath(self.x.P[self.oldKey_index], m, self.x.K[self.oldKey_index], stack )
            
            self.x = stack.pop(-1)
            self.temp = self.internal_Node.K[self.oldKey_index]
            self.internal_Node.K[self.oldKey_index] = self.x.K[0]
            self.x.K[0] = self.temp
            
        finished = False 
        self.deleteKey(T, m, self.x, oldKey)
        
        if len(stack) != 0 : 
            self.y = stack.pop(-1)
            
        # 여기까지는 디버그 끝, 내부노드 or 말단노드에서 key 찾고 후행키와 교체하고 삭제하기 
        # 스플릿이나 머지 안했음 
        # 스켈레톤 코드 그대로 쓰기 
        ### ----------------------------------
        
        while True : 
            if (self.root == self.x) or (self.x.n >= m//2 ) :
                finished = True 
                # ok
            else :
                self.bestSibling_result = self.bestSibling(T, m, self.x, self.y)
                
                if self.y.P[self.bestSibling_result].n > m//2 :
                    self.redistributeKeys(T, m, self.x, self.y, self.bestSibling_result)
                    finished = True 
                else :
                    self.mergeNode(T, m, self.x, self.y, self.bestSibling_result)
                    self.x = self.y
                    if len(stack) != 0 : 
                        self.y = stack.pop(-1)
                    else : 
                        finished = True 
            
            if finished == True : 
                break 
        
        #if self.y.n == 0 :
        #    T = self.y.P[0]
            ### discard y node 이걸 구현해야함..귀차늠...ㅇㅇ 
        
        ## stop 
        
        pass 

    def deleteKey(self, T, m, x, oldKey) : 
        i = 0
        q = 1
        while(oldKey > x.K[i]) : 
            i += 1 
            q += 1

        while(i < x.n) :
            x.K[i] = x.K[i+1]
            x.P[q] = x.P[q+1]
            i += 1
            q += 1
        ### 여기 P 마지막꺼만 삭제? 옮기느 작업을 추가해야하지않나싶긴하네
        x.n -= 1 
        return 
        
    
    def bestSibling(self, T, m, x, y) : 
        i = 0
        bestSibling_ = 0
        while (y.P[i] != self.x) : 
            i += 1
        if i == 0 :
            bestSibling_ = i+1
        elif i == y.n : 
            bestSibling_ = i-1
        elif y.P[i-1].n >= y.P[i+1].n :
            bestSibling_ = i-1 
        else : 
            bestSibling_ = i+1 
        return bestSibling_    
    
    def redistributeKeys(self, T, m, x, y, bestSibling) : 
        i = 0
        while(self.y.P[i] != self.x) : 
            i += 1
        bestNode = self.y.P[bestSibling]
        if bestSibling < i : 
            lastKey = bestNode.K[bestNode.n-1]
            self.insertKey(T, m, self.x, None, self.y.K[i-1])
            self.deleteKey(T, m, bestNode, lastKey)
            self.y.K[i-1] = lastKey
        else : 
            firstKey = bestNode.K[0]
            self.insertKey(T, m, self.x, None ,self.y.K[i])
            self.deleteKey(T, m, bestNode, firstKey)
            self.y.K[i] = firstKey
            
        pass 
    
    def mergeNode(self, T, m, x, y, bestSibling) : 
        i = 0 
        while(y.P[i] != self.x) : 
            i += 1
        bestNode = y.P[bestSibling]
        if bestSibling > i : 
            bestSibling = i 
            bestNode = copy.deepcopy(self.x) 
            pass
            # swap(bestSibling, i)
            #swap(bestNode, x)
        i -= 1 
        bestNode.K[bestNode.n] = y.K[i]
        bestNode.n += 1
        j = 0
        while(j < self.x.n) : 
            bestNode.K[bestNode.n] = self.x.K[j]
            bestNode.P[bestNode.n] = self.x.P[j]
            bestNode.n = bestNode.n+1
            j += 1
        bestNode.P[bestNode.n] = self.x.P[self.x.n] ## 여기 다시 테케 만들어서 디버그 
        self.deleteKey(T, m, self.y, self.y.K[i])
        if (self.y.K[0] == 0) and (self.y == self.root) : 
            self.root = bestNode 
        
        pass 
    
# ----------------------------------------------------------------
    def inorderBT(self, T, m) :
        pass
            
Test = B_Tree()


# Test.deleteBT(Test,5,28)
pass 
