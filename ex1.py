import sys

import matplotlib.pyplot as plt
import numpy as np
SIZE =3
def get_clusters(pixels,z):
    clusters = [[] for _ in range(len(z))]
    cost =0
    for p in pixels:
        min = None
        min_index = None
        i = 0
        for z_i in z:
            sum = 0
            for j in range(0, SIZE):
                sum += pow((p[j] - z_i[j]),2)
            if min is None:
                min = sum
                min_index = i
            elif sum < min:
                min = sum
                min_index = i
            i += 1
        clusters[min_index].append(p)
        cost += min
    cost /= len(pixels)
    return clusters,cost


def cal_new_z(clusters,old_z):
    new_z = []
    index = 0
    for c in clusters:
        z = [0 for k in range(SIZE)]
        if len(c) >0 :
            for p in c:
                for i in range(SIZE):
                   z[i] += p[i]
            for i in range(SIZE):
                z[i] = (z[i] / len(c)).round(4)
            new_z.append(z)
        else:
            new_z.append(old_z[index])
        index +=1
    return new_z


image_fname,centroids_fname,out_fname = sys.argv[1],sys.argv[2],sys.argv[3]
z= np.loadtxt(centroids_fname)

orig_pixels = plt.imread(image_fname)
pixels = orig_pixels.astype(float)/255.
pixels = pixels.reshape(-1,3)
f = open(out_fname, "w+")
# x_axis=[]
# y_axis=[]
for i in range(0,20):
    clusters,cost = get_clusters(pixels, z)
    # y_axis.append(cost)
    # x_axis.append(i)
    new_z = cal_new_z(clusters,z)
    new_z = np.asarray(new_z)
    f.write(f"[iter {i}]:{','.join([str(i) for i in new_z])}\n")
    if i != 0 and np.array_equal(z, new_z):
        break;
    z = new_z
f.close()
# plt.plot(x_axis,y_axis,marker="o")
# plt.xlabel("iterations")
# plt.ylabel("total loss")
# plt.title(f"k={len(z)}")
# plt.show()

