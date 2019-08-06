folderPath="$HOME/series"

for i in $@; do
	python3 ./main.py $folderPath$i
done

