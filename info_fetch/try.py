import numpy as np
import numpy.linalg as la

A = np.array([[1,4],[1,3],[1,2],[1,1]])
a1 = A[:,0]
a2 = A[:,1]

x = (a1.T@a2)/(a1.T@a1)
q1 = a1/la.norm(a1)
B = a2 - (a1 * x)
q2 = B/la.norm(B)
Q = np.array([q1,q2]).T
print("q1:{}\nq2:{}\nQTQ:{}".format(q1,q2,Q.T@Q))

