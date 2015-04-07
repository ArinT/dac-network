import numpy as np

W_ap = np.load("W_ap.npy")
W_ptp = np.load("W_ptp.npy")
W_pa = W_ap.T

W_aptp = np.dot(W_ap,W_ptp)
W_aptpa = np.dot(W_aptp, W_pa)

# print W_aptpa 


# W_ap_inverse = W

np.set_printoptions(threshold='nan')

# print W_ap

# print W_ap[0]
# print W_pa[0]
# print W_aptpa[0]
# print W_aptpa[1]
# print W_aptpa[2]

print W_aptpa.shape

# np.savetxt('W_aptpa_test.txt', W_aptpa)
np.save('W_aptpa',W_aptpa)

print "W_aptpa done"