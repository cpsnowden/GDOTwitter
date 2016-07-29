package cps15.App.LayoutAlg;

import org.json.simple.JSONObject;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by ChrisSnowden on 28/07/2016.
 */
public class OpenOrdArgs extends LayoutArgs {


    public static final String LAYOUT_ALGO = "OPENORD";

    private static final Integer LIQUID_STAGE = 25;
    private static final Integer EXPANSION_STAGE = 25;
    private static final Integer COOLDOWN_STAGE = 25;
    private static final Integer CRUNCH_STAGE = 10;
    private static final Integer SIMMER_STAGE = 15;
    private static final Float EDGE_CUT = 0.8F;
    private static final Integer THREADS_COUNT = 7;
    private static final Integer INTERNAL_LAYOUT_ITERATIONS = 750;
    private static final Long LAYOUT_ITERATIONS = 750L;
    private static final Float REAL_TIME = 0.2F;

    public OpenOrdArgs(JSONObject jsonObject) {
        super(jsonObject);
    }

    public void getDefaults() {

        settings.put("LIQUID_STAGE", LIQUID_STAGE);
        settings.put("EXPANSION_STAGE", EXPANSION_STAGE);
        settings.put("COOLDOWN_STAGE", COOLDOWN_STAGE);
        settings.put("CRUNCH_STAGE", CRUNCH_STAGE);
        settings.put("SIMMER_STAGE", SIMMER_STAGE);
        settings.put("EDGE_CUT", EDGE_CUT);
        settings.put("THREADS_COUNT", THREADS_COUNT);
        settings.put("INTERNAL_LAYOUT_ITERATIONS", INTERNAL_LAYOUT_ITERATIONS);
        settings.put("LAYOUT_ITERATIONS", LAYOUT_ITERATIONS);
        settings.put("REAL_TIME", REAL_TIME);

    }

    public Integer getLiquidStage() {
        return (Integer) settings.get("LIQUID_STAGE");
    }

    public Integer getExpansionStage() {
        return (Integer) settings.get("EXPANSION_STAGE");
    }

    public Integer getCooldownStage() {
        return (Integer) settings.get("COOLDOWN_STAGE");
    }

    public Integer getCrunchStage() {
        return (Integer) settings.get("CRUNCH_STAGE");
    }

    public Integer getSimmerStage() {
        return (Integer) settings.get("SIMMER_STAGE");
    }

    public Float getEdgeCut() {
        return (Float) settings.get("EDGE_CUT");
    }

    public Integer getInteralLayoutIterations() {
        return (Integer) settings.get("INTERNAL_LAYOUT_ITERATIONS");
    }


    public Integer getThreadsCount() {
        return (Integer) settings.get("THREADS_COUNT");
    }

    public Float getRealTime() {
        return (Float) settings.get("REAL_TIME");
    }

    @Override
    public Long getLayoutIterations() {
        return (Long) settings.get("LAYOUT_ITERATIONS");
    }

    @Override
    public String getLayoutAlgo() {
        return LAYOUT_ALGO;
    }

}
