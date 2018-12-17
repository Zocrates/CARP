import time
import sys
import numpy as np

def Open():
    size = 0
    depot = 1
    matrix_cost = np.zeros([size, size])
    matrix_demand = np.zeros([size, size])
    Capacity = 0
    count=0
    list=[]
    file_name = sys.argv[1]
    time_limit = int(sys.argv[3])
    seed = int(sys.argv[5])
    f=open('F:/sustech/AI/carpn/carpn/carp/carp_sample/egl-e1-A.dat','r')
    for line in f:
        line.split()
        list.append(line)
        count=count+1
    vertice=list[1]
    size=int(vertice[11:])+1
    matrix_cost = np.zeros([size, size])
    matrix_demand = np.zeros([size, size])
    i=list[2]
    depot=int(i[8])
    re=list[3]
    RE=int(re[17:])
    nre=list[4]
    NRE=int(nre[21:])
    c=list[6]
    Capacity=int(c[11:])

    for j in range(9,count-1):
        data=list[j]
        x = int(data.split()[0])
        y = int(data.split()[1])
        cost = int(data.split()[2])
        demand = int(data.split()[3])
        matrix_cost[y][x] = cost
        matrix_cost[x][y] = cost
        matrix_demand[x][y] = demand
        matrix_demand[y][x] = demand
    for i in range(1,size):
        for j in range(1,size):
            if i!=j and matrix_cost[i][j]==0:
                matrix_cost[i][j]=np.inf
    return matrix_cost,matrix_demand,depot,size,Capacity


#将导入数据用Floyd算法算出最短路径在存入新矩阵
def Floyd():
    arr = Open()
    min_cost = arr[0]
    size = arr[3]
    for k in range(1,size):
        for i in range(1,size):
            for j in range(1,size):
                if (min_cost[i][j] > min_cost[i][k] + min_cost[k][j]):
                    min_cost[i][j] = min_cost[i][k] + min_cost[k][j]
    return min_cost

def Floyd2():
    min_c=Floyd()
    arr = Open()
    size = arr[3]
    for k in range(1,size):
        for i in range(1,size):
            for j in range(1,size):
                if (min_c[i][j] > min_c[i][k] + min_c[k][j]):
                    min_c[i][j] = min_c[i][k] + min_c[k][j]
    return min_c

def demand_cost():
    arr = Open()
    size = arr[3]
    original_cost=arr[0]
    matrix_demand=arr[1]
    matrix_cost=Floyd2()
    for i in range(1,size):
        for j in range(1,size):
            if matrix_demand[i][j]!=0:
                matrix_cost[i][j]=original_cost[i][j]
    return matrix_cost

def s_format():
    s=PathScan()[0]
    s_print = []
    for p in s:
        s_print.append(0)
        s_print.extend(p)
        s_print.append(0)
    return s_print

#将得到的最短路径进行pathscan
def PathScan():
    orgnl_cost=demand_cost()
    arr=Open()
    matrix_demand=arr[1]
    depot=arr[2]
    size=arr[3]
    Capacity=arr[4]
    test=Floyd2()
    rev_arc=[]
    arc=[]
    Route=[]
    Sum=0
    S=[]
    tS=[]
    tRoute=[]
    tCost=[]
    Cost=[]
    tLoad=[]
    Load=[]
    #将所有弧加入arc,已删除重复的弧
    for i in range(1,size):
        for j in range(i,size):
            if i!=j and matrix_demand[i][j]!=0:
                arc.append([i,j])
                rev_arc.append([j,i])
    task=arc+rev_arc

    #开始算法
    while True:
        s=[]
        route=[]
        load=0
        cost=0
        i=depot
        while True:
            d=np.inf
            if not task: break
            for u in task:
                if load + matrix_demand[u[0]][u[1]] < Capacity:
                    if test[i][u[0]] < d:
                        nu = u
                        d = test[i][u[0]]
                    elif test[i][u[0]]==d:
                        nu = u
                        d = test[i][u[0]]

            if d != np.inf:
                smallk=(nu[0],nu[1])
                s.append(smallk)
                route.append(nu)
                task.remove(nu)
                task.remove(nu[::-1])
                load = load + matrix_demand[nu[0]][nu[1]]
                cost = cost + orgnl_cost[nu[0]][nu[1]]+ d
                i = nu[1]

            if d == np.inf or not task: break
        S.append(s)
        cost = cost + test[i][depot]
        Route.append(route)
        Load.append(load)
        Cost.append(cost)
        if not task: break
    if sum(Cost) <= sum(tCost) or sum(tCost) == 0:
        tCost = Cost
        tLoad = Load
        tRoute = Route
        tS=S
    for k in tCost:
        Sum=k+Sum
    return tS,Sum


print("s", (",".join(str(d) for d in s_format())).replace(" ", ""))
print("q", int(PathScan()[1]))