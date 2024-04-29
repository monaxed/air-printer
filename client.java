import java.io.*;
import java.net.*;
import java.util.*;

public class client {
    public static final int BYTESIZE = 64;
    public static final int PORT = 5050;
    public static final String FORMAT = "UTF-8";
    public static final String DISCONNECT_MESSAGE = "!DISCONNECT";
    public static final String SERVER = "192.168.1.11";

    static Scanner input = new Scanner(System.in);
    
    public static void main(String[] args) {
        try {
            Socket clientSocket = new Socket(SERVER, PORT);
            OutputStream outputStream = clientSocket.getOutputStream();
            InputStream inputStream = clientSocket.getInputStream();

            System.out.println("Enter file path: ");
            String path = input.nextLine();
            File pather = new File(path);
            packetHandler file = new packetHandler(path);

            sendstring(file.getfiletype(), outputStream, inputStream);
            sendstring(file.getfilename(), outputStream, inputStream);
            sendcontent(pather,file.getContent(), outputStream, inputStream);
            sendstring(DISCONNECT_MESSAGE, outputStream, inputStream);


            // sendstring("hello world", outputStream, inputStream);
            // sendstring("test 1", outputStream, inputStream);
            // sendstring("test2", outputStream, inputStream);
            // sendstring(DISCONNECT_MESSAGE, outputStream, inputStream);
            
            clientSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static void sendstring(String msg, OutputStream outputStream, InputStream inputStream) throws IOException {
        byte[] messageBytes = msg.getBytes(FORMAT); // decoding message with the specified format
        int msgLength = messageBytes.length; // getting the length of the message
        byte[] lengthBytes = String.valueOf(msgLength).getBytes(FORMAT); // changing message length into bytes with the specified format
        
        byte[] sendLengthBytes = new byte[BYTESIZE];
        for (int i = 0; i < BYTESIZE; i++) {
            if (i < lengthBytes.length) {
                sendLengthBytes[i] = lengthBytes[i];
            } else {
                sendLengthBytes[i] = (byte) ' ';
            }
        }
        
        outputStream.write(sendLengthBytes);
        outputStream.write(messageBytes);
        
        byte[] responseBytes = new byte[2048];
        int bytesRead = inputStream.read(responseBytes);
        String response = new String(responseBytes, 0, bytesRead, FORMAT);
        System.out.println(response);
    }


    public static void sendcontent(File path, byte[] msgBytes, OutputStream outputStream, InputStream inputStream) throws IOException {
        int msgLength = msgBytes.length; // getting the length of the message
        byte[] lengthBytes = Integer.toString(msgLength).getBytes(FORMAT); // changing message length into bytes with the specified format

        long filesize = (path.length());
        String filesizestring = Long.toString(filesize);
        System.out.println(filesizestring);
        byte[] fileSizeBytes = filesizestring.getBytes("UTF-8");
        
        byte[] sendLengthBytes = new byte[BYTESIZE];
        for (int i = 0; i < BYTESIZE; i++) {
            if (i < lengthBytes.length) {
                sendLengthBytes[i] = lengthBytes[i];
            } else {
                sendLengthBytes[i] = (byte) ' ';
            }
        }
        
        outputStream.write(fileSizeBytes);
        outputStream.write(msgBytes);
        
        byte[] responseBytes = new byte[2048];
        int bytesRead = inputStream.read(responseBytes);
        String response = new String(responseBytes, 0, bytesRead, FORMAT);
        System.out.println(response);
    }
}
