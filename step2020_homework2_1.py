import numpy, sys, time
import matplotlib.pyplot as plt
import os

numbers=[]
times=[]

#collect data for relationship of N and time to calculate matrix product 
for n in range(1,300,50):
    a = numpy.zeros((n, n)) # Matrix A
    b = numpy.zeros((n, n)) # Matrix B
    c = numpy.zeros((n, n)) # Matrix C
    
    # Initialize the matrices to some values.
    for i in range(n):
        for j in range(n):
            a[i, j] = i * n + j
            b[i, j] = j * n + i
            c[i, j] = 0
    
    begin = time.time()
    
    #calculate matrix product of a and b
    for i in range(n):
        for j in range(n):
            for k in range(n):
                c[i,j]+=a[i,k]*b[k,j]
    
    end = time.time()
    numbers.append(n)
    times.append((end - begin))

#make gragh
plt.rcParams['font.family'] = 'IPAexGothic'
plt.plot(numbers,times)

plt.title("the relation of N and time",fontname="MS Gothic")
plt.xlabel("N",fontname="MS Gothic")
plt.ylabel("time[sec]",fontname="MS Gothic")
plt.grid()

save_dir="./output/"
save_file="homework2_relationship_gragh"+'.png'
path=os.path.join(save_dir,save_file)
plt.savefig(path)

plt.show()
