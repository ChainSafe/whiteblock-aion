#!/usr/bin/env python

import json

'''
    aggerateData goes through the list of blocks in the blocks.json file.
    - The parser starts collecting datapoints after the first block with transactions
      have been hit (fullLength)
    - The index of the block with a timeStamp approximately 120s from the first blockWithTx is
       marked (a2min)
    - Once the parser goes through the list, the actual test run dataPoint are extracted using a2min and are
     stored into (after2Min)
'''

def aggerateData(p, tps):
    with open(p, 'r') as f:
        nodeInfo = json.load(f)

    fullLength = {
        "blockSizes": [],
        "totalTransactions": [],
        "txThroughPut": [],
        "timestamps": [],
        "blockTime": [],
        "blockNumber": []
    }

    initialStamp = int(nodeInfo[0]['timestamp'], 0)
    previousStamp = int(nodeInfo[0]['timestamp'], 0)
    startStamp = 0
    index = 0

    a2min = 0
    txCheck = False

    for blockInfo in nodeInfo:
        timeStamp = int(blockInfo['timestamp'], 0)
        blockSize = int(blockInfo['size'], 0)
        totalTransactions = len(blockInfo['transactions'])
        blockNumber = blockInfo['number']

        if totalTransactions > 0 and not txCheck:
            txCheck, initialStamp = True, timeStamp
            previousBlockIndex = blockNumber - 2
            previousStamp = int(nodeInfo[previousBlockIndex]['timestamp'], 0)

        if txCheck:

            fullLength['blockSizes'].append(blockSize)
            fullLength["blockTime"].append(timeStamp - previousStamp)
            fullLength["timestamps"].append(timeStamp)
            fullLength["totalTransactions"].append(totalTransactions)
            fullLength["blockNumber"].append(blockNumber)


            fullLength["txThroughPut"].append(totalTransactions)
            if fullLength['blockTime'][-1] != 0:
                fullLength["txThroughPut"][-1] = totalTransactions/fullLength['blockTime'][-1]

            previousStamp = int(blockInfo['timestamp'], 0)
            diff = (timeStamp - initialStamp)

            if (diff >= 120):
                diff1 = abs(diff - 120)
                diff2 = abs(120 - (timeStamp - fullLength["timestamps"][-2]))

                # initialStamp = Timestamp of the first blockWithTx
                # diff1 = how close the current timeStamp is to the 120 mark from initialStamp
                # diff2 = how close is the timeStamp of the pervious block to the 120 mark from initialStamp

                if startStamp == 0:
                    a2min = index
                    startStamp = -1
                    if diff2 < diff1:
                        a2min = index - 1
            index += 1

    startIndex = fullLength["blockNumber"][a2min] - 1
    intervalStart = int(nodeInfo[startIndex]['timestamp'], 0)
    intervalEnd = int(nodeInfo[-1]['timestamp'], 0)

    txSent = tps * (intervalEnd - intervalStart)

    after2Min = {
        "blockSizes": fullLength['blockSizes'][a2min:],
        "totalTransactions": fullLength['totalTransactions'][a2min:],
        "timestamps": fullLength['timestamps'][a2min:],
        "blockTime": fullLength['blockTime'][a2min:],
        "txThroughPut": fullLength['txThroughPut'][a2min:],
        "txSent": txSent
    }

    after2Min['avgBlockSize'] = sum(after2Min['blockSizes']) / len(after2Min["blockSizes"])
    after2Min['avgBlockTime'] = sum(after2Min['blockTime']) / len(after2Min["blockTime"])
    after2Min['txSuccessRate'] = sum(after2Min['totalTransactions']) / txSent
    after2Min['avgTxThroughPut'] = sum(after2Min['totalTransactions']) / (intervalEnd - intervalStart)
    after2Min['TimeStampOfStartBlock'] = intervalStart

    return after2Min, fullLength
