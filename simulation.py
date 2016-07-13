from request import request
import config
import time
import random

#Converts a log file of XY coordinates to node numbers and returns a reduced list of lists that contains the log information in its elements.
#Ex.     S|D |#|V|tStamp
#       [1,15,1,4 , 0  ],
#       [2,3,2,3  , 30 ],...
       
def convXYtoNode(logFile):
    benchmark = []

    with open(logFile,"r") as bmread:
        for line in bmread:
            benchmarkLine = []
            benchmarkItems = line.split()
            for i in benchmarkItems:
                benchmarkLine.append(int(float(i)))
            benchmark.append(benchmarkLine)

    newBenchmark = []
    for row in benchmark:
        if (row[0] != 0) & (row[2] != 0):
            newRow = [(row[0] - 1) * 8 + row[1], (row[2] - 1) * 8 + row[3]]
            newRow.extend(row[4:6])
            newRow.append(row[6]*config.EccToOcc)
            newBenchmark.append(newRow)
    return newBenchmark




#Pre-Condition: Number of nodes to be used is input into function
#Post: A list of unique random numbers from 0 to the number of nodes -1 is returned
def generateKey(nodeCount):
    random.seed()
    key = []
    while len(key) < nodeCount:
        randNum = random.randint(0,15)
        uniqueCheck = [False]* len(key)
        if len(key) > 0:
            for i in range(0,len(key)):
                if randNum != key[i]:
                    uniqueCheck[i] = True
            if uniqueCheck[0:len(key)] == [True]*len(uniqueCheck):
                key.append(randNum)

        else:
            key.append(randNum)
    return key

def writeResults(logFile, tClocks,tSimulation, tProgram):
    with open('results.log',"a") as resultFile:
        resultFile.write(logFile + '    ' + str(tClocks) + '    ' + str(tSimulation) + '    ' + str(tProgram) + '\n')

#key1  = generateKey(config.nodeCount)         

for i in range(0,len(config.benchmarks)):
    startTime = time.time()
    logFile = config.benchmarks[i]    
    nodeBenchmarkList = convXYtoNode(logFile)
    listLen = len(nodeBenchmarkList)
    print config.benchmarksOnly[i]
    print '-----------------' + '\n'
    print 'ListLength:' + str(listLen)
    reqCount = 0
    endFlag = False
    config.isover = False
    config.nodestate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    t = 0

    while config.isover == False:
        while  (t == nodeBenchmarkList[reqCount][4] and endFlag==False):
            if reqCount+1 == listLen:
                endFlag = True
            config.activeReq.append(request(nodeBenchmarkList[reqCount][0],nodeBenchmarkList[reqCount][1],nodeBenchmarkList[reqCount][3],nodeBenchmarkList[reqCount][4],nodeBenchmarkList[reqCount][4],endFlag))
            if endFlag == False:
                reqCount += 1

        for req in config.activeReq:
            req.reqProcessing(t)
        t += 1



    print config.nodestate
    print 'Optical Clock Cycles: '+ str(t)
    totalTime = float(t)/(config.OCC*(10**9))
    print 'Runtime: '+ str(totalTime) +'seconds'
    tProgram = time.time()-startTime
    print 'Time for Program: ' + str(tProgram)

    writeResults(config.benchmarksOnly[i], t,totalTime, tProgram)
