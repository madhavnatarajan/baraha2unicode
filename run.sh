for file in inputs/TS*.docx
do
	python3 baraha2unicode.py "${file}"
done
