import java.net.*;
import java.io.*;

public class TestApplication {

    public static void main(String[] args) throws IOException {

        // Define the IP address and port to use
        String ipAddress = "localhost";
        int port = 12345;

        // Create a socket object and connect to the server
        Socket socket = new Socket(ipAddress, port);

        // Create input and output streams for the socket
        OutputStream outputStream = socket.getOutputStream();
        InputStream inputStream = socket.getInputStream();

        // Send data to the server
        String message = "Hello, server!";
        outputStream.write(message.getBytes());

        // Receive data from the server
        byte[] buffer = new byte[1024];
        int bytesRead = inputStream.read(buffer);
        String response = new String(buffer, 0, bytesRead);

        System.out.println("Received response from server: " + response);

        message = "exit";
        outputStream.write(message.getBytes());

        byte[] bufferRead = new byte[1024];
        int bytes = inputStream.read(bufferRead);
        String response1 = new String(bufferRead, 0, bytes);

        System.out.println("Received response from server: " + response1);

        // Close the socket
        socket.close();
    }
}