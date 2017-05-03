SRC_PATH=$1
DST_PATH=$2
LABEL_PATH=$3

for FILE in $SRC_PATH/* ;
do
	fn=${FILE##*/}
	id=${fn%.*}
	infile=$FILE
	outfile=$DST_PATH/$id.csv
	labelfile=$LABEL_PATH/$id.label.csv
	python tools/data_script.py $infile $outfile
	python extract_samples.py $outfile $labelfile
	echo "processed $FILE"
done
