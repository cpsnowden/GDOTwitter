package cps15.App;

import cps15.App.LayoutAlg.LayoutArgs;
import cps15.App.LayoutAlg.Layouts;
import cps15.App.LayoutAlg.OpenOrdArgs;
import org.gephi.graph.api.GraphController;
import org.gephi.graph.api.GraphModel;
import org.gephi.graph.api.UndirectedGraph;
import org.gephi.io.exporter.api.ExportController;
import org.gephi.io.exporter.spi.CharacterExporter;
import org.gephi.io.exporter.spi.Exporter;
import org.gephi.io.importer.api.Container;
import org.gephi.io.importer.api.ImportController;
import org.gephi.io.processor.plugin.DefaultProcessor;
import org.gephi.layout.plugin.AutoLayout;
import org.gephi.layout.spi.Layout;
import org.gephi.project.api.ProjectController;
import org.gephi.project.api.Workspace;
import org.openide.util.Lookup;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.logging.Logger;

public class GephiWorker {
    private static final Logger logger = Logger.getLogger(GephiWorker.class.getName());

    private ProjectController pc;
    private Workspace workspace;
    private GraphModel graphModel;
    private LayoutArgs layoutArgs;
    private boolean performanceMonitor = false;
    private List<Long> nanoStepTimes = new ArrayList<>();
    public GephiWorker(LayoutArgs layoutArgs) {

        pc = Lookup.getDefault().lookup(ProjectController.class);
        pc.newProject();
        this.workspace = pc.getCurrentWorkspace();
        this.layoutArgs = layoutArgs;
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


    public void runLayout(String fileName) {

        logger.info("Attempting to run layout");
        Layout layout = Layouts.getLayout(graphModel, layoutArgs);
        Long layoutIterations = layoutArgs.getLayoutIterations();
        logger.info("Running layout for " + layoutIterations + " steps");
//        int j = 0;
//        for(Node n: graphModel.getUndirectedGraph().getNodes()) {
//            System.out.println(n.x());
//            if(j++ > 10) break;
//        }

        long prev_time = System.nanoTime();
        long duration = 0;
        if(null != layout) {
            for (int i = 0; i < layoutIterations; i++) {
                if(!layout.canAlgo()) {
                    logger.info("Stopping algorithm at step " + i);
                    break;
                }

                layout.goAlgo();
                duration = System.nanoTime() - prev_time;
                logger.info("Took " + duration);
                if(performanceMonitor){
                    nanoStepTimes.add(duration);
                }

                if (i % 100 == 0) {
                    logger.info("Step " + i);
                }
                prev_time = System.nanoTime();
            }
            layout.endAlgo();
            logger.info("Finished running layout");
            if(performanceMonitor){
                logger.info("Writing performance file");
                try {
                    FileWriter writer = new FileWriter("Performance_" + fileName + ".dat");
                    writer.write("[");
                    for(Long l:nanoStepTimes){
                        writer.write(l + ",");
                    }
                    writer.write("-1]");
                    writer.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
//        j = 0;
//        for(Node n: graphModel.getUndirectedGraph().getNodes()) {
//            System.out.println(n.x());
//            if(j++ > 10) break;
//        }
    }

    public void clearWorkspace() {
        pc.closeCurrentWorkspace();
        this.workspace = pc.newWorkspace(pc.getCurrentProject());
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
