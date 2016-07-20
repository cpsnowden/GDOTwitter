package cps15.App;

import com.mongodb.MongoClient;
import com.mongodb.gridfs.GridFS;
import com.mongodb.gridfs.GridFSDBFile;
import com.mongodb.gridfs.GridFSInputFile;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.IOException;
import java.util.concurrent.TimeoutException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Created by ChrisSnowden on 17/07/2016.
 */
public class App {
    private static final Logger logger = Logger.getLogger(App.class.getName());
    private static final String MONGO_HOST = "";
    private static final String MONGO_DB = "FILE_DATA";

    private JSONParser jsonParser;
    private GridFS gridFS;
    private RabbitMQWrapper rabbitMQWrapper;
    private boolean healthy = true;

    public static void main(String[] args){

        App gephi_worker = null;
        try {
            gephi_worker = new App();
        } catch (IOException e) {
            e.printStackTrace();
            logger.log(Level.SEVERE, "Exception", e);
            return;
        } catch (TimeoutException e) {
            e.printStackTrace();
            logger.log(Level.SEVERE, "Exception", e);
            return;
        }

        try {
            gephi_worker.run();
        } catch (IOException e) {
            e.printStackTrace();
            logger.log(Level.SEVERE, "Exception", e);
        } catch (InterruptedException e) {
            e.printStackTrace();
            logger.log(Level.SEVERE, "Exception", e);
        }

    }

    public App() throws IOException, TimeoutException {

        jsonParser = new JSONParser();
        gridFS = new GridFS(new MongoClient().getDB(MONGO_DB));
        rabbitMQWrapper = new RabbitMQWrapper();

    }

    private void run() throws IOException, InterruptedException {

        rabbitMQWrapper.start();
        while(healthy) {
            String response = process(rabbitMQWrapper.get());
            rabbitMQWrapper.basicPublish(response);
        }
        logger.severe("Stopping consuming as not longer healthy");

    }

    private String process(String message) {

            JSONObject arguments = parseArguments(message);
            if (arguments == null) {
                return getResponse("Unknown", false, "Could not parse arguments");
            }

            String fileName = (String) arguments.get("fileName");
        try {
            GridFSDBFile file = gridFS.findOne(fileName);

            GephiArguments gephiArguments = new GephiArguments().loadFromJSON((JSONObject) (arguments.get("GephiParameters")));

            GephiWorker gephiWorker = new GephiWorker(gephiArguments);

            //Error checking here
            gephiWorker.importFile(file.getInputStream());
            gephiWorker.runLayout();

            GridFSInputFile gridFSInputFile = gridFS.createFile(gephiWorker.export(), fileName);
            gridFSInputFile.save();

            return getResponse(fileName, true);
        } catch (Exception e) {
            return getResponse(fileName, false, e.getMessage());
        }
    }

    private static String getResponse(String fileName, boolean status) {
        return getResponse(fileName, status, "");
    }

    private static String getResponse(String fileName, boolean status, String details) {

        JSONObject response = new JSONObject();

        response.put("fileName", fileName);
        response.put("status", status?"sucess":"failed");
        response.put("details", details);

        return response.toJSONString();
    }

    private JSONObject parseArguments(String json) {

        try {
            return  (JSONObject) jsonParser.parse(json);
        } catch (ParseException e) {
            e.printStackTrace();
            return null;
        }

    }
}
