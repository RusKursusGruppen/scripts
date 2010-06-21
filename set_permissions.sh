#!/bin/sh
set -e
chgrp -R rkg *
chmod g+rw -R *
echo "Updated read/write permissions for group rkg."
