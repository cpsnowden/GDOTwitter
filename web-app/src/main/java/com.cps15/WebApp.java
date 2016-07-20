package com.cps15;

import org.eclipse.jetty.security.HashLoginService;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.webapp.WebAppContext;

public class WebApp{

    public static void main(String[] args) throws Exception {

        String webappDirLocation = "src/main/webapp/";

        // The port that we should run on can be set into an environment variable
        // Look for that variable and default to 8080 if it isn't there.
        String webPort = System.getenv("PORT");
        if (webPort == null || webPort.isEmpty()) {
            webPort = "8080";
        }
        Server server = new Server(Integer.valueOf(webPort));

        WebAppContext webapp = new WebAppContext();
        webapp.setContextPath("/");
        webapp.setDescriptor(webappDirLocation + "/WEB-INF/web.xml");
        webapp.setResourceBase(webappDirLocation);

//        HashLoginService loginService = new HashLoginService("JCGRealm");
//
//        loginService.setConfig("realm.properties");
//        System.out.println("I am here");
//        System.out.printf(loginService.getConfig());
//        System.out.printf(loginService.getUsers().values().toString());
//        server.addBean(loginService);

        server.setHandler(webapp);
        server.start();
        server.join();
    }
}