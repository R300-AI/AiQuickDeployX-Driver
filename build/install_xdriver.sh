WORK_DIR=$(readlink -f .)     #from root to work_dir
echo ${WORK_DIR}
docker rmi -f xdriver
docker rm -f xdriver
docker build -f ./docker/Dockerfile . -t xdriver
#docker run --name xdriver --link mongodb:mongo -p 5000:5000 -v ${WORK_DIR}/Xdriver/data:/workspace/data -it xdriver
docker run --name xdriver --link mongodb:mongo -p 5000:5000 -v ${WORK_DIR}/Xdriver/data:/workspace/Xdriver/data -it xdriver