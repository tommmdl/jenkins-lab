FROM jenkins/jenkins:lts-jdk21
RUN jenkins-plugin-cli --plugins workflow-aggregator git timestamper
COPY jenkins/init.groovy /usr/share/jenkins/ref/init.groovy.d/01-lab.groovy
