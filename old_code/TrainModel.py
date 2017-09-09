from __future__ import division

import os

import biosppy.signals.ecg as bio
import matplotlib.pyplot as plt
import numpy as np
import paramiko as para
import wfdb as wf
from keras.layers import Dense
from keras.models import Sequential

# Data Extraction from Database
dpath = '/media/abhinav/USB20FD/PTBDB/physionet.org/physiobank/database/ptbdb/'  # Path To Databank
fpath = 'patients.txt'  # Path to the full patient list
cpath = 'control.txt'  # Path to the control non MI patient list
sampsize = 10000
rate = 1000

# Define text arrays
patients = (np.loadtxt(fname=fpath, dtype=str)).tolist()
controls = (np.loadtxt(fname=cpath, dtype=str)).tolist()
# Take control patient array away from full patient array
mipatients = (set(patients) - set(controls))
misize = len(mipatients)
csize = len(controls)
# Allocate memory for MIdatabase array
midatabase = np.zeros(shape=(misize, (sampsize + 1)))
cdatabase = np.zeros(shape=(csize, (sampsize + 1)))
i = 0
for p in mipatients:
    sig = (wf.rdsamp(dpath + str(p), sampto=sampsize, pbdl=0, channels=[0])[0])
    nsig = np.append(sig, [1])
    nsig.shape = (1, 10001)
    # print nsig.shape[1]
    midatabase[i] = nsig  # Appends the two 2D arrays together
    i = i + 1
n = 0
for c in (controls):
    sig = (wf.rdsamp(dpath + str(c), sampto=sampsize, pbdl=0, channels=[0])[0])
    nsig = np.append(sig, [0])
    nsig.shape = (1, 10001)
    cdatabase[n] = nsig  # Appends the two 2D arrays together
    n = n + 1
print midatabase
print cdatabase
# print midatabase [0,10000]

fulldatabase = np.append(midatabase, cdatabase, 0)
print fulldatabase
size = fulldatabase.shape[0]
print size
'''
The database is structured as follows
each sample has 10000 points of data with a classification
either
1 - Heart Attack
0 - Not Heart Attack
On indice 10000 or after the 10000 points
'''

i = 0
extracted = np.zeros(shape=(size, (31)))

# Extraction
while i < size:
    r = fulldatabase[i]
    t = r[:9999]
    # Beat extraction
    templates = bio.ecg(t, rate, False)[4]
    beat = templates[5]  # Use the beat extraction 5
    p = 20 * np.log10(np.abs(np.fft.rfft(beat)))  # Perform an FFT

    # This performs an FFT and extract magnitude information
    # of the frequency domain

    nqf = rate / 2
    samps = p.size
    pperf = samps / nqf
    newpoints = int(pperf * 50)
    s = p[0:newpoints]
    ns = np.append(s, r[10000])
    extracted[i] = ns
    i = i + 1

extracted = np.array(extracted)
size = extracted.shape[0]
trainsize = int(size * 0.7)  # Training Data Allocation
np.random.seed(49)  # Create Seed to consistently generate same random sequence
# Shuffle on the first axis
np.random.shuffle(extracted)
training, test = extracted[:trainsize, :], extracted[trainsize:, :]
# Machine Learning
# Split into input and output
X = training[:, 0:30]
Y = training[:, 30]
Xtest = test[:, 0:30]
Ytest = test[:, 30]

# Models

# create model
model = Sequential()
model.add(Dense(30, input_dim=30, init='uniform', activation='relu'))
model.add(Dense(15, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))

# Backend compiles the defined model into sequential
# code with the loss function and optimmization algorithm

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the Model with a set number of iterations (epoch)
# and the size of each data batch

# Fit the model
history = model.fit(X, Y, nb_epoch=150, batch_size=10)

# This example does not have a sepperate
# train and testing data set but ideally
# this would be the case

print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['acc'])
# plt.plot(history.history['val_acc'])
plt.title('Model Accuracy vs Iteration Number')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
# plt.plot(history.history['val_loss'])
plt.title('Model Loss vs Iteration Number')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training'], loc='upper left')
plt.show()

# evaluate the model
scores = model.evaluate(Xtest, Ytest)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

# Export the model
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
    json_file.close()

# Save all the weights to HDF5
model.save_weights("model.h5")
print "Saved Model"
# SSH Client

# os.system("scp model.json pi@10.0.0.112")
# os.system("scp model.h5 pi@10.0.0.112")
username = "pi"
password = "raspberry"
server = 10.0
.0
.112
localweights = "model.h5"
remoteweights = ""
localmodel = "model.json"
remotemodel = ""

ssh = para.SSHClient()
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect(server, username=username, password=password)
stfp = ssh.open_sftp()
stfp.put(localmodel, remotemodel)
stfp.put(localweights, remoteweights)  # Weights
stfp.close()
ssh.close()
