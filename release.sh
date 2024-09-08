#!/usr/bin/bash

set -eo pipefail

SELF=$(readlink -f "$0")
DIR=$(dirname "$SELF")

cd "$DIR"

if [ -e tmp/release ]; then
    rm -r tmp/release
fi

mkdir -p tmp/release

cp blender_manifest.toml tmp/release
cp io_import_pixelart.py tmp/release/__init__.py

pushd tmp/release

blender --command extension build

pkg=$(echo io_import_pixelart-*.zip)

mv "$pkg" ../..

popd

echo "Created $pkg"
