import nn
import config

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


def mapping(key, benchmark):
    for row in benchmark:
        row[0]=key[row[0]]
        row[1]=key[row[1]]

    return benchmark
  
  
def writeNNDictionary(nnDict):
    with open('nnKeyDictionary.log',"a") as nnKeyDict:
        for i in range(len(nnDict)):
	    nnKeyDict.write(str(nnDict[i][0]) + '    ' + str(nnDict[i][1]) + '\n' )   

nnDict = []
  
for i in range(0,len(config.benchmarks)):
    logFile = config.benchmarks[i]    
    nodeBenchmarkList = convXYtoNode(logFile)  
    nNKey = nn.nearestNeighbourKeygen(nodeBenchmarkList)
    nnDict.append([config.benchmarksOnly[i], nNKey])
    
writeNNDictionary(nnDict)



