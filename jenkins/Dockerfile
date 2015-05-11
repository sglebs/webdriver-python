FROM jenkins
MAINTAINER marcio@betterdeveloper.net
ENV REFRESHED_AT 2015-05-11
COPY plugins.txt /plugins.txt
RUN /usr/local/bin/plugins.sh /plugins.txt
COPY config.xml $JENKINS_HOME/jobs/webdriver-python/config.xml
USER root
RUN chown -R jenkins:jenkins $JENKINS_HOME/jobs/webdriver-python/
