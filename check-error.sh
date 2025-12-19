#!/bin/bash

mkdir  /tmp/dir3/dir2 

if [ $? -eq 0 ]
  then 
	echo "Dir created"
  else
	echo " Error $? "
        exit 1
fi
ls -al /tmp/dir1
echo "Dane"
