FROM tomcat:9.0-jdk11 AS tomcat

# Create a non-root user similar to Bitnami's UID 1001
RUN groupadd -g 1001 tomcat \
 && useradd -u 1001 -g tomcat -s /bin/bash -m tomcat

# Prepare writable directories
RUN mkdir -p /target \
 && chown -R 1001:1001 /target /usr/local/tomcat

USER 1001

# Copy Tomcat configuration
COPY catalina.properties /usr/local/tomcat/conf/catalina.properties
COPY server.xml /usr/local/tomcat/conf/server.xml

# Deploy application
COPY ROOT.war /usr/local/tomcat/webapps/ROOT.war

EXPOSE 8080
