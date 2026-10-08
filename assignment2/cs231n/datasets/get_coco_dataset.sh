#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d coco_captioning ]; then
  curl --fail --location --retry 3 https://cs231n.stanford.edu/coco_captioning.zip --output coco_captioning.zip
  unzip -q coco_captioning.zip
  rm coco_captioning.zip
fi
