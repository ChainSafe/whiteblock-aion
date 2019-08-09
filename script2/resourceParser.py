#!/usr/bin/env python

import json

'''
    aggerateData goes through the list of cpulogs for each node in cpu.log file.
    The function selects all dataPoints that are >= timeStamp and computes the average.
    
    timeStamp = TimeStamp of the block before the first block with transactions
    p = file path
'''
def aggerateData (p, timeStamp):
 
    cpuLog = open(p, "r")

    after2Min = {
        "cpuUsage": [],
        "ramUsage": [],
    }

    fullLength = {
        "cpuUsage": [],
        "cpuAvgs": [],
        "ramUsage": [],
        "ramAvgs": [],
        "timeStamps": []
    }

    i = 0

    for interval in cpuLog:
        
        nodes = json.loads(interval)
        totalNode = len(nodes)

        if (len(fullLength["cpuUsage"]) == 0):
            fullLength["cpuUsage"] = [[] for _ in range(totalNode)]
            fullLength["ramUsage"] = [[] for _ in range(totalNode)]
           
        for nodeIndex in range(totalNode):
            if nodes[nodeIndex]['timestamp'] >= int(timeStamp):
                fullLength["cpuUsage"][nodeIndex].append(nodes[nodeIndex]["resourceUse"]["cpu"])
                fullLength["ramUsage"][nodeIndex].append(nodes[nodeIndex]["resourceUse"]["residentSetSize"])


    for i in range(totalNode):
        avg = sum(fullLength["cpuUsage"][i])/len(fullLength["cpuUsage"][i])
        fullLength["cpuAvgs"].append(avg)
        
        avg = sum(fullLength["ramUsage"][i])/len(fullLength["ramUsage"][i])
        fullLength["ramAvgs"].append(avg)
    
    fullLength["cpuAvgUsage"] = sum(fullLength["cpuAvgs"])/len(fullLength["cpuAvgs"])
    fullLength["ramAvgUsage"] = sum(fullLength["ramAvgs"])/len(fullLength["ramAvgs"])
    

    return fullLength
