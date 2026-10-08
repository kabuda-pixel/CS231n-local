#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d cifar-10-batches-py ]; then
  curl --fail --location --retry 3 https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz --output cifar-10-python.tar.gz
  tar -xzf cifar-10-python.tar.gz
  rm cifar-10-python.tar.gz
fi
