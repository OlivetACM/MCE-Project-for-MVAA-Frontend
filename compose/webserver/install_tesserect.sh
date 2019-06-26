#!/usr/bin/env bash

sudo apt-get install libpng-dev libjpeg-dev libtiff-dev zlib1g-dev
sudo apt-get install gcc g++
sudo apt-get install autoconf automake libtool checkinstall

wget http://www.leptonica.org/source/leptonica-1.73.tar.gz
tar -zxvf leptonica-1.73.tar.gz
cd leptonica-1.73
./configure
make
sudo checkinstall
sudo ldconfig

cd ~
git clone https://github.com/tesseract-ocr/tesseract.git
cd tesseract
./autogen.sh
./configure
make
sudo make install
sudo ldconfig