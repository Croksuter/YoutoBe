import numpy as np
import pickle

a = np.array([1,2,3,4,5])
with open("pickle.p",'wb') as f:
    pickle.dump(a,f)
with open("pickle.p",'rb') as f:
    print(type(pickle.load(f)))