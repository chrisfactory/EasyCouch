
cd easycouch-web-server
docker-compose -f "docker-compose.yml" down
docker-compose -f "docker-compose.yml" up -d --build

cd ../easycouch-stack 
docker-compose -f "docker-compose.yml" down
docker-compose -f "docker-compose.yml" up -d --build

# sudo sh -c "echo -n '[username]:' >> ${NGINX_FILES_PATH}/htpasswd/${VIRTUAL_HOST}"
# sudo sh -c "openssl passwd -apr1 >> ${NGINX_FILES_PATH}/htpasswd/${VIRTUAL_HOST}"