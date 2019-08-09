#!/usr/bin/env python
import os
import json
import sys

from nodeParser import aggerateData
from resourceParser import aggerateData as aggerateSystemData

# NOTE: directory Represents where all the tests are
directory = os.fsencode(sys.argv[1])
# NOTE: TPS must match with the prescribed tps 
TPS = 200

results = {}
blockParsing = False

'''
    Goes through all the blocks.json files in the test directory
    and stores the final result in 'info.txt' file.
    
    info format
    Chain Metrics
    <avgBlockSize>
    <avgBlockTime>
    <EstimatedTxSent>
    <TxSuccessRate>
    <avgTxThroughPut>
    <TimeStamp of first block with transactions>
'''
for subdir, dirs, files in os.walk(directory):

    for file in files:
        path = os.path.join(subdir, file)

        if "blocks.json" in str(file):
            stats, fullstats = aggerateData(path.decode("utf-8"), TPS)
            
            d = os.path.dirname(path)
            seriesNam  = os.path.dirname(os.path.dirname(d))

            seriesPath = os.path.abspath(d)
            newFile = seriesNam.decode("utf-8")  + "/info.txt"
            f = open(newFile, "w+")
            f.write("Chain Metrics \n")
            f.write(str(stats['avgBlockSize']) + '\n')
            f.write(str(stats['avgBlockTime']) + '\n')
            f.write(str(stats['txSent']) + '\n')
            f.write(str(stats['txSuccessRate']) + '\n')
            f.write(str(stats['avgTxThroughPut']) + '\n')
            f.write(str(stats['TimeStampOfStartBlock'])+'\n')
            f.close()

            newFile = seriesNam.decode("utf-8")  + "/graphMetrics.txt"
            f = open(newFile, "w+")
            f.write("----------------\n")
            f.write("BlockSizes:\n")
            f.write(str(stats['blockSizes']) + "\n")
            f.write("BlockTime:\n")
            f.write(str(stats['blockTime'])+ "\n")
            f.write("BlockTxThroughPut:\n")
            f.write(str(stats['txThroughPut'])+ "\n")
            f.write("TimeStamps:\n")
            f.write(str(stats['timestamps'])+ "\n")
            f.write("totalTransactions per block:\n")
            f.write(str(stats['totalTransactions'])+ "\n")
            f.write("--------------------\n")
            f.close()

'''
    Goes through all the cpu.log and datadir_size.log files.
    Extracts the timeStamp of the first block with transactions from info.txt on line 7 
    
    Collects all the valid dataPoints and adds the final result in info.txt
'''
for subdir, dirs, files in os.walk(directory):

    for file in files:
        path = os.path.join(subdir, file)
        if "cpu.log" in str(file):
            d = os.path.dirname(path)
            seriesPath = os.path.abspath(d)

            timeStamp = '0' 
            try:
                chainMetrics = open(seriesPath.decode("utf-8")+"/info.txt", "r")
                lines = chainMetrics.readlines()
            
                if lines[6].isdigit():
                        timeStamp = lines[6]
                chainMetrics.close()
            except:
                print("Bad Block. No blocks were evaluated in" + seriesPath.decode("utf-8"))


            stats = aggerateSystemData(seriesPath.decode("utf-8")+"/cpu.log", timeStamp)

            d = os.path.dirname(path)
            seriesPath = os.path.abspath(d)
            # newFile = seriesPath.decode("utf-8")  + "/resMetrics.txt"
            newFile = seriesPath.decode("utf-8")  + "/info.txt"

            # newFile = os.path.join(str(seriesPath), "info.txt")
            f = open(newFile, "a+")
            f.write("-----------------------\n")
            f.write("CPU/RAM metrics \n")
            f.write(str(stats['cpuAvgUsage']) + '\n' )
            f.write(str(stats['ramAvgUsage']) + '\n' )
            f.write("-----------------------\n")
            f.close()

            newFile = seriesNam.decode("utf-8")  + "/graphMetrics.txt"
            f = open(newFile, "a+")
            f.write("-----------------------\n")
            f.write("CPUsage Per NODE: \n")
            f.write(str(stats["cpuUsage"]) + '\n')
            f.write("RAMUsage Per NODE: \n")
            f.write(str(stats['ramUsage']) + '\n')
            f.write("TimeStamps for each usage:\n")
            f.write(str(stats['timeStamps']) + '\n')
            f.write("Average Cpu Usage per node : \n"+ str(stats['cpuAvgs']) + '\n')
            f.write("Average Ram Usage per node : \n"+ str(stats['ramAvgs']) + '\n')
            f.write("-----------------------\n")
            f.close()

            
            dirSizeFile = open(seriesPath.decode("utf-8")+"/datadir_size.log", 'r')
            sizes = dirSizeFile.readlines()
            validSizes = []
            validStamps = []
            for line in sizes:
                info = line.split(" ")
                # 0 -> size,  1 -> timestamp
                if int(info[1]) >= int(timeStamp):
                    validSizes.append(int(info[0]))
                    validStamps.append(int(info[1]))
            
            dataDirAvg = sum(validSizes)/len(validSizes)

            newFile = seriesPath.decode("utf-8")  + "/info.txt"
            f = open(newFile, "a+")
            f.write("-----------------------\n")
            f.write("Directory Size\n")
            f.write("Avg DataDir size:" + str(dataDirAvg) + "\n")
            f.write("-----------------------\n")
            
            f.close()

            newFile = seriesNam.decode("utf-8")  + "/graphMetrics.txt"
            f = open(newFile, "a+")
            f.write("-----------------------\n")
            f.write("Directory Sizes:\n" + str(validSizes) + '\n')
            f.write("Size Stamps:\n" + str(validStamps) + '\n')
 
print("...Completed...")


