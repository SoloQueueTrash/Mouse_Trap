import java.io.*;
import java.net.*;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;

public class GetPhoto {
    public static void render(byte[] imageData) {
        try {
        
        System.out.println("Saving photo");

        ByteArrayInputStream bis = new ByteArrayInputStream(imageData);
        BufferedImage image = ImageIO.read(bis);

        // Save the image as a JPEG file
        File outputfile = new File("received_image.jpg");
        ImageIO.write(image, "jpg", outputfile);

        System.out.println("Image saved as received_image.jpg");
    } catch (IOException e) {
        e.printStackTrace();
        }
    }

    public static byte[] receive(Socket socket) {
        try {
            InputStream inputStream = socket.getInputStream();
            byte[] imageData = inputStream.readAllBytes();
            return imageData;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public static void send(Socket socket, String message) {
        try{
            OutputStream outputStream = socket.getOutputStream();
            outputStream.write(message.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {

        try (Socket socket = new Socket("localhost", 12345)) {
            
            System.out.println("Connected to Python server.");
            send(socket, "cmd_open");

            render(receive(socket));
            send(socket, "Exit");


        } catch (IOException e) {
            e.printStackTrace();
        }

    }

}
