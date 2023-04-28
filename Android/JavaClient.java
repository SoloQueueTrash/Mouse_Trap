import java.io.*;
import java.net.*;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;

public class JavaClient {

    public static void main(String[] args) {
        String serverName = "localhost";
        int port = 12345;

        try {
            System.out.println("Connecting to " + serverName + " on port " + port);
            Socket client = new Socket(serverName, port);
            System.out.println("Connection established: " + client.getRemoteSocketAddress());

            // set up the reader and writer
            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
            PrintWriter writer = new PrintWriter(client.getOutputStream(), true);

            while (true) {
                // read input from the user
                System.out.print("Enter message to send: ");
                String message = reader.readLine();

                // break the loop if the message is empty
                if (message.equals("")) {
                    break;
                }
                System.out.println("Sending: " + message);

                // send the message to the server
                writer.println(message);
                
                message = message.replaceAll("\\n", "");

                System.out.print(message.equals("cmd_photo"));

                if (message.equals("cmd_photo")) {
                    try {
                        InputStream inputStream = client.getInputStream();
                        byte[] imageData = inputStream.readAllBytes();
                        System.out.println("Saving photo");

                        ByteArrayInputStream bis = new ByteArrayInputStream(imageData);
                        BufferedImage image = ImageIO.read(bis);

                        // Save the image as a JPEG file
                        File outputfile = new File("received_image.jpg");
                        ImageIO.write(image, "jpg", outputfile);

                        System.out.println("Image saved as received_image4.jpg");
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                } else {
                    // receive a response from the server
                    BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
                    String response = in.readLine();
                    System.out.println("Received message from server: " + response);
                }

            }

            // close the connection
            client.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
