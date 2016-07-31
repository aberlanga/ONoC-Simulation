from request import request
import config
import time
import random
import nn

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


def mapping(key, benchmark):
    for row in benchmark:
        row[0]=key[row[0]]
        row[1]=key[row[1]]

    return benchmark











def writeResults(logFile, tClocks,tSimulation, tProgram, currentReconfiguration,comCost):
    with open('results.log',"a") as resultFile:
        resultFile.write(logFile + '    ' + currentReconfiguration + '    ' + str(tClocks) + '    ' + str(tSimulation) + '    ' + str(comCost) + '    ' + str(tProgram) + '\n')







randKey1  = generateKey(config.nodeCount)         
randKey2  = generateKey(config.nodeCount)
randKey3  = generateKey(config.nodeCount)


currentReconfiguration = ""

for i in range(0,len(config.benchmarks)):
    logFile = config.benchmarks[i]    
    ConstnodeBenchmarkList = convXYtoNode(logFile)
    listLen = len(ConstnodeBenchmarkList)
    print config.benchmarksOnly[i]
    print '-----------------' + '\n'
    print 'ListLength:' + str(listLen)
    for reconfigs in range(0,5):
        startTime = time.time()
        nodeBenchmarkList = ConstnodeBenchmarkList
        reqCount = 0
        endFlag = False
        isover = False
        config.nodestate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        maxActiveReqLen = 0

        t = 0
        if reconfigs == 0:
            currentReconfiguration = "Numerical"
            

        if reconfigs == 1:
            nodeBenchmarkList = mapping(randKey1,nodeBenchmarkList)
            currentReconfiguration = "Random1"

        if reconfigs == 2:
            nodeBenchmarkList = mapping(randKey2,nodeBenchmarkList)
            currentReconfiguration = "Random2"

        if reconfigs == 3:
            nodeBenchmarkList = mapping(randKey3,nodeBenchmarkList)
            currentReconfiguration = "Random3"

        if reconfigs == 4:
            nNKey = nn.nearestNeighbourKeygen(nodeBenchmarkList)
            nodeBenchmarkList = mapping(nNKey,nodeBenchmarkList)
            currentReconfiguration = "nNeighbor"

        while isover == False:
            while  (t <= nodeBenchmarkList[reqCount][4] and endFlag==False):
                if reqCount+1 == listLen:
                    endFlag = True
                config.activeReq.append(request(nodeBenchmarkList[reqCount][0],nodeBenchmarkList[reqCount][1],nodeBenchmarkList[reqCount][3],nodeBenchmarkList[reqCount][4],nodeBenchmarkList[reqCount][4]))
                if endFlag == False:
                    reqCount += 1


            for req in config.activeReq:
                req.reqProcessing(t)
            t += 1*config.EccToOcc
            if (endFlag == True) & (len(config.activeReq) == 0) & (config.nodestate == [0] * config.nodeCount):
		isover = True


        tProgram = time.time()-startTime
        print config.nodestate 
        print '\n'
        print "Reconfiguration: " + currentReconfiguration
        print 'Optical Clock Cycles: '+ str(t)
        totalTime = float(t)/(config.OCC*(10**9))
        print 'Runtime: '+ str(totalTime) +'seconds'
        print 'ComCost: ' + str(config.comCost)
        print 'Time for Traffic: ' + str(tProgram)

        writeResults(config.benchmarksOnly[i], t,totalTime, tProgram,currentReconfiguration,config.comCost)
