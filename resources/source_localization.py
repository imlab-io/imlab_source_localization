import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
from numpy import linalg as alg

# cretae the locations of the cell towers
CellTowers = np.array([[3.0,1.0,9.0],[9.0,1.0, 2.0]])

# cell distances from unknown source location X 
Distances = np.array([[6.0],[4.0],[5.0]])

# get the error function
def GetF(X1, X2, Pi, di):
    F = np.zeros((len(X1), len(X1)))

    # go over all the points
    for x in range(len(X1)):
        for y in range(len(X1)):
            # get the X vector
            X = np.array([[X1[x,y]],[X2[x,y]]])

            # compute the term
            for i in range(len(di)):
                # compute the function value
                F[x, y] += (alg.norm(X - Pi[:, [i]]) - di[i][0])**2
    return F

# set the epsilon for stopping condition
eps = 1e-3

# select one of the starting positions
X = np.array([[10.0], [10.0]])

# get the values for drawing
x1_list = [X[0][0]]
x2_list = [X[1][0]]

# start the iterations
step = 0
while True:

    # increase the number of steps
    step = step + 1

    # create the direction with zeros
    xsum = np.zeros((2, 1))

    # compute the term
    for i in range(len(Distances)):
        # compute \sum_{i \in S}  P_i + \sum_{i \in S}  d_i\frac{P_k - P_i}{\lVert P_k - P_i \lVert}
        xsum += CellTowers[:, [i]] + Distances[i][0] * (X - CellTowers[:, [i]]) / alg.norm(X - CellTowers[:, [i]])

    # compute the fixed point method
    Xn = xsum / len(Distances)

    # add the current coordinates to the list
    x1_list.append(Xn[0][0])
    x2_list.append(Xn[1][0])

    print("Iter[", step, "]: ", alg.norm(Xn-X))

    # check for the return
    if alg.norm(Xn-X) <= eps:
        break
    
    # go to the next iteration
    X = Xn

# display the results
# create the space and function
xRange = [0, 10]
yRange = [0, 10]

# illustrate the function using surface
fig = plt.figure()
ax = fig.add_subplot(111)

# take uniform points and draw the function
X1, X2 = np.meshgrid(np.linspace(xRange[0], xRange[1], 200), np.linspace(yRange[0], yRange[1], 200))

# draw the error surface
GX = GetF(X1, X2, CellTowers, Distances)
im = ax.imshow(GX, alpha=0.4, extent=[
    xRange[0], xRange[1], yRange[0], yRange[1]], origin='lower')
ax.contour(X1, X2, GX, 30, alpha=0.7, zorder=1)

# plot the steps
ax.plot(x1_list, x2_list, ls='-', color='royalblue', marker='o',
         mfc='orange', mec='orange', linewidth=3, markersize=5, zorder=2)
ax.scatter(x1_list[0], x2_list[0], c='black', s=30, zorder=3)
ax.scatter(x1_list[-1], x2_list[-1], c='crimson', s=30, zorder=3)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_aspect('equal')

fig.colorbar(im, ax=ax)

# save the result
plt.savefig('source_localization_steps.png', bbox_inches='tight', dpi=300)

plt.show()

# display the results
print("Solution: ", x1_list[-1], " , ", x2_list[-1], "found in ", step, " iteration")

FinalX = np.ones((1, 1)) * x1_list[-1]
FinalY = np.ones((1, 1)) * x2_list[-1]
print("Final cost is: ", GetF(FinalX, FinalY, CellTowers, Distances))
