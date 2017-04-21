#!/bin/bash
while read line
do
    /usr/bin/expect remote.exp ${line}
done < abc.conf
