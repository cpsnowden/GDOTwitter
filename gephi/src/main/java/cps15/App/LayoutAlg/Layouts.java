package cps15.App.LayoutAlg;

import cps15.ForceAtlas2MS.ForceAtlas2;
import cps15.ForceAtlas2MS.ForceAtlas2Builder;
import org.gephi.graph.api.GraphModel;
import org.gephi.layout.plugin.openord.OpenOrdLayout;
import org.gephi.layout.plugin.openord.OpenOrdLayoutBuilder;
import org.gephi.layout.spi.Layout;

import java.util.logging.Logger;

/**
 * Created by ChrisSnowden on 28/07/2016.
 */
public class Layouts {
    private static final Logger logger = Logger.getLogger(Layouts.class.getName());
    public static Layout getLayout(GraphModel graphModel, LayoutArgs layoutArgs) {
        logger.info("Using layout " + layoutArgs.getLayoutAlgo());
        switch (layoutArgs.getLayoutAlgo()) {
            case MsForceAtlas2Args.LAYOUT_ALGO: {

                ForceAtlas2 layout = new ForceAtlas2Builder().buildLayout();
                MsForceAtlas2Args args = (MsForceAtlas2Args) layoutArgs;
                layout.setGraphModel(graphModel);
                layout.resetPropertiesValues();
                layout.setScalingRatio(args.getLayoutScale());
                layout.setBarnesHutOptimize(args.getBarnesHuttOptimize());
                layout.setBarnesHutTheta(args.getBarnesHutTheta());
                layout.setStrongGravityMode(args.getStrongerGravity());
                layout.setGravity(args.getGravity());
                layout.setAdjustSizes(args.getAdjustSizes());
                layout.setEdgeWeightInfluence(args.getEdgeWeightInfluence());
//                layout.setThreadsCount(args.getThreadsCount());
                layout.setGravityXRatio(args.getGravityXScaling());
                layout.setGravityYRatio(args.getGravityYScaling());
                layout.setLinLogMode(args.getLinLogMode());
                layout.setAdjustSizes(args.getPreventOverlap());
                layout.initAlgo();
                logger.info("Scaling Ratio " + layout.getScalingRatio());
                logger.info("Barnes Hut " + layout.isBarnesHutOptimize());
                logger.info("Barnes Hut Theta " + layout.getBarnesHutTheta());
                logger.info("Strong Gravity " + layout.isStrongGravityMode());
                logger.info("Gravity " + layout.getGravity());
                logger.info("Adjust Size " + layout.isAdjustSizes());
                logger.info("LinLog Mode " + layout.isLinLogMode());
                return layout;
            }
            case OpenOrdArgs.LAYOUT_ALGO: {
                OpenOrdArgs args = (OpenOrdArgs) layoutArgs;
                OpenOrdLayout layout =  new OpenOrdLayout(new OpenOrdLayoutBuilder());
                layout.setGraphModel(graphModel);
                layout.resetPropertiesValues();
                layout.initAlgo();
//                layout.setLiquidStage(args.getLiquidStage());
//                layout.setExpansionStage(args.getExpansionStage());
//                layout.setCooldownStage(args.getCooldownStage());
//                layout.setCrunchStage(args.getCrunchStage());
//                layout.setSimmerStage(args.getSimmerStage());
//                layout.setEdgeCut(args.getEdgeCut());
//                layout.setNumThreads(args.getThreadsCount());
//                layout.setNumIterations(args.getInteralLayoutIterations());
//                layout.setRealTime(args.getRealTime());
                return layout;
            }
        }


        return null;
    }



}
