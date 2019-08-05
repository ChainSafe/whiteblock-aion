# whiteblock-aion

# Running Test script
```
./test_script_final2.sh <test_series_number>
ex:
  ./test_script_final2.sh 1 2 3 4 5

The above will run test_series 1 - 5
```


# Parser
## nodeParser.py
Goes through all files named blocks.json, and returns the analysis of the blocks that existed in the file.

**Metrics Calculated**
+ avgBlockTime
+ avgBlockSize
+ avgTxSuccessRate
+ avgTxThroughPut

## resourceParser.py
Goes through all files named cpu.log, and returns the analysus of the cpu & ram usage by each node

**Metrics Calculated**
+ avgCPUUsage per Node
+ avgRamUsage per Node

All metric calculation formulas have been specified in metricCalculations.txt file


## main.py
+ Takes the path to the test directory that needs parsing
```
./main.py /home/master/series1
or
./main.py /home/master/series1a.1<otherInfo>
```
+ Goes through all the files in the director, and analyzes all blocks.json & cpu.log files.
+ Generates two files **info.txt** & **resMetrics.txt** within each series_* * . * directory
++ info.txt contains block metrics for the respective test
++ resMetrics.txt contains resource metrics for the respective test

** if the tps for a specific series is different, then the TPS variable in main.py need to be modified with the right amount.

## parser.sh
+ Script was made to automate the usage of main.py.
+ Can run main.py on multiple series with the same TPS configuration

**Setup**
++ Modify $folderPath with the desired path

+ Send in series name as arguments.

USAGE:
```
# All the series_1* test runs exists in the folder home/master/series1
# All the series_2* test runs exists in the folder home/master/series2
# All the series_3* test runs exists in the folder home/master/series3
...
if we wanted to parse test_series 1 - 3 
we can set the folderPath = "home/master/series"
Run :
  ./parser.sh 1 2 3
  
or if we wanted to run a specific section of a specific series (say series1)
we can set the folderPath = "home/master/series1/series_1a."
Run:
  ./parser.sh 1 2
 
The above will run the parser on series_1a.1 and series_1a.2
```


 


