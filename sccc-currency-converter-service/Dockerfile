FROM glassfish:4.1-jdk8


# ADAPTED FROM: https://github.com/AdamBien/docklands/issues/20
# 4848 - admin interface
# 8080 - web port over HTTP
# 8181 - HTTPS
RUN echo "--- Setup the password file ---" && \
    echo "AS_ADMIN_PASSWORD=" > /tmp/glassfishpwd && \
    echo "AS_ADMIN_NEWPASSWORD=admin" >> /tmp/glassfishpwd  && \
    echo "--- Enable DAS, change admin password, and secure admin access ---" && \
    asadmin --user=admin --passwordfile=/tmp/glassfishpwd change-admin-password --domain_name domain1 && \
    asadmin start-domain && \
    echo "AS_ADMIN_PASSWORD=admin" > /tmp/glassfishpwd && \
    asadmin --user=admin --passwordfile=/tmp/glassfishpwd enable-secure-admin && \
    asadmin --user=admin stop-domain && \
    rm /tmp/glassfishpwd

COPY target/*.war $GLASSFISH_HOME/glassfish/domains/domain1/autodeploy/ccs.war

EXPOSE 8080