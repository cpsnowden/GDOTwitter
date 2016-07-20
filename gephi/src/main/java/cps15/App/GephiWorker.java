package cps15.App;

import cps15.ForceAtlas2MS.ForceAtlas2;
import cps15.ForceAtlas2MS.ForceAtlas2Builder;
import org.gephi.graph.api.GraphController;
import org.gephi.graph.api.GraphModel;
import org.gephi.graph.api.UndirectedGraph;
import org.gephi.io.exporter.api.ExportController;
import org.gephi.io.exporter.spi.CharacterExporter;
import org.gephi.io.exporter.spi.Exporter;
import org.gephi.io.importer.api.Container;
import org.gephi.io.importer.api.ImportController;
import org.gephi.io.processor.plugin.DefaultProcessor;
import org.gephi.layout.spi.Layout;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.openide.util.Lookup;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.io.StringWriter;
import java.nio.charset.StandardCharsets;
import java.util.logging.Logger;

public class GephiWorker {
    private static final Logger logger = Logger.getLogger(GephiWorker.class.getName());

    private Workspace workspace;
    private GephiArguments gephiArguments;
    private GraphModel graphModel;

    public GephiWorker(GephiArguments gephiArguments) {

        ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
        pc.newProject();
        this.workspace = pc.getCurrentWorkspace();
        this.gephiArguments = gephiArguments;
    }

    public boolean importFile(InputStream inputStream) {

        logger.info("Attempting to import file from gridfs input stream");

        ImportController importController = Lookup.getDefault().lookup(ImportController.class);
        Container container = importController.importFile(inputStream, importController.getFileImporter("graphml"));
        importController.process(container, new DefaultProcessor(), workspace);
        this.graphModel = Lookup.getDefault().lookup(GraphController.class).getGraphModel();

        UndirectedGraph uG = graphModel.getUndirectedGraph();

        logger.info("Imported file, resulting graph has " + uG.getNodeCount() + " nodes and " + uG.getEdgeCount() + " edges ");

        return true;
    }

    public Layout get_layout(String layoutAlgo){

        logger.info("Getting layout algorithm: " + layoutAlgo);

        if(layoutAlgo.equals("FA2MS")) {

            ForceAtlas2 layout = new ForceAtlas2Builder().buildLayout();
            layout.setGraphModel(this.graphModel);
            layout.initAlgo();
            layout.resetPropertiesValues();
            layout.setScalingRatio(this.gephiArguments.getLAYOUT_SCALE());
            layout.setBarnesHutOptimize(this.gephiArguments.getBARNES_HUTT_OPTIMIZE());
            layout.setBarnesHutTheta(this.gephiArguments.getBARNES_HUT_THETA());
            layout.setStrongGravityMode(this.gephiArguments.getSTRONGER_GRAVITY());
            layout.setGravity(this.gephiArguments.getGRAVITY());
            layout.setAdjustSizes(this.gephiArguments.getADJUST_SIZES());
            layout.setEdgeWeightInfluence(this.gephiArguments.getEDGE_WEIGHT_INFLUENCE());
            layout.setThreadsCount(this.gephiArguments.getTHREADS_COUNT());
            layout.setGravityXRatio(this.gephiArguments.getGravityXScaling());
            layout.setGravityYRatio(this.gephiArguments.getGravityYScaling());
            return layout;

        } else {
            return null;
        }

    }

    public void runLayout() {

        logger.info("Attempting to run layout");

        Layout layout = get_layout(this.gephiArguments.getLayoutAlgo());
        Long layout_iterations = this.gephiArguments.getLAYOUT_ITERATIONS();

        logger.info("Running layout for " + layout_iterations + " steps");
        for (int i = 0; i < layout_iterations; i++) {
            layout.goAlgo();
            if(i%100==0){
                logger.info("Step " + i);
            }
        }
        layout.endAlgo();
        logger.info("Finished running layout");
    }

    public InputStream export() {

        ExportController exportController = Lookup.getDefault().lookup(ExportController.class);

        Exporter exporter = exportController.getExporter("graphml");
        exporter.setWorkspace(this.workspace);
        StringWriter stringWriter = new StringWriter();
        exportController.exportWriter(stringWriter, (CharacterExporter) exporter);
        logger.info("Exporting directly to gridfs");

        return new ByteArrayInputStream(stringWriter.toString().getBytes(StandardCharsets.UTF_8));

    }
}
