import copy, math
'''
삽입 : 성공 
삭제 : 성공
언어 : python 3.10.6
운영체제 : mac OS 
'''
class Node : 
    def __init__(self, m) :
        # K: 키들을 담고 있는 배열
        # P: 자식노드를 담고 있는 배열
        # n: 노드가 가진 키의 개수 
        self.K = [0 for _ in range(m)]
        self.n = 0
        self.P = [0 for _ in range(m+1)]
    
class B_Tree : 
    def __init__(self) : 
        self.root = None 
        return None 
    
# ------------------------------<< insert >>----------------------------------

    def insertBT(self, T, m, newKey) : 
        # root 가 없는 경우 새 노드 생성
        if self.root == None : 
            T = self.getNode(m) 
            T.K[0] = newKey 
            T.n = 1
            self.root = T 
            return self.root
        
        T = self.root 
        # newKe 까지의 경로를 stack에 저장 
        found, stack = self.serachPath(T, m, newKey, None)
        
        # found가 True면 이미 newKey가 트리 내에 존재함. 삽입 안함
        if found == True : 
            print(f"i {newKey} : The key already exists")
            return self.root
        
        finished = False 
        self.x = stack.pop(-1)
        self.y = None 
        
        while True : 
            # 노드가 가질 수 있는 Key의 최대보다 적을 경우 그대로 삽입
            if self.x.n < m-1 : 
                self.insertKey(T, m, self.x, self.y, newKey) 
                finished = True 
                
            # 노드가 가질 수 있는 Key가 이미 최대인 경우 삽입 후 split
            else : 
                # newKey를 배열에 넣은 후 그 중 centerKey를 return 
                # return한 centerKey를 다시 newKey에 저장
                newKey, self.y = self.splitNode(T, m, self.x, self.y, newKey)
                if len(stack) != 0 :
                    self.x = stack.pop(-1)
                else : 
                    # 분할이 root에서 일어날 경우
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
    
    # Key의 경로를 stack에 저장하여 리턴하는 함수
    def serachPath(self, T, m, key, stack) : 
        # 빈 stack이 들어온다면 빈 리스트로 저장하고 그렇지 않다면 기존 stack에 추가
        if (stack == None) or (len(stack) == 0) : 
            stack = []
        self.x = T 
        
        while True : 
            i = 0
            # newKey의 경로를 탐색
            while ((i < self.x.n) and (key > self.x.K[i])) : 
                i += 1
            if (i <= self.x.n) and (key == self.x.K[i]) : 
                stack.append(self.x) 
                return True, stack
            stack.append(self.x) 
            self.x = self.x.P[i]
            # P 배열에서 서브트리가 중간에 빈 경우
            # while문을 끝내지 않고 P 배열의 다음 서브트리 확인
            if self.x != 0 and self.x != None : 
                continue
            break 
        return False, stack 
    
    # newKey를 노드 내 해당 위치에 추가하는 함수
    def insertKey(self, T, m, x, y, newKey) : 
        i = self.x.n - 1 
        # newKey의 위치를 기준으로 하나씩 옆으로 옮긴다. 
        # newKey가 들어갈 공간을 만드는 것과 동일
        while ((i >= 0) and (newKey < self.x.K[i])) : 
            self.x.K[i+1] = self.x.K[i]
            self.x.P[i+2] = self.x.P[i+1]
            i = i-1
        self.x.K[i+1] = newKey 
        
        if y != None : 
            # y 가 None이 아닐 경우 서브트리가 제대로 옮겨지지 않는 경우 
            # def splitNode()에서 지정한 relinkNode를 P 배열에 추가
            self.x.P[i+1] = self.relinkNode 
        self.x.P[i+2] = y 
        self.x.n = self.x.n+1
        return 
    
        # newKey를 추가한 노드의 key의 개수가 max를 넘었을 경우 split하는 함수
    def splitNode(self, T, m, x, y, newKey) : 
        # key를 추가하고 tempNode에 저장
        # self.x는 새로운 노드로 바꿈.
        self.insertKey(T, m, x , y, newKey)
        self.tempNode = copy.deepcopy(self.x)
        self.centerKey = self.tempNode.K[self.tempNode.n // 2 ]
        self.x = self.getNode(m)
        self.x.n = 0 
        i = 0
        
        # tempNode에서 centerKey를 기준으로 x노드에 키와 자식 노드를 복사
        while(self.tempNode.K[i] < self.centerKey) : 
            self.x.K[i] = self.tempNode.K[i]
            self.x.P[i] = self.tempNode.P[i]
            i += 1
            self.x.n += 1
        self.x.P[i] = self.tempNode.P[i]
        self.newNode = self.getNode(m)
        q = 0 
        i += 1
        # newNode로 x노드에 복사하지 않은 tempNode의 키와 자식 노드를 복사
        while(i < self.tempNode.n) : 
            self.newNode.K[q] = self.tempNode.K[i]
            self.newNode.P[q] = self.tempNode.P[i]
            i += 1
            q += 1
            self.newNode.n += 1
        self.newNode.P[q] = self.tempNode.P[i]
        self.relinkNode = copy.deepcopy(self.x)
        return self.centerKey , self.newNode 
    
    # 새로운 노드를 만드는 함수
    def getNode(self, m) : 
        return Node(m) 
    
#---------------------------<< delete >>------------------------------------

    # oldKey를 삭제하고 경우에 따라 redistribution, merge를 진행하는 함수
    def deleteBT(self, T, m, oldKey) : 
        T = self.root 
        # oldKey의 경로와 트리 내 존재 유무를 확인
        found, stack = self.serachPath(T, m, oldKey, None)
        # 만약 oldKey가 트리 내 존재하지 않는다면 삭제할 수 없음
        if found == False : 
            print(f"d {oldKey} : The key does not exist")
            return 
        self.internal_Node = stack[-1]
        self.x = stack.pop(-1)
        self.oldKey_index = -1
        is_internal_Node = False 
        
        # 내부노드에서 발견되었다면 is_internal_Node의 값을 변경
        for i in range(0,len(self.x.P)) : 
            if (self.x.P[i] != 0) and (self.x.P[i] != None) : 
                is_internal_Node = True
        
        # 내부노드에서 발견된 경우 
        if is_internal_Node : 
            # oldKey가 K배열에서 몇 번째 key인지를 탐색
            for i in range(0,len(self.internal_Node.K)) : 
                if self.internal_Node.K[i] == oldKey : 
                    self.oldKey_index = i
            # oldKey와 바꿀 후행키를 찾고 stack에 경로 저장
            found2, stack = self.serachPath(self.x.P[self.oldKey_index], m, self.x.K[self.oldKey_index], stack )
            self.x = stack.pop(-1)
            # 서로 다른 노드에서 후행키를 추가하고 oldKey를 추가
            self.temp = self.internal_Node.K[self.oldKey_index]
            for i in range(0,len(self.x.K)) : 
                if self.x.K[i] != 0 : 
                    self.newKey_index = i 
            self.internal_Node.K[self.oldKey_index] = self.x.K[self.newKey_index]
            self.x.K[self.newKey_index] = self.temp
        
        finished = False 
        # oldKey를 삭제
        self.deleteKey(self.internal_Node, m, self.x, oldKey)
        
        if len(stack) != 0 : 
            self.y = stack.pop(-1)
            
        while True : 
            # x 노드의 underflow 검사
            if (self.root == self.x) or (self.x.n >= math.ceil(m/2)-1 ) :
                finished = True 

            else :
                # y노드가 x노드의 부모인 경우 
                if self.x in self.y.P : 
                    self.bestSibling_result = self.bestSibling(T, m, self.x, self.y)
                    # 형제 노드에서 키를 재분배하는 경우 
                    if self.y.P[self.bestSibling_result].n > m//2 :
                        self.redistributeKeys(T, m, self.x, self.y, self.bestSibling_result)
                        finished = True 
                    # 형제 노드에서 키를 재분배하지 못하고 합병하는 경우 
                    else :
                        self.mergeNode(T, m, self.x, self.y, self.bestSibling_result)
                        self.x = self.y
                        if len(stack) != 0 : 
                            self.y = stack.pop(-1)
                        else : 
                            finished = True  
                # internal_Node가 x노드의 부모인 경우
                else : 
                    self.bestSibling_result = self.bestSibling(T, m, self.x, self.internal_Node)
                    # 형제 노드에서 키를 재분배하는 경우 
                    if self.internal_Node.P[self.bestSibling_result].n > math.ceil(m/2)-1 :
                        self.redistributeKeys(T, m, self.x, self.internal_Node, self.bestSibling_result)
                        finished = True 
                    # 형제 노드에서 키를 재분배하지 못하고 합병하는 경우 
                    else :
                        self.mergeNode(T, m, self.x, self.internal_Node, self.bestSibling_result)
                        self.x = self.internal_Node 
                        if len(stack) != 0 : 
                            self.y = stack.pop(-1)
                        else : 
                            if self.internal_Node.K[0] == 0 : 
                                continue
                            finished = True 
            
            if finished == True : 
                break 
        return 

    # oldKey를 x노드에서 삭제하는 함수 
    def deleteKey(self, T, m, x, oldKey) : 
        i = 0
        q = 1
        # x노드에서 oldKey의 index를 구함
        while(oldKey > x.K[i]) : 
            i += 1 
            q += 1
        # 구한 index를 기준으로 key와 자식 노드를 이동
        while(i < x.n) :
            x.K[i] = x.K[i+1]
            x.P[q] = x.P[q+1]
            i += 1
            q += 1
        x.n -= 1 
        return 
        
    # 형제 노드(왼쪽, 오른쪽) 중 어떤 노드가 사용하기에 최적의 노드인지를 구하는 함수    
    def bestSibling(self, T, m, x, y) : 
        i = 0
        bestSibling_ = 0
        # x노드의 부모인 y노드에서 최적의 형제 노드를 탐색
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
    
    # 재분배 하는 함수 
    def redistributeKeys(self, T, m, x, y, bestSibling) : 
        i = 0
        # y노드에서 x노드가 몇 번째 자식 노드인지를 구함
        while(y.P[i] != self.x) : 
            i += 1
        # 최적의 형제 노드를 bestNode에 저장
        bestNode = y.P[bestSibling]
        # x노드를 기준으로 사용할 형제 노드가 왼쪽에 있는 경우
        if bestSibling < i : 
            lastKey = bestNode.K[bestNode.n-1]
            self.insertKey(T, m, self.x, None, y.K[i-1])
            self.deleteKey(T, m, bestNode, lastKey)
            y.K[i-1] = lastKey
        # x노드를 기준으로 사용할 형제 노드가 오른쪽에 있는 경우
        else : 
            firstKey = bestNode.K[0]
            self.insertKey(T, m, self.x, None ,y.K[i])
            self.x.P[i+1] = bestNode.P[0]
            bestNode.P[0] = bestNode.P[1] 
            self.deleteKey(T, m, bestNode, firstKey)
            y.K[i] = firstKey
        return     
    
    # 합병하는 함수 
    def mergeNode(self, T, m, x, y, bestSibling) : 
        i = 0
        # y노드에서 x노드가 몇 번째 자식 노드인지를 구함
        while(y.P[i] != self.x) : 
            i += 1
        # bestNode를 최적의 형제 노드로 저장
        bestNode = y.P[bestSibling]
        # 형제 노드가 x노드 기준 오른쪽에 있다면 서로의 위치를 바꿈
        if bestSibling > i : 
            self.x =  y.P[bestSibling]
            bestNode = y.P[i]
        else :
            i -= 1 
        # bestNode와 x 노드, y노드의 K[i]를 합병 
        bestNode.K[bestNode.n] = y.K[i]
        bestNode.n += 1
        j = 0
        while(j < self.x.n) : 
            bestNode.K[bestNode.n] = self.x.K[j]
            bestNode.P[bestNode.n] = self.x.P[j]
            bestNode.n = bestNode.n+1
            j += 1
        bestNode.P[bestNode.n] = self.x.P[self.x.n] 
        # y노드에서 bestNode로 합병한 K[i]를 삭제
        self.deleteKey(T, m, y, y.K[i])
        if (y.K[0] == 0) and (y == self.root) : 
            self.root = bestNode 
        return 

#---------------------------<< print >>------------------------------------
    # 중위 순회하면서 출력하는 함수 
    def inorderBT(self, T, m) :
        i = 0 
        while True : 
            # P의 끝까지 돈 경우 
            if len(T.P) == i+1 : 
                break
            # P를 돌다가 자식 노드가 없는 경우
            # 다음 P의 다음 자식 노드로 이동 
            if T.P[i] == None or T.P[i] == 0 : 
                i += 1
                continue
            # P의 자식 노드로 이동하여 다시 중위 순회
            self.inorderBT(T.P[i],m)
            # 자신의 key가 0인 경우를 출력 안함
            if T.K[i] != 0 : 
                print(f"{T.K[i]}", end = " ")
            i += 1 
        for k in T.P : 
            if k != None and k != 0 : 
                return 
        for k in T.K : 
            if k == 0 or k == None : 
                continue
            # 자신의 key를 출력
            print(f"{k}", end = " ")
        
        return 
    
# M = 3, 4 인 경우 반복문으로 출력
for M in range(3,5) : 
    Test = B_Tree()
    f = open("File_processing/B_Tree_File/BT-input.txt","r")

    for i in f : 
        data = i.split(' ')
        data[1] = data[1][:-1]
        if data[0] == 'i' : 
            Test.insertBT(Test,M,int(data[1]))
        else : 
            Test.deleteBT(Test,M,int(data[1]))
        Test.inorderBT(Test.root,M)
        print("")
    