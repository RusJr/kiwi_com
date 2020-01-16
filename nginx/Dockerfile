FROM nginx:1.16.0

ENV TZ=Asia/Almaty
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /tmp/static/ /tmp/socket
ADD nginx.conf /etc/nginx/nginx.conf
