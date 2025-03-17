#!/bin/bash


AFL_DIR="../../../Benchmarks/baselines/AFL++"

for subdir in "$AFL_DIR"/*/; do
	if [ -d "$subdir/fuzz/" ]; then
		rm -rf "$subdir/fuzz/"
	fi
	folder_dir=$(basename "$subdir")
	(cd "$subdir" && nohup /bin/bash ./runFuzz.sh > /dev/null 2>&1 &)
	echo "started runFuzz.sh in $folder_dir"
done





