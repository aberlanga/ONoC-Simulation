import config

class request:
	# This is the initializer for the request class
    def __init__(self, sourceNode, destNode, volume, timeStamp,timeTrack,lastReqFlag):
        self.sourceNode     = sourceNode
        self.destNode       = destNode
        self.volume         = volume
        self.timeStamp      = timeStamp
        self.timeTrack      = timeStamp
        self.lastReqFlag    = lastReqFlag
        self.scheduled      = False
        #self.transmitted    = False
        self.right          = False





    def schedule(self):
		# makes source lower than destination
        if self.sourceNode > self.destNode:
            temp = self.sourceNode
            self.sourceNode = self.destNode
            self.destNode = temp 
            

		# checks for shortest path
		# first if triggers if direct (e.g. 123...14 15 16) path is the shortest or equadistant, elif triggers if opposite direction path is shorter
        if (self.destNode - self.sourceNode) <= (config.nodeCount - self.destNode + self.sourceNode):
			# checks that path is available and if so reserves path
            if (config.nodestate[self.sourceNode:(self.destNode +1)] == [False] * (self.destNode +1 - self.sourceNode)):     
                config.nodestate[self.sourceNode:(self.destNode +1)] = [1] * ((self.destNode +1) - self.sourceNode)
                self.scheduled = True
                self.timeTrack += config.tInitialize # insert time parameters
                self.right = True
                


            elif (config.nodeCount - self.destNode + self.sourceNode) < config.weighted_cutoff:
                if (config.nodestate[0:(self.sourceNode +1)] == [False] * (self.sourceNode +1)) & (config.nodestate[self.destNode:] == [False] * (config.nodeCount - self.destNode)):
                    for i in config.nodestate:
                        if i <= self.sourceNode | i >= self.destNode:
                            config.nodestate[i] = 1
                    self.scheduled = True
                    self.timeTrack += config.tInitialize # insert time parameters
                else:
                    self.timeTrack += 1
            else:
                self.timeTrack += 1
        else:
            if (config.nodestate[0:(self.sourceNode +1)] == [False] * (self.sourceNode +1)) & (config.nodestate[self.destNode:] == [False] * (config.nodeCount - self.destNode)):
                for i in config.nodestate:
                    if i <= self.sourceNode | i >= self.destNode:
                        config.nodestate[i] = 1
                self.scheduled = True
                self.timeTrack += config.tInitialize # insert time parameters
            elif (self.destNode - self.sourceNode) < config.weighted_cutoff:
                if config.nodestate[self.sourceNode:(self.destNode +1)] == [False] * (self.destNode +1 - self.sourceNode):     
                    config.nodestate[self.sourceNode:(self.destNode +1)] = [1] * ((self.destNode +1) - self.sourceNode)
                    self.scheduled = True
                    self.timeTrack += config.tInitialize # insert time parameters
                    self.right = True
                else:
                    self.timeTrack += 1

            else:
                self.timeTrack += 1


        #Transmission here
        if self.scheduled == True:
            dataTransTime = self.volume*config.packetSize/(config.OCC*(10**9)) 
            self.timeTrack += config.tChannelAloc + dataTransTime #insert addition parameters
            #self.transmitted = True




    def delete_self(req):
        config.activeReq.remove(req)



    # def transmit(self):
    #     volume = self.volume
    #     dataTransTime = volume*config.packetSize/(config.OCC*(10**9)) 
    #     self.timeTrack += config.tCloseChannels + config.tOpenChannels + dataTransTime #insert addition parameters
    #     self.transmitted = True



    def release(self):
        if self.right == True:
            config.nodestate[self.sourceNode:(self.destNode +1)] = [0] * ((self.destNode +1) - self.sourceNode)
        else:
            for i in config.nodestate:
                    if i <= self.sourceNode | i >= self.destNode:
                        config.nodestate[i] = 0
        if self.lastReqFlag:
            config.isover = True
        self.delete_self()
    


    def reqProcessing(self, t):
        if self.scheduled == False:
            self.schedule()
            
        # if (self.transmitted == False) & self.scheduled == True):
        #     self.transmit()
            
        if (self.scheduled == True) & (self.timeTrack <= t):
            self.release()




    pass




    
