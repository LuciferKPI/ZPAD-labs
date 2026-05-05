#!/bin/bash
# Створення папки build та компіляція проєкту
mkdir -p build
cd build
cmake ..
make