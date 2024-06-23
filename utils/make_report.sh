#!/bin/sh

sudo docker run --rm --volume "$(pwd):/data" --user "$(id -u):$(id -g)" pandoc/extra ./docs/report.md -o ./report.pdf --template eisvogel --listings --toc
