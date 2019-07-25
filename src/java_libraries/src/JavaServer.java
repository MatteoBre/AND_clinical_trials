import py4j.GatewayServer;

public class JavaServer {
    public static void main(String[] args) {
        GatewayServer server = new GatewayServer(new APIWrapper());

        System.out.println("Gateway server started");
        server.start();
    }
}
