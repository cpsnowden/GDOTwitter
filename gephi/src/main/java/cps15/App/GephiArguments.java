//package cps15.App;
//
//
//import org.json.simple.JSONObject;
//
//import java.util.HashMap;
//import java.util.Map;
//import java.util.logging.Logger;
//
//
///**
// * Created by ChrisSnowden on 17/07/2016.
// */
//
//public class GephiArguments{
//    private static final Logger logger = Logger.getLogger(GephiWorker.class.getName());
//    private static final Double LAYOUT_SCALE = 2.0;
//    private static final Boolean BARNES_HUT_OPTIMIZE = true;
//    private static final Double BARNES_HUT_THETA = 1.2;
//    private static final Boolean STRONGER_GRAVITY = true;
//    private static final Double GRAVITY = 1.0;
//    private static final Boolean ADJUST_SIZES = true;
//    private static final Long LAYOUT_ITERATIONS = 10000L;
//    private static final Double EDGE_WEIGHT_INFLUENCE = 1.0;
//    private static final Integer THREADS_COUNT = 7;
//    private static final Double GRAVITY_X_SCALING = 1.0;
//    private static final Double GRAVITY_Y_SCALING = 1.0;
//    private static final String LAYOUT_ALGO = "FA2MS";
//
//    private Map<String, Object> settings = new HashMap<String, Object>();
//
//    public GephiArguments() {
//
//        settings.put("LAYOUT_SCALE", LAYOUT_SCALE);
//        settings.put("BARNES_HUT_OPTIMIZE", BARNES_HUT_OPTIMIZE);
//        settings.put("BARNES_HUT_THETA", BARNES_HUT_THETA);
//        settings.put("STRONGER_GRAVITY", STRONGER_GRAVITY);
//        settings.put("GRAVITY", GRAVITY);
//        settings.put("ADJUST_SIZES", ADJUST_SIZES);
//        settings.put("LAYOUT_ITERATIONS", LAYOUT_ITERATIONS);
//        settings.put("EDGE_WEIGHT_INFLUENCE", EDGE_WEIGHT_INFLUENCE);
//        settings.put("THREADS_COUNT", THREADS_COUNT);
//        settings.put("GRAVITY_X_SCALING", GRAVITY_X_SCALING);
//        settings.put("GRAVITY_Y_SCALING", GRAVITY_Y_SCALING);
//        settings.put("LAYOUT_ALGO", LAYOUT_ALGO);
//
//    }
//
//    public GephiArguments loadFromJSON(JSONObject jsonObject) {
//
//        if(null != jsonObject) {
//            logger.info("Received the following custom arguments " + jsonObject.toJSONString());
//            for(Object key: jsonObject.keySet()) {
//                String strKey = (String) key;
//                if(settings.containsKey(strKey)) {
//                    settings.put(strKey, jsonObject.get(key));
//                }
//            }
//        }
//
//        return this;
//    }
//
//    public Double getGravityXScaling() {
//        return (Double) settings.get("GRAVITY_X_SCALING");
//    }
//
//    public Double getGravityYScaling() {
//        return (Double) settings.get("GRAVITY_Y_SCALING");
//    }
//
//    public Double getLayoutScale() {
//        return (Double) settings.get("LAYOUT_SCALE");
//    }
//
//    public Boolean getBarnesHuttOptimize() {
//        return (Boolean) settings.get("BARNES_HUT_OPTIMIZE");
//    }
//
//    public Double getBarnesHutTheta() {
//        return (Double) settings.get("BARNES_HUT_THETA");
//    }
//
//    public Boolean getStrongerGravity() {
//        return (Boolean) settings.get("STRONGER_GRAVITY");
//    }
//
//    public Double getGravity() {
//        return (Double) settings.get("GRAVITY");
//    }
//
//    public Boolean getAdjustSizes() {
//        return (Boolean) settings.get("ADJUST_SIZES");
//    }
//
//    public Long getLAYOUT_ITERATIONS() {
//        return (Long) settings.get("LAYOUT_ITERATIONS");
//    }
//
//    public Double getEdgeWeightInfluence() {
//        return (Double) settings.get("EDGE_WEIGHT_INFLUENCE");
//    }
//
//    public Integer getThreadsCount() {
//        return (Integer) settings.get("THREADS_COUNT");
//    }
//
//    public String getLayoutAlgo() {
//        return (String) settings.get("LAYOUT_ALGO");
//    }
//
//}
