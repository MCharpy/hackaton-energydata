import numpy as np
import pickle

def read_int(f):
    ba = bytearray(4)
    f.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.int32)
    return prm[0]

def read_double(f):
    ba = bytearray(8)
    f.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.double)
    return prm[0]

def read_double_tab(f, n):
    ba = bytearray(8*n)
    nr = f.readinto(ba)
    if nr != len(ba):
        return []
    else:
        prm = np.frombuffer(ba, dtype=np.double)
        return prm

def get_pics_from_file(filename):
    f_pic = open(filename, "rb")
    info = dict()
    info["nb_pics"] = read_int(f_pic)
    info["freq_sampling_khz"] = read_double(f_pic)
    info["freq_trame_hz"] = read_double(f_pic)
    info["freq_pic_khz"] = read_double(f_pic)
    info["norm_fact"] = read_double(f_pic)
    tab_pics = []
    pics = read_double_tab(f_pic, info["nb_pics"])
    nb_trames = 1
    while len(pics) > 0:
        nb_trames = nb_trames + 1
        tab_pics.append(pics)
        pics = read_double_tab(f_pic, info["nb_pics"])
    f_pic.close()
    return tab_pics, info

classifier = pickle.load(open("./KNN_model.sav",'rb'))
sc_X = pickle.load(open("./scaling_function.sav",'rb'))

# Loading the signal
input, info = get_pics_from_file("../data/pics_LOGINMDP.bin")

# Average value of NOKEY
pics_nokey, info = get_pics_from_file("../data/pics_NOKEY.bin")
nokey = np.mean(pics_nokey,axis=0)

output = []
step = 90

for i in range(30000000):
    if (step * (i + 1)) >= len(input):
        break
    curr = input[step * i:step * (i + 1)] # chunking
    curr = np.subtract(curr, nokey) # removing noise
    curr = sc_X.transform(curr) # scaling
    curr_output = classifier.predict(curr)

    # Picking best guess
    unique, pos = np.unique(curr_output, return_inverse=True)
    max_value = unique[np.bincount(pos).argmax()]

    if max_value == 'NOKEY':
        continue

    # Guessing key pressed with the SHIFT key (if there is)
    if max_value == 'SHIFT':
        curr = input[step * i:step * (i + 1)]

        # Removing the meaningful value of SHIFT's signal
        for j, frame in enumerate(curr):
            frame[5] = 0
            curr[j] = frame

        curr = np.subtract(curr,nokey)
        curr = sc_X.transform(curr)
        curr_output = classifier.predict(curr)
        unique, pos = np.unique(curr_output, return_inverse=True)
        max_value = unique[np.bincount(pos).argmax()]

        if max_value == 'NOKEY' or max_value == 'SHIFT':
            continue # Nothing added to input
        if output == [] or ("SHIFT " + max_value) != output[-1]:
            output.append("SHIFT " + max_value)

    elif output == [] or max_value != output[-1]:
        output.append(max_value)

#%%

print("The input's length is:", len(output))
for a in output:
    print(a)