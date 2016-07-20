package cps15.App;

import com.rabbitmq.client.*;

import java.io.IOException;
import java.util.concurrent.TimeoutException;
import java.util.logging.Logger;

/**
 * Created by ChrisSnowden on 17/07/2016.
 */
public class RabbitMQWrapper {

    private static final Logger logger = Logger.getLogger(App.class.getName());
    private static final String GEPHI_QUEUE = "GEPHI_QUEUE";
    private Channel channel;
    private Connection connection;
    private QueueingConsumer queueingConsumer;
    private QueueingConsumer.Delivery delivery;
    private AMQP.BasicProperties properties;
    private AMQP.BasicProperties replyProperties;

    public RabbitMQWrapper() throws IOException, TimeoutException {
        ConnectionFactory connectionFactory = new ConnectionFactory();
        connectionFactory.setHost("localhost");

        connection = connectionFactory.newConnection();
        channel = connection.createChannel();
    }

    public void start() throws IOException {

        channel.queueDeclare(GEPHI_QUEUE, false, false, false, null);
        channel.basicQos(1);
        queueingConsumer = new QueueingConsumer(channel);
        channel.basicConsume(GEPHI_QUEUE, false, queueingConsumer);
        logger.info(" [x] Awaiting RPC requests");
    }

    public String get() throws InterruptedException {

        delivery = queueingConsumer.nextDelivery();
        properties = delivery.getProperties();
        replyProperties = new AMQP.BasicProperties.Builder().correlationId(properties.getCorrelationId()).build();
        String request = new String(delivery.getBody());
        logger.info("Received request: " + request);
        return request;

    }

    public void basicPublish(String response) throws IOException {
        channel.basicPublish("", properties.getReplyTo(), replyProperties, response.getBytes());
        channel.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
        logger.info("Sent response: " + response);
    }
}
