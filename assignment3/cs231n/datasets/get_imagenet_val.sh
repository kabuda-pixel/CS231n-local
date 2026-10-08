#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -f imagenet_val_25.npz ]; then
  curl --fail --location --retry 3 https://cs231n.stanford.edu/imagenet_val_25.npz --output imagenet_val_25.npz
fi
