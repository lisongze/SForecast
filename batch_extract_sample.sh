SRC_PATH=$1
DST_PATH=$2

echo $SRC_PATH
echo $DST_PATH

for FILE in $SRC_PATH/* ;
do
	fn=${FILE##*/}
	id=${fn%.*}
	infile=$FILE
	outfile=$DST_PATH/$id.csv
	python tools/data_script.py $infile $outfile
	echo "processed $FILE"
done
