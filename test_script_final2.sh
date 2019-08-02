#!/bin/bash -xeu
COMMAND=whiteblock
WAIT_TIME=300

NODES=30
IMAGE=gcr.io/whiteblock/aion:master
BANDWIDTH=1000
ACCOUNTS=50
PACKET_LOSS=0
LATENCY=0
TPS=200
CPU_LIMIT=2
MEM_LIMIT=0
TX_SIZE=200
RETRY_DELAY=5
RETRIES=10


TMUX=

retry_run() {
	n=0
	set -e
	until [ $n -ge $RETRIES ]
	do
		$@ && break  
		n=$[$n+1]
		sleep $RETRY_DELAY
	done
	set +e
}

run_test() {
	sudo docker restart genesis rpc
	local dir=series_$1_$(date +"%FT%T"| tr -d '[:space:]')
	OUTPUT_FILE=$dir/cpu.log
	OUTPUT_FILE_FOR_DATADIR_SIZE=$dir/datadir_size.log
	tmux new -s cpu_recorder -d; tmux send-keys "while :; do NO_PRETTY=1 ./whiteblock get nodes; sleep 5 | tee $OUTPUT_FILE; done" C-m

	echo "Running Tests"
	retry_run $COMMAND build -b aion -n $NODES -c $CPU_LIMIT -m $MEM_LIMIT -i $IMAGE -y
	sleep 10
	echo "Build complete"

	retry_run $COMMAND netconfig all -d $LATENCY -l $PACKET_LOSS -b $BANDWIDTH

	retry_run $COMMAND tx start stream -v 1 -t $TPS --size $TX_SIZE
	sleep $WAIT_TIME
	echo stopping tx stream
	retry_run $COMMAND tx stop
	retry_run $COMMAND export --local --dir $dir
	tmux kill-session -t cpu_recorder
}


run_case() {
	for i in {1..3}
	do
		run_test $1.$i
	done
}

reset_vars() {
	# Defaults to contol case specs
	LATENCY=0
	PACKET_LOSS=0
	BANDWIDTH=1000
	NODES=30 #clients
	ACCOUNTS=15 #Sender accounts
	TX_SIZE=200
	TPS=200
}

for i in $@; do

	reset_vars
	case "$i" in
		1)
			# Control Case
			run_case 1a
			run_case 1b
			run_case 1c
			;;
		2)
			# Network Latency Test
			ACCOUNTS=12

			LATENCY=50
			run_case 2a
			LATENCY=100
			run_case 2b
			LATENCY=150
			run_case 2c
			;;
		3)
			# Packet Loss
			NODES=24
			ACCOUNTS=12

			PACKET_LOSS=0.01
			run_case 3a
			PACKET_LOSS=0.1
			run_case 3b
			PACKET_LOSS=1
			run_case 3c
			;;
		4)
			# V Bandwidth test
			BANDWIDTH=10
			run_case 4a
			BANDWIDTH=50
			run_case 4b
			BANDWIDTH=100
			run_case 4c
			;;
		5)
			# V Increase Network Latency
			LATENCY=200
			run_case 5a
			LATENCY=300
			run_case 5b
			LATENCY=400
			run_case 5c
			;;
		6)
			# V Stress Test
			LATENCY=150
			PACKET_LOSS=0.01
			BANDWIDTH=10
			TPS=500

			run_case 6a
			run_case 6b
			run_case 6c
			;;
		7)
			# V Transaction Size
			TX_SIZE=500
			run_case 7a
			TX_SIZE=750
			run_case 7b
			TX_SIZE=1000
			run_case 7c
			;;
		8)
			# V Transaction Count
			LATENCY=0
			PACKET_LOSS=0

			BANDWIDTH=10
			TPS=300
			run_case 8a

			BANDWIDTH=50
			TPS=400
			run_case 8b

			BANDWIDTH=100
			TPS=500
			run_case 8c
			;;
		9)
			# V Sending Account
			LATENCY=0
			PACKET_LOSS=0
			BANDWIDTH=1000

			ACCOUNTS=20
			run_case 9a

			ACCOUNTS=25
			run_case 9b

			ACCOUNTS=30
			run_case 9c
			;;

		*)
			echo "Enter a valid case#"
			;;
	esac
done
