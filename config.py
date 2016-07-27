import os, sys


# Pre: Requires correct directory of benchmarks in variable path
# Post: Creates list of benchmarks
path = '/home/aberlanga1/Documents/ONoC-Simulation-master/Benchmark Data/16-core'
dirs = os.listdir(path)
benchmarks = []
benchmarksOnly = []

# Appends all benchmarks in directory into one list

for file in dirs:
    benchmarks.append(file)
    benchmarksOnly.append(file)
for i in range(0,len(benchmarks)):
    benchmarks[i] = path + '/' + benchmarks[i]

activeReq = []
nodestate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
OCC = 40 #GHz
ECC = 2 #GHz
packetSize = 8 #bits
nodeCount = 16
weighted_cutoff = 9 # max nodes allowed to be bypassed on furthest path
comCost = 0


#Global time constants to account for certain processes.
EccToOcc       = int(OCC/ECC)
tBuffer        = 1 *EccToOcc
tMUX           = 1 *EccToOcc
tSequence      = 1 *EccToOcc
tSchedule      = 1 *EccToOcc
tInitialize = tBuffer + tMUX + tSequence + tSchedule
tOpenChannels  = 1 *EccToOcc
tCloseChannels = 1 *EccToOcc

tInitialize = tBuffer + tMUX + tSequence + tSchedule
tChannelAloc = tOpenChannels + tCloseChannels

#Global clock cycle constant for tracking t clock intervals
t = 0