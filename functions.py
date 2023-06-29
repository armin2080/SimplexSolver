import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

iterations = []


def slack(line,var_count):
    symbol = line[-2]
    if symbol==">=" or symbol==">":
        for i in range(len(line)):
            var = line[i]
            if var[0] == "":
                var[0] = "+1"
            if type(var) == list:
                if var != symbol:
                    if var[0][0] == "-":
                        var = ["+" + f"{var[0][1:]}",var[1]]
                    elif var[0][0] == "+":
                        var = ["-" + f"{var[0][1:]}",var[1]]
                    else:
                        var = ["-" + f"{var[0]}",var[1]]
            else:
                if var != symbol:
                    if var[0] == "-":
                        var = "+" + f"{var[1:]}"
                    else:
                        var = "-" + var
                else:
                    if var == ">=":
                        var = "<="
                    else:
                        var == "<"
            line[i] = var
    elif symbol=="<=" or symbol=="<":
        var_count += 1
        new_var = ['+',f"{var_count}"]
        line.insert(-2,new_var)
        line[-2] = "="
        

        
    return line , var_count

def load_st(st,target_var_count):

    b = []

    for k in range(len(st)) :
        st[k] = st[k].split(" ")
        for t in range(len(st[k])) :
            if 'x' in st[k][t]:
                st[k][t] = st[k][t].split("x")
                b.append(int(st[k][t][1]))
    m = max(b)

    if target_var_count == 2:
        x = np.linspace(-200,200,1000)

        for i in range(len(st)):
            line = st[i]
            a = line[0][0]
            b = line[1][0]
            c = float(line[-1])
            if a == "" or a == "+":
                a = "1"
            elif a == "-":
                a = "-1"
            if b == "" or b == "+":
                b = "1"
            elif b == "-":
                b = "-1"
            a = float(a)
            b = float(b)
            y = (c - a*x)/ b
            plt.plot(x,y)
            figure = plt.gcf()

        plt.xlabel("x1")
        plt.ylabel("x2")

        plt.xlim(-10,10)
        plt.ylim(-10,10)

        plt.axvline(x=0, c="black", label="x=0")
        plt.axhline(y=0, c="black", label="y=0")

        canvas = FigureCanvas(figure)
        plt.show()
    else:
        canvas = ''

    for i in range(len(st)):
        line = st[i]
        line , m = slack(line,m)
        if line[-2] == "<=" or "<":
            line,m = slack(line,m)

    s_matrix = np.zeros((len(st),m+1))

    for i in range(len(st)) :
        line = st[i]
        s_matrix[i,s_matrix.shape[1]-1] = float(line[-1])
        for j in range(len(line)-2) :
            index = int(line[j][1])
            value = line[j][0]
            if value == "" or value == "+":
                value = 1
            elif value == "-":
                value = -1
            else:
                value = float(value)
            s_matrix[i,index-1] = value

    
        
    return s_matrix , canvas 

matrix = [[-1, -2, -3, -4,  0],
       [ 1,  2,  1,  0,  0],
       [ 1,  3,  0,  1,  0],
       [ 2,  4,  0,  0,  1]]


def target_func(target_list):
    maximum = 0
    for i in range(len(target_list)):
        if "x" in target_list[i]:
            var = target_list[i].split("x")
            if var[0] == "" or var[0] == "+":
                var[0] = "1"
            elif var[0] == "-":
                var[0] = "-1"
            target_list[i] = var
            
            index = int(target_list[i][1])
            if index > maximum:
                maximum = index
    output = [0 for i in range(maximum)]
    for i in range(len(target_list)):
        output[i] = float(target_list[i][0])
        
    return output , maximum


def inverse_target(target,var_count):
    while len(target)!= var_count:
        target.append(0)
    inverse_t = np.zeros(len(target),dtype=float)
    for i in range(len(target)):
        inverse_t[i] = -(float(target[i]))
    return inverse_t

def combine(target,st):

    matrix = np.insert(st, 0,target, axis=0)
    return matrix
    

target = np.array([1 , 2])
st = np.array([[1 , 2 ,1,3,0,0], [2 , 3 ,0, 4,1,0],[2 , 3 ,0, 4,0,1]])
# start(target,st)

def id_matrix(matrix):
    
    matrix = np.delete(matrix,matrix.shape[1]-1,1)
    index = []
    identity_matrix = np.eye(matrix.shape[0])
    for i in range(matrix.shape[1]):
        column = matrix[:,i]
        for j in range(matrix.shape[0]):
            id_column = identity_matrix[:,j]
            if np.array_equal(column, id_column):
                np.delete(identity_matrix, j,1)
                index.append(i)
 
    if len(index) == matrix.shape[0]:
        return index
    else:
        return False

def gaus(matrix,output_index,enter_value):
    main_element = matrix[output_index+1,enter_value]
    main_row = matrix[output_index + 1] / main_element
    matrix[output_index + 1] = main_row
    for i in range(matrix.shape[0]):
        if i != (output_index+1):
            target_element = matrix[i,enter_value]
            target_row = matrix[i]
            matrix[i]= np.subtract(target_row,main_row*target_element)
    return matrix

def simplex(matrix,basics):
    matrix = matrix.astype('float')
    target = matrix[0]
    if basics == False:
        return "Problem cannot be solved"
    if np.all((target<=0)):
        for i in range(target.shape[0]):
            if i not in basics:
                if target[i] == 0:
                    return "Problem has alternative optimized solution"
        return "Problem has a unique optimized solution"
    else:
        enter_value = np.argmax(target)
        Y = np.array(matrix[:,enter_value][1:])
        if np.all((Y<=0)):
            return "Problem has Infinite solutions"
        else:
            thetas = np.zeros((1,Y.shape[0]))
            RHS = matrix[:,matrix.shape[1]-1][1:]
            minimum = 100000
            for i in range(Y.shape[0]):
                y = Y[i]
                rhs = RHS[i]
                if y > 0:
                    theta = rhs / y
                    thetas[0,i] = theta
                    if theta < minimum:
                        minimum , index = theta , i
        
        matrix = gaus(matrix,index,enter_value)
        new_basic = basics.copy()
        new_basic[index] = enter_value
        
        return [matrix , new_basic]           