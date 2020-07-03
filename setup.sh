#!/usr/bin/env bash

# sudo sh -c "echo -n '[username]:' >> ${NGINX_FILES_PATH}/htpasswd/${VIRTUAL_HOST}"
# sudo sh -c "openssl passwd -apr1 >> ${NGINX_FILES_PATH}/htpasswd/${VIRTUAL_HOST}"

  
if [ -e .env ]; 
then 
    source .env
fi
# else 
    # echo "It seems you didn´t create your .env file, so we will create one for you."
    # cp .env.sample .env
    # exit 1
# fi

docker-compose -f "./easycouch-web-server/docker-compose.yml" down
docker-compose -f "./easycouch-stack/docker-compose.yml" down

cd easycouch-stack 
mkdir -p $APP_DIR{/rutorrent,/couchpotato,/sickchill,/plex,/jellyfin}
chgrp -R 101 $APP_DIR{/rutorrent,/couchpotato,/sickchill,/plex,/jellyfin}
chmod -R g+rwx $APP_DIR{/rutorrent,/couchpotato,/sickchill,/plex,/jellyfin}
cd ../easycouch-web-server 

mkdir -p $APP_DIR/web-server{/conf.d,/vhost.d,/html,/certs,/htpasswd}
chgrp -R 101 $APP_DIR/web-server \
             $APP_DIR/web-server{/conf.d,/vhost.d,/html,/certs,/htpasswd}
chmod -R g+rwx $APP_DIR/web-server \
               $APP_DIR/web-server{/conf.d,/vhost.d,/html,/certs,/htpasswd} 


echo  username ??
read username
echo It\'s nice to meet you $username  
sh -c "echo -n "$username:" >> $APP_DIR/web-server/htpasswd/${RUTORRENT_URL}"
sh -c "openssl passwd -apr1 >> $APP_DIR/web-server/htpasswd/${RUTORRENT_URL}"

cd ..


docker-compose -f "./easycouch-web-server/docker-compose.yml" up -d --build
docker-compose -f "./easycouch-stack/docker-compose.yml" up -d --build


 
   
# chown abc:abc $APP_DIR{/rutorrent,/couchpotato,/sickchill,/plex,/jellyfin}
 
# mkdir -p \
# 	/config{/log/rtorrent,/log/rutorrent,/rtorrent/rtorrent_sess,/rutorrent/settings/users} \
# 	/config/rutorrent/profiles{/settings,/torrents,/users,/tmp} \
# 	/downloads{/completed,/incoming,/watched,/done}/{/Movies,/TV} \
# 	/run/php
# echo $APP_DIR
# mkdir -p $APP_DIR/apps{/couchpotato2/jellyfin}
# mkdir -p $APP_DIR/apps2 
# echo $APP_DIR/apps2 

# # 2. Create docker network
# docker network create $NETWORK $NETWORK_OPTIONS

# # 3. Verify if second network is configured
# if [ ! -z ${SERVICE_NETWORK+X} ]; then
#     docker network create $SERVICE_NETWORK $SERVICE_NETWORK_OPTIONS
# fi

# # 4. Download the latest version of nginx.tmpl
# curl https://raw.githubusercontent.com/jwilder/nginx-proxy/master/nginx.tmpl > nginx.tmpl

# # 5. Update local images
# docker-compose pull

# # 6. Add any special configuration if it's set in .env file

# # Check if user set to use Special Conf Files
# if [ ! -z ${USE_NGINX_CONF_FILES+X} ] && [ "$USE_NGINX_CONF_FILES" = true ]; then

#     # Create the conf folder if it does not exists
#     mkdir -p $NGINX_FILES_PATH/conf.d

#     # Copy the special configurations to the nginx conf folder
#     cp -R ./conf.d/* $NGINX_FILES_PATH/conf.d

#     # Check if there was an error and try with sudo
#     if [ $? -ne 0 ]; then
#         sudo cp -R ./conf.d/* $NGINX_FILES_PATH/conf.d
#     fi

#     # If there was any errors inform the user
#     if [ $? -ne 0 ]; then
#         echo
#         echo "#######################################################"
#         echo
#         echo "There was an error trying to copy the nginx conf files."
#         echo "The proxy will still work with default options, but"
#         echo "the custom settings your have made could not be loaded."
#         echo 
#         echo "#######################################################"
#     fi
# fi 

# # 7. Start proxy

# # Check if you have multiple network
# if [ -z ${SERVICE_NETWORK+X} ]; then
#     docker-compose up -d
# else
#     docker-compose -f docker-compose-multiple-networks.yml up -d
# fi

# exit 0














# mkdir -p data/certs
# mkdir data/htpasswd
# mkdir data/conf.d
# mkdir data/vhost.d
# mkdir data/html
# chgrp -R 101 data
# chmod -R g+rwx data