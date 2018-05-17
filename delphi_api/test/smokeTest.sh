#!/bin/bash

docker kill delphiapi_delphi_api_1 > /dev/null
docker kill delphiapi_db_1 > /dev/null
docker-compose up -d db > /dev/null
docker-compose up -d delphi_api > /dev/null

docker exec -it delphiapi_delphi_api_1 python migrate.py > /dev/null

MAINRESPONSE="$(./touchMainEndpoint.sh)"
STAKERESPONSE="$(./touchSeededStake.sh)"


if [[ $(< mainOut) == "$MAINRESPONSE" ]]
then
    echo "Main Endpoint Succeeded"
else
    echo "!Main Endpoint Failed!"
fi


if [[ $(< stakeOut) == "$STAKERESPONSE" ]]
then
    echo "Stake Endpoint Succeeded"
else
    echo "!Stake Endpoint Failed!"
fi
