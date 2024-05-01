import java.io.*;
import java.net.*;

public class test2 {
    public static void main(String[] args) throws IOException {
        packetHandler filer = new packetHandler("C:/Programming/Server/tester.pdf");
        String type = filer.getfiletype();
        String fileName = filer.getfilename();
        String filePath = "C:/Programming/Server/tester.pdf";
        String serverAddress = "192.168.1.11";
        String FORMAT = "UTF-8";
        int serverPort = 5050;

        try {
            Socket clientSocket = new Socket(serverAddress, serverPort);
            OutputStream outputStream = clientSocket.getOutputStream();
            InputStream inputStream = clientSocket.getInputStream();




            // send file type
            outputStream.write(type.getBytes(FORMAT));

            //listen
            byte[] responseBytes = new byte[2048];
            // int bytesRead = inputStream.read(responseBytes);
            // String response = new String(responseBytes, 0, bytesRead, FORMAT);
            // System.out.println(response);
    

            // Send file name
            outputStream.write(fileName.getBytes(FORMAT));
            // listen
            // bytesRead = inputStream.read(responseBytes);
            // response = new String(responseBytes, 0, bytesRead, FORMAT);
            // System.out.println(response);


            // Send file content
            FileInputStream fileInputStream = new FileInputStream(filePath);

            byte[] buffer = new byte[4096];
            int bytesRead2;
            while ((bytesRead2 = fileInputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead2);
            }

            // Send end marker
            outputStream.write("<END>".getBytes());

            int bytesRead = inputStream.read(responseBytes);
            String response = new String(responseBytes, 0, bytesRead, FORMAT);
            System.out.println(response);


            // Close resources
            fileInputStream.close();
            outputStream.close();
            clientSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
