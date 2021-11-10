from PIL import Image
import numpy as np
import time
import math

def power_svd(A, iters):
    mu, sigma = 0, 1
    x = np.random.normal(mu, sigma, size=A.shape[1])
    B = A.T.dot(A)
    for i in range(iters):
        new_x = B.dot(x)
        x = new_x
    v = x / np.linalg.norm(x)
    sigma = np.linalg.norm(A.dot(v))
    u = A.dot(v) / sigma
    return np.reshape(u, (A.shape[0], 1)), sigma, np.reshape(v, (A.shape[1], 1))

def svd(A, iterations=10):
    rank = np.linalg.matrix_rank(A)
    U = np.zeros((A.shape[0], 1))
    S = []
    V = np.zeros((A.shape[1], 1))

    # SVD using Power Method
    for i in range(rank):
        u, sigma, v = power_svd(A, iterations)
        U = np.hstack((U, u))
        S.append(sigma)
        V = np.hstack((V, v))
        A = A - u.dot(v.T).dot(sigma)

    return U[:, 1:], S, V[:, 1:].T

def main():
    t = time.time()
    #A = np.array([[1, 2], [3, 4]])
    gambarawal = Image.open('./src/compress/binjai.jpeg') # untuk buka gambarnya pake PIL
    mawal = np.array(gambarawal)
    #m = np.array(test).reshape((2, 3))
    print(np.shape(gambarawal))
    A = mawal[:,:,0] @ mawal[:,:,0].T
    rank = np.linalg.matrix_rank(A)
    U = np.zeros((A.shape[0], 1))
    S = []
    V = np.zeros((A.shape[1], 1))

    # Define the number of iterations
    delta = 0.001
    epsilon = 0.97
    lamda = 2
    iterations = int(math.log(4 * math.log(2 * A.shape[1] / delta) / (epsilon * delta)) / (2 * lamda))

    # SVD using Power Method
    for i in range(rank):
        u, sigma, v = power_svd(A, iterations)
        U = np.hstack((U, u))
        S.append(sigma)
        V = np.hstack((V, v))
        A = A - u.dot(v.T).dot(sigma)
    elapsed = time.time() - t
    print("Power Method of Singular Value Decomposition is done successfully!\nElapsed time: ",elapsed,"seconds\n")
    print("Left Singular Vectors are: \n", U[:, 1:], "\n")
    print("Singular Values are: \n", S, "\n")
    print("Right Singular Vectors are: \n", V[:, 1:].T)


if __name__ == '__main__':
    main()