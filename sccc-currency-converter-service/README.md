# Currency Converter SOAP Service

## Deployment
```
mvn clean install
```

This will produce a Docker image which can be used to deploy.
```
docker run -p 8080:8080 -p 4848:4848 --name currency-converter-service axoncallum/currency-converter-service
```
This will publish the port 8080 to the web service and 4848 to the admin interface.
The default username and password is both `admin`