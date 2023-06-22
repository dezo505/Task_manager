#!/bin/bash
if ! python --version &> /dev/null
then
    echo "Python is not installed."
    exit 1
fi

if ! pip --version &> /dev/null
then
    echo "Pip is not installed."
    exit 1
fi

pip install -r requirements.txt

python ../main.py
