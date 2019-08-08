#!/usr/bin/env python
'''
Metrics for single test
    Average Block size:  sum(each block_size)/total_blocks

    blockTime(n) = timeStamp(n) - timeStamp(n-1)
    Average Block Time:  sun(block_time for each block)/total_blocks

    txSent = tps * (time_of_test_run after delay)
    txSuccessRate = (totalTrasnactionsInBlock/txSent)

    txThroughPut = totalTransactionsInBlock/blockTime
    avgTxThroughPut = sum(txThroughPut for each block)/total_blocks 

'''

import json

def aggerateData (p, tps):
    with open(p, 'r') as f:
        nodeInfo = json.load(f)

    testInitialDelay = 120

    fullLength = {
        "blockSizes": [],
        "totalTransactions": [],
        "txThroughPut": [],
        "timestamps" : [],
        "blockTime" : [],
        "blockNumber": []
    }


    initialStamp = int(nodeInfo[0]['timestamp'], 0)
    previousStamp = int(nodeInfo[0]['timestamp'], 0)
    startStamp = 0
    index = 0
    txStartIndex = 0

    a2min = 0
    txCheck = False
    # print("Total Block Length", len(nodeInfo), "\n")
    for blockInfo in nodeInfo:
        timeStamp = int(blockInfo['timestamp'], 0)
        blockSize = int(blockInfo['size'], 0)
        totalTransactions = len(blockInfo['transactions'])
        blockNumber = blockInfo['number']
        
        if totalTransactions > 0 and not txCheck:
            txCheck, initialStamp = True, timeStamp
            previousBlockIndex =blockNumber - 2
            previousStamp = int(nodeInfo[previousBlockIndex]['timestamp'], 0)


        if txCheck:
            
            fullLength['blockSizes'].append(blockSize)
            fullLength["blockTime"].append(timeStamp - previousStamp)
            fullLength["timestamps"].append(timeStamp)
            fullLength["totalTransactions"].append(totalTransactions)
            fullLength["blockNumber"].append(blockNumber)

            # fullLength["txThroughPut"].append(totalTransactions)
            # if fullLength['blockTime'][-1] != 0:
            #     fullLength["txThroughPut"][-1] = totalTransactions/fullLength['blockTime'][-1]

            previousStamp = int(blockInfo['timestamp'],0)
            diff = (timeStamp - initialStamp)


            # First Block with transactions + 120 = Start of test Interval
            if (diff >= 120):
                diff1 = abs(120 - diff)
                diff2 = abs(120 - (timeStamp -  fullLength["timestamps"][-2]))

                if startStamp == 0:
                    a2min = index
                    txStartIndex = blockNumber = blockInfo['number'] - 1
                    startStamp = -1
                    if diff2 < diff1:
                        a2min = index - 1
            index += 1
    
    startIndex = fullLength["blockNumber"][a2min] -1
    intervalStart = int(nodeInfo[startIndex]['timestamp'], 0)
    intervalEnd = int(nodeInfo[-1]['timestamp'], 0)

    txSent = tps * (intervalEnd - intervalStart)
    # print("time", intervalEnd - intervalStart, "seconds \n")
    # print("TxSent", txSent, "\n")

    after2Min = {
        "blockSizes": fullLength['blockSizes'][a2min:],
        "totalTransactions": fullLength['totalTransactions'][a2min:],
        "timestamps" : fullLength['timestamps'][a2min:],
        "blockTime" : fullLength['blockTime'][a2min:],
        "txSent": txSent
    }

    # print("After 2MIN blocks", after2Min['blockSizes'], "\n")
    
    
    after2Min['avgBlockSize'] = sum(after2Min['blockSizes'])/len(after2Min["blockSizes"])
    after2Min['avgBlockTime'] = sum(after2Min['blockTime'])/len(after2Min["blockTime"])
    after2Min['txSuccessRate'] = sum(after2Min['totalTransactions'])/txSent
    after2Min['avgTxThroughPut'] = sum(after2Min['totalTransactions'])/(intervalEnd - intervalStart)
    after2Min['TimeStampOfStartBlock'] = intervalStart


    # print("Avg block size", after2Min['avgBlockSize'], "\n" )
    # print("Avg Block time", after2Min['avgBlockTime'], "seconds \n")
    # print("Avg Tx Throughput", after2Min['avgTxThroughPut'], "\n")
    # print("Tx success rate", (after2Min['txSuccessRate'])*100, "%\n")

    return after2Min, fullLength

# initialPath = "/Users/master/Documents/Professional/whiteblock/whiteblock-parser/script/test/"
# check = "/Users/master/Documents/Professional/whiteblock/Test/series_2a.1_2019-07-30T22:53:10/nodes/fb921383-af49-4e86-9a57-82b51ec1f381/blocks.json"
# testPath = "/Users/priom/Desktop/ChainSafe/whiteblock-aion/script2/blocks.json"

# aggerateData(testPath, 200)
