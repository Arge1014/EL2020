#!/bin/bash
echo 'Type a word'
read var1
if [${#var1} -gt 8]
then
	echo "Thats a long word"
#elif ${var1}<2
#	echo'That is a one letter word'
else
	echo "That is a shortish word"
fi
echo 'Have a nice day :)'
