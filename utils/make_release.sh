#!/bin/sh

set -eu

URL="https://github.com/LucaBarban/progettobasimod2.git"
NAME="progettobasimod2"
DIR="/tmp/$NAME"

[ -d "$DIR" ] && rm -rf "$DIR"

git clone --filter=blob:none "$URL" "$DIR"

cd "$DIR"

rm -rf ./.*
mkdir -p ./app/static/covers
python ./utils/images.py
sh ./utils/make_report.sh
cat ./utils/db.sql ./utils/insert.sql >./db.sql
rm -rf ./utils
rm -rf ./docs
rm ./env-sample
rm ./compose.yml
rm ./LICENSE
rm ./*.md

zip -r "$HOME/Downloads/scratchdevs.zip" .

echo "ALL DONE"
