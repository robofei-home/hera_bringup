#!/bin/sh

echo 'Criando backup no diretório "originais"...'
mkdir originais && mv *.jpg originais

echo 'Transformando imagens para tons de cinza no diretório "gray"...'
cp originais gray -r
mogrify -type Grayscale gray/*.jpg
mkdir gray/100
mv gray/*.jpg gray/100

echo 'Redimensionando em 75%...'
cp gray/100 gray/75 -r && mogrify -resize 75% gray/75/*.jpg
echo 'Redimensionando em 50%...'
cp gray/100 gray/50 -r && mogrify -resize 50% gray/50/*.jpg
echo 'Redimensionando em 25%...'
cp gray/100 gray/25 -r && mogrify -resize 25% gray/25/*.jpg
echo 'Redimensionando em 10%...'
cp gray/100 gray/10 -r && mogrify -resize 10% gray/10/*.jpg
echo 'Redimensionando em 5%...'
cp gray/100 gray/5 -r && mogrify -resize 5% gray/5/*.jpg

echo 'Concluído'
