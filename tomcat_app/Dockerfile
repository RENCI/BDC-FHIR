FROM bitnami/tomcat:9.0 AS tomcat

RUN rm -rf /opt/bitnami/tomcat/webapps/ROOT && \
    mkdir -p /opt/bitnami/hapi/data/hapi/lucenefiles && \
    chmod 775 /opt/bitnami/hapi/data/hapi/lucenefiles
#WORKDIR /app

#ARG OPENTELEMETRY_JAVA_AGENT_VERSION=1.31.0
#RUN curl -LSsO https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v${OPENTELEMETRY_JAVA_AGENT_VERSION}/opentelemetry-javaagent.jar
USER root
RUN mkdir -p /target && chown -R 1001:1001 target
USER 1001

COPY --chown=1001:1001 catalina.properties /opt/bitnami/tomcat/conf/catalina.properties
COPY --chown=1001:1001 server.xml /opt/bitnami/tomcat/conf/server.xml
COPY --chown=1001:1001 ROOT.war /opt/bitnami/tomcat/webapps/ROOT.war
#COPY --chown=1001:1001 opentelemetry-javaagent.jar /app
ENV ALLOW_EMPTY_PASSWORD=yes
#EXPOSE 8080 5432
EXPOSE 8080