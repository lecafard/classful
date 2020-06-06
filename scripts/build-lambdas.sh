#!/bin/sh

for i in "./lambdas/"*
do
	pkg=`basename "$i"`
	echo "Building $pkg"
	pip3 install --target "./build/lambda.$pkg" -r "$i/requirements.txt"
	cp -rp "$i/"* "./build/lambda.$pkg"
done
