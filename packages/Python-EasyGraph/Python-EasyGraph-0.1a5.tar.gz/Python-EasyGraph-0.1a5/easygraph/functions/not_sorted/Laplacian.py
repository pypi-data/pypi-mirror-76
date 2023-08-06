def  Laplacian(G,nodes=None,weight=None):
    n=len(G)+1
    X=[0]*n
    W=[0]*n
    CL={}
    Xi=[0]*n
    for i in range(1,n):
        for j in range(1,n):
            if j in G[i].keys():
                X[i]+=G[i][j]
                W[i]+=G[i][j]*G[i][j]
    ELG=sum(X[i]*X[i] for i in range(1,n))+sum(W[i] for i in range(1,n))
    for i in range(1,n):
        Xi=list(X)
        for j in range(1,n):
            if i in G[j].keys():
                Xi[j]-=G[j][i]
        Xi[i]=0
        ELGi=sum(Xi[i]*Xi[i] for i in range(1,n))+sum(W[i] for i in range(1,n))-2*W[i]
        CL[i]=(float)(ELG-ELGi)/ELG
    return CL

