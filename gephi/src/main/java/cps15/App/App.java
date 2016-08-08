package cps15.App;

import com.mongodb.*;
import com.mongodb.gridfs.GridFS;
import com.mongodb.gridfs.GridFSDBFile;
import com.mongodb.gridfs.GridFSInputFile;
import cps15.App.LayoutAlg.LayoutArgs;
import cps15.App.LayoutAlg.MsForceAtlas2Args;
import cps15.App.LayoutAlg.OpenOrdArgs;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.Properties;
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
    private static final String DEFAULT_CONFIG_FILE = "config.properties";

    private JSONParser jsonParser;
    private GridFS gridFS;
    private RabbitMQWrapper rabbitMQWrapper;
    private boolean healthy = true;

    private static String userName;
    private static String password;
    private static String host;
    private static int port;
    private static String authDB;

    public static void main(String[] args){

        Properties prop = new Properties();
        InputStream input = null;
        String configFile = DEFAULT_CONFIG_FILE;

        if(args.length > 0) {
            configFile = args[0];
        }
        logger.info("Using config file: " + configFile);

        try{
            input = new FileInputStream(configFile);
            prop.load(input);
            userName = prop.getProperty("username");
            password = prop.getProperty("password");
            host = prop.getProperty("host", "localhost");
            authDB = prop.getProperty("authDB", "admin");
            port = Integer.parseInt(prop.getProperty("port", "27017"));
            logger.info("Username: " + userName + ",host: " + host + ",authDB: " + authDB + ",port: " + port);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if(input!= null) {
                try{
                    input.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            } else {

                logger.severe("Could not load mongo username and password");
            }
        }

        App gephi_worker = null;
        try {
            gephi_worker = new App(host, port,userName, password, authDB);
        } catch (IOException | TimeoutException e) {
            e.printStackTrace();
            logger.log(Level.SEVERE, "Exception", e);
            return;
        }

        try {
            gephi_worker.run();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            logger.log(Level.SEVERE, "Exception", e);
        }

    }

    public App(String userName, String password) throws IOException, TimeoutException {
        this("localhost",27017, userName, password, "admin");
    }

    public App(String host, int port, String userName, String password, String authDB) throws IOException, TimeoutException {

        jsonParser = new JSONParser();
        MongoCredential credential = MongoCredential.createCredential(userName, authDB, password.toCharArray());
        DB db = new MongoClient(new ServerAddress(host, port), Arrays.asList(credential)).getDB(MONGO_DB);
        logger.info("Found collections " + db.getCollectionNames());
        try {
            db.command("ping");
        } catch (MongoTimeoutException e) {
            logger.severe("Could not ping the mongo host");
            throw new MongoTimeoutException("!!");
        }
        logger.info("Managed to ping the host");

        gridFS = new GridFS(db);
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

            JSONObject gephiParams = (JSONObject) arguments.get("GephiParameters");
            LayoutArgs layoutArgs;
            String layoutName = (String) gephiParams.getOrDefault("LAYOUT_ALGO", "FA2MS");

            switch (layoutName) {
                case OpenOrdArgs.LAYOUT_ALGO:
                    layoutArgs = new OpenOrdArgs(gephiParams);
                    break;
                case MsForceAtlas2Args.LAYOUT_ALGO:
                    layoutArgs = new MsForceAtlas2Args(gephiParams);
                    break;
                default:
                    return getResponse(fileName, false, "Unknown layout algorithm");
            }

            GephiWorker gephiWorker = new GephiWorker(layoutArgs);

            //Error checking here
            gephiWorker.importFile(file.getInputStream());
            gephiWorker.runLayout();

            GridFSInputFile gridFSInputFile = gridFS.createFile(gephiWorker.export(), fileName);
            gridFSInputFile.save();
            gephiWorker.clearWorkspace();

            return getResponse(fileName, true);
        } catch (Exception e) {
            e.printStackTrace();
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
