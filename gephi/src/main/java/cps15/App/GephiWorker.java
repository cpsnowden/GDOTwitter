package cps15.App;

import cps15.App.LayoutAlg.LayoutArgs;
import cps15.App.LayoutAlg.Layouts;
import org.gephi.graph.api.GraphController;
import org.gephi.graph.api.GraphModel;
import org.gephi.graph.api.Node;
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
    private GraphModel graphModel;
    private LayoutArgs layoutArgs;

    public GephiWorker(LayoutArgs layoutArgs) {

        ProjectController pc = Lookup.getDefault().lookup(ProjectController.class);
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


    public void runLayout() {

        logger.info("Attempting to run layout");
        Layout layout = Layouts.getLayout(graphModel, layoutArgs);
        Long layoutIterations = layoutArgs.getLayoutIterations();
        logger.info("Running layout for " + layoutIterations + " steps");
//        int j = 0;
//        for(Node n: graphModel.getUndirectedGraph().getNodes()) {
//            System.out.println(n.x());
//            if(j++ > 10) break;
//        }
        if(null != layout) {
            for (int i = 0; i < layoutIterations; i++) {
                layout.goAlgo();
                if (i % 100 == 0) {
                    logger.info("Step " + i);
                }
            }
            layout.endAlgo();
            logger.info("Finished running layout");
        }
//        j = 0;
//        for(Node n: graphModel.getUndirectedGraph().getNodes()) {
//            System.out.println(n.x());
//            if(j++ > 10) break;
//        }
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
