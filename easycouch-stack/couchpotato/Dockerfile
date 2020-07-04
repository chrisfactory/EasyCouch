
FROM lsiobase/alpine:3.12 AS base
LABEL maintainer="chrisfactory" 
# set python to use utf-8 rather than ascii.
ENV PYTHONIOENCODING="UTF-8"
RUN apk add --no-cache python2   
RUN mkdir -p /app/couchpotato


FROM lsiobase/alpine:3.12 AS gitSrc
WORKDIR /src 
RUN apk add --no-cache git
RUN git clone https://github.com/Cyberden/CouchPotatoServer.git couchpotato
RUN git clone https://github.com/linuxserver/docker-couchpotato.git dockercouchpotato
WORKDIR "/src"

  
FROM lsiobase/alpine:3.12 AS transform
WORKDIR /src  
COPY --from=gitSrc /src/couchpotato . 

 
#Add sarcher
COPY patch/couchpotato/core/media/_base/providers/torrent/. ./couchpotato/core/media/_base/providers/torrent
COPY patch/couchpotato/core/media/movie/providers/torrent/. ./couchpotato/core/media/movie/providers/torrent

COPY patch/couchpotato/core/media/_base/providers/nzb/. ./couchpotato/core/media/_base/providers/nzb

COPY patch/couchpotato/core/_base/. ./couchpotato/core/_base/ 
COPY patch/couchpotato/core/downloaders/. ./couchpotato/core/downloaders/ 
  
COPY patch/couchpotato/core/media/_base/searcher/. ./couchpotato/core/media/_base/searcher
COPY patch/couchpotato/core/plugins/. ./couchpotato/core/plugins/ 

WORKDIR "/src"
  



FROM base as final 
COPY --from=gitSrc /src/dockercouchpotato/root /
COPY --from=transform /src /app/couchpotato
EXPOSE 5050
WORKDIR /app/couchpotato
VOLUME /config /downloads /movies
