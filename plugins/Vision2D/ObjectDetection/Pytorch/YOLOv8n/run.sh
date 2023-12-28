#!/bin/bash
while getopts u:d:l:o: flag
do
    case "${flag}" in
        u) USERNAME=${OPTARG};;
        d) DATASET=${OPTARG};;   #資料集來源的絕對路徑
        l) LOG=${OPTARG};;       #Log檔的絕對路徑
        o) OUTPUT=${OPTARG};;    #輸出資料夾的絕對路徑
    esac
done
WORK_DIR=$(readlink -f .)     #from root to work_dir
MODULE_DIR=$(dirname "$0")    #from work_dir to run.sh

# Config Image
echo "Start to build ${MODULE_NAME} docker..."
DATASET_NAME=$(python3 -c "data='${DATASET}'; print(data.split('/')[-1])")
MODULE_NAME=$(python3 -c "import json; data='${MODULE_DIR}'.split('/'); print(data[-2].lower() + '_' + data[-2].lower())")
CONTAINER_NAME=$(python3 -c "print('${USERNAME}_${DATASET_NAME}_${MODULE_NAME}'.replace('/','_'))")

docker rmi -f $MODULE_NAME    
docker rm -f $CONTAINER_NAME 
docker build -f $MODULE_DIR/docker/Dockerfile . -t $MODULE_NAME
echo "${MODULE_NAME} docker has been build."

# Run Container
echo "Start to run ${MODULE_NAME} docker..."

DATASET_DIR=$(python3 -c "module_dir = '${MODULE_DIR}'.replace('${WORK_DIR}', ''); print('${WORK_DIR}' + module_dir + '${DATASET}'.split('${MODULE_DIR}')[-1])")
LOG_DIR=$(python3 -c "module_dir = '${MODULE_DIR}'.replace('${WORK_DIR}', ''); print('${WORK_DIR}' + module_dir + '${LOG}'.split('${MODULE_DIR}')[-1])")
OUTPUT_DIR=$(python3 -c "module_dir = '${MODULE_DIR}'.replace('${WORK_DIR}', ''); print('${WORK_DIR}' + module_dir + '${OUTPUT}'.split('${MODULE_DIR}')[-1])")
ENGINE_DIR=$(python3 -c "module_dir = '${MODULE_DIR}'.replace('${WORK_DIR}', ''); print('${WORK_DIR}' + module_dir + '/engine')")

docker container run --name $CONTAINER_NAME -it -v $OUTPUT_DIR:/usr/src/ultralytics/benchmark -v $DATASET_DIR:/usr/src/ultralytics/dataset -v $ENGINE_DIR:/usr/src/ultralytics/engine $MODULE_NAME | tee -a $LOG_DIR
