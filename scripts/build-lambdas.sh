#!/bin/sh

for i in "./lambdas/"*
do
	pkg=`basename "$i"`
	echo "Building $pkg"
	mkdir -p "./build/lambda.$pkg"
	if [ -f "$i/requirements.txt" ]; then
		pip3 install --target "./build/lambda.$pkg" -r "$i/requirements.txt"
	fi
	cp -rp "$i/"* "./build/lambda.$pkg/"
done
