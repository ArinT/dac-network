import numpy as np

W_aptpa = np.load("W_aptpa.npy")
W = W_aptpa
#create new pathsim score matrix

# print len(W)
# exit()
num_authors = len(W)
W_pathsim = np.zeros(shape = (num_authors,num_authors))


for i in range(num_authors):
	for j in range(num_authors):
		denom = W[i,i] + W[j,j]
		if denom == 0:
			W_pathsim[i,j] = 0
			print "wtf"
			continue

		W_pathsim[i,j] = 2 * W[i,j] / denom

# print W
# print W_pathsim

# np.set_printoptions(suppress=True, threshold='nan')

# print W_pathsim
# np.savetxt('pathsim.txt', W_pathsim)
np.save('pathsim',W_pathsim)
#S(i,j) = 2 * W[i,j] / (W[i,i] + W[j,j])

print "pathsim done"

print W_pathsim[0]
print W_pathsim.T[0]

print "next"


print W_pathsim[10]
print W_pathsim.T[10]

print W_pathsim[10][10]
print W_pathsim.T[10][10]

print "next"

print W_pathsim[100]
print W_pathsim.T[100]

print W_pathsim[100][100]
print W_pathsim.T[100][100]

print "next"

print W_pathsim[1000]
print W_pathsim.T[1000]

print W_pathsim[1000][1000]
print W_pathsim.T[1000][1000]
