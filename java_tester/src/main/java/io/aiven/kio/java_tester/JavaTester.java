package io.aiven.kio.java_tester;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.Base64;

import org.apache.kafka.common.protocol.ApiMessage;
import org.apache.kafka.common.protocol.ByteBufferAccessor;
import org.apache.kafka.common.protocol.ObjectSerializationCache;
import org.apache.kafka.common.protocol.Readable;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class JavaTester {
    private static final String SUCCESS_RESPONSE = "{\"success\": true}";

    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        System.out.println("Java tester started");
        System.out.flush();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))) {
            String caseStr;
            while ((caseStr = reader.readLine()) != null) {
                String result = test(caseStr);
                System.out.println(result);
                System.out.flush();
            }
        }
    }

    private static String test(String caseStr) {
        try {
            JsonNode caseNode = OBJECT_MAPPER.readTree(caseStr);
            short version = caseNode.get("version").shortValue();
            String shortClassName = caseNode.get("class").asText();
            RootMessageInfo rootMessageInfo = new RootMessageInfo(shortClassName, version);

            ObjectSerializationCache objectSerializationCache = new ObjectSerializationCache();
            ApiMessage constructedMessage =
                new ObjectCreator<>(rootMessageInfo, rootMessageInfo.rootClazz, rootMessageInfo.rootSchema)
                    .create(caseNode.get("json"));
            int size = constructedMessage.size(objectSerializationCache, version);
            ByteBufferAccessor writer = new ByteBufferAccessor(ByteBuffer.allocate(size));
            constructedMessage.write(writer, objectSerializationCache, version);

            byte[] serializedFromPython = Base64.getDecoder().decode(caseNode.get("serialized").asText());
            Readable readable = new ByteBufferAccessor(ByteBuffer.wrap(serializedFromPython));
            ApiMessage messageDeserializedFromPython = rootMessageInfo.rootClazz.newInstance();
            messageDeserializedFromPython.read(readable, version);

            if (!messageDeserializedFromPython.equals(constructedMessage)) {
                String message = "Deserialized message is not equal to constructed\n"
                    + "Input: " + caseStr + "\n"
                    + "Deserialized: " + messageDeserializedFromPython + "\n"
                    + "Constructed: " + constructedMessage;
                return failureResponse(message);
            } else {
                byte[] serializedInJava = writer.buffer().array();
                if (!Arrays.equals(serializedFromPython, serializedInJava)) {
                    String message = "Message serialized in Java is not equal to message serialized in Python\n"
                        + "Input: " + caseStr + "\n"
                        + "Deserialized: " + messageDeserializedFromPython + "\n"
                        + "Constructed: " + constructedMessage;
                    return failureResponse(message);
                } else {
                    return SUCCESS_RESPONSE;
                }
            }
        } catch (Exception e) {
            return exceptionResponse(e, caseStr);
        }
    }

    private static String failureResponse(String message) {
        ObjectNode objectNode = OBJECT_MAPPER.createObjectNode();
        objectNode.put("success", false);
        objectNode.put("message", message);
        try {
            return OBJECT_MAPPER.writeValueAsString(objectNode);
        } catch (JsonProcessingException e) {
            // this shouldn't happen
            throw new RuntimeException(e);
        }
    }

    private static String exceptionResponse(Exception exception, String caseStr) {
        ObjectNode objectNode = OBJECT_MAPPER.createObjectNode();
        objectNode.put("success", false);

        StringWriter stringWriter = new StringWriter();
        PrintWriter printWriter = new PrintWriter(stringWriter);
        exception.printStackTrace(printWriter);
        objectNode.put("exception", stringWriter.toString() + "\n" + "Case: " + caseStr);

        try {
            return OBJECT_MAPPER.writeValueAsString(objectNode);
        } catch (JsonProcessingException e) {
            // this shouldn't happen
            throw new RuntimeException(e);
        }
    }
}
