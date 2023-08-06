__all__=[
    "ego_betweenness"
]
import numpy as np 
import numpy.matlib 

def ego_betweenness(G):
    adj=G.adj.copy()
    num=len(adj)+1
    G=np.matlib.zeros((num,num))
    for i in range(1,num):
        for j in range(1,num):
            temp_key = adj[i].keys()
            if j in temp_key:
                G[i,j]=adj[i][j]['weight']
    for i in range(1,num):
        l1=list()
        l1.append(i)
        for j in range(1,num):
            if G[i,j]!=0:
                l1.append(j)
        for j in range(1,num):
            if G[j,i]!=0:
                l1.append(j)
        l2=list(set(l1))
        n=len(l2)+1
        A=np.matlib.zeros((n,n))
        for i in range(1,n):
            for j in range(1,n):
                A[i,j]=G[l2[i],l2[j]]
        B=A*A
        C=1-A
        n=len(A)+1
        sum=0
        flag=1
        for i in range(1,n):
            for j in range(1,n):
                if A[i,j]!=A[j,i]:
                    flag=0
                    break
            if flag==0:
                break
        for i in range(1,n):
            for j in range(1,n):
                if i!=j and C[i,j]==1 and B[i,j]!=0:
                    sum+=1.0/B[i,j]
        if flag==1:
            sum/=2
        print(sum)

