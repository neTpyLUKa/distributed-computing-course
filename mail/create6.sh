#!/bin/bash

for i in $(seq 0 5);
do
    ./setup.sh email add "${i}@localhost.com" qwerty
done

