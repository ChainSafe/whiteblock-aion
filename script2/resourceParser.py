#!/usr/bin/env python
# Performance Metrics
# Block Size: Measure the average block size; plot the block size over time.
# Block time: Measure the average block time; plot the blocktime over time.
# Transaction Throughput: Measure the average throughput of transactions; plot the throughput over time.
# Tx Success Rate: Measure the number of transactions that have been sent and how many were included in blocks by the end of the test; plot the percentage of unsuccessful transactions over time.
'''

Per node:
    cpuAvg = sum(cpuUsage at each timestamp after delay)/total_dataPoints
    ramAvg = sum(ramUsage at each timestamp after delay)/total_dataPoints
    
'''
import json

def aggerateData (p):
 
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
    }

    i = 0

    for interval in cpuLog:
        
        nodes = json.loads(interval)
        totalNode = len(nodes)

        if (len(fullLength["cpuUsage"]) == 0):
            fullLength["cpuUsage"] = [[] for _ in range(totalNode)]
            fullLength["ramUsage"] = [[] for _ in range(totalNode)]
           
        for nodeIndex in range(totalNode):
            fullLength["cpuUsage"][nodeIndex].append(nodes[nodeIndex]["resourceUse"]["cpu"])
            fullLength["ramUsage"][nodeIndex].append(nodes[nodeIndex]["resourceUse"]["residentSetSize"])
            # print(nodeIndex)


    for i in range(totalNode):
        avg = sum(fullLength["cpuUsage"][i])/len(fullLength["cpuUsage"][i])
        fullLength["cpuAvgs"].append(avg)
        
        avg = sum(fullLength["ramUsage"][i])/len(fullLength["ramUsage"][i])
        fullLength["ramAvgs"].append(avg)
    
    fullLength["cpuAvgUsage"] = sum(fullLength["cpuAvgs"])/len(fullLength["cpuAvgs"])
    fullLength["ramAvgUsage"] = sum(fullLength["ramAvgs"])/len(fullLength["ramAvgs"])
    

    return fullLength
# cpu = "/Users/master/Documents/Professional/whiteblock/script/series_1b.1_2019-07-19T19:03:16/cpu.log"
