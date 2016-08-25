# Management Web-App

Management web-app consumes main API. Allows control over:
1. Data set creation: launch new streams, stop and pause existing ones or delete collections
2. Spin up Twitter additional twitter consumers if Twitter stream filter is broad
3. Launch analytics tasks: kick off new analytics tasks and download the results including viewing charts in place
4. Create predefined slides for the GDO app.


## Dependencies
All dependencies are managed by Maven, no additional required

## To Run
Run using Maven Jetty.
```bash
mvn jetty:run
```

