package cps15.App.LayoutAlg;

import cps15.App.GephiWorker;
import org.json.simple.JSONObject;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Created by ChrisSnowden on 28/07/2016.
 */
public abstract class LayoutArgs {

    private static final Logger logger = Logger.getLogger(LayoutArgs.class.getName());
    protected Map<String, Object> settings = new HashMap<>();

    public LayoutArgs() {
    }

    public LayoutArgs(JSONObject jsonObject) {
        getDefaults();
        loadFromJSON(jsonObject);
    }

    public void loadFromJSON(JSONObject jsonObject) {
        if(null != jsonObject) {
            logger.info("Received the following custom arguments " + jsonObject.toJSONString());
            for(Object key: jsonObject.keySet()) {
                String strKey = (String) key;
                if(settings.containsKey(strKey)) {
                    settings.put(strKey, jsonObject.get(key));
                }
            }
        }
        logger.log(Level.INFO, this.toString());
    }

    @Override
    public String toString() {
        String str = "";

        for(String i : settings.keySet()){
            str += "(" + i + ":" + settings.get(i).toString() + ")";
        }
        return str;
    }


    public abstract String getLayoutAlgo();

    public abstract void getDefaults();

    public abstract Long getLayoutIterations();
}
