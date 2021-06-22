#!/bin/bash
# This script will sync up GPU data from LENGAU
# mkdir logs
pushd logs
rsync -arvz --progress -e ssh krishna@scp.chpc.ac.za:/mnt/lustre3p/logs/gpu .
popd
