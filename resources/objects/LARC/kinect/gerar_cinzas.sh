#!/bin/sh

echo 'Criando backup no diretório "originais"...'
mkdir originais && mv *.png originais

echo 'Transformando imagens para tons de cinza no diretório "gray"...'
cp originais gray -r
mogrify -type Grayscale gray/*.png
mkdir gray/100
mv gray/*.png gray/100

echo 'Redimensionando em 75%...'
cp gray/100 gray/75 -r && mogrify -resize 75% gray/75/*.png
echo 'Redimensionando em 50%...'
cp gray/100 gray/50 -r && mogrify -resize 50% gray/50/*.png
echo 'Redimensionando em 25%...'
cp gray/100 gray/25 -r && mogrify -resize 25% gray/25/*.png
echo 'Redimensionando em 10%...'
cp gray/100 gray/10 -r && mogrify -resize 10% gray/10/*.png
echo 'Redimensionando em 5%...'
cp gray/100 gray/5 -r && mogrify -resize 5% gray/5/*.png

echo 'Concluído'
