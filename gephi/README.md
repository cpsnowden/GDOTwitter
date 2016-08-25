# GephiWorker

The MongoHost, Post and Authentication settings should be added to a properties file and passed as the first argument when running. Currently as the the Gephi workers are running on a seperate machine to the RabbitMQ exchange, open an ssh tunnel from the
Gephi machine to the Celery machine and  forward port 5672 using for example:

```bash
ssh -4  -L 5672:127.0.0.1:5672 cloud-vm-45-56.doc.ic.ac.uk
```

## Dependencies
All dependencies are managed by Maven, no additional required

## To Run
Run using Maven Jetty.
```bash
mvn exec:java -Dexec.args="config_remote.properties"
```

