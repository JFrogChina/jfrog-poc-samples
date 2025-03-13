FROM demo.jfrogchina.com/slash-docker-virtual/docker-framework:latest

LABEL MAINTAINER="Alex Wang"

RUN rm -rf /home/exec/tomcat/webapps/*

ADD target/app-boot-*.war /home/exec/tomcat/webapps/ROOT.war

CMD /bin/bash -c cd /home/exec; /home/exec/tomcat/bin/catalina.sh run
