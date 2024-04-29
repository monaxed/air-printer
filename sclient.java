import java.io.*;
import java.net.*;

public class sclient {
    public static final int BYTESIZE = 64;
    public static final int PORT = 5050;
    public static final String FORMAT = "UTF-8";
    public static final String DISCONNECT_MESSAGE = "!DISCONNECT";
    public static final String SERVER = "192.168.1.11";

    static BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
    
    public static void main(String[] args) {
        try {
            Socket clientSocket = new Socket(SERVER, PORT);
            OutputStream outputStream = clientSocket.getOutputStream();
            InputStream inputStream = clientSocket.getInputStream();

            System.out.println("Enter file path: ");
            String path = input.readLine();
            File file = new File(path);

            sendString("application/pdf", outputStream, inputStream);
            sendString(file.getName(), outputStream, inputStream);
            sendFile(file, outputStream, inputStream);
            sendString(DISCONNECT_MESSAGE, outputStream, inputStream);

            clientSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static void sendString(String msg, OutputStream outputStream, InputStream inputStream) throws IOException {
        byte[] messageBytes = msg.getBytes(FORMAT);
        int msgLength = messageBytes.length;
        byte[] lengthBytes = String.format("%-" + BYTESIZE + "s", msgLength).getBytes(FORMAT);
        
        outputStream.write(lengthBytes);
        outputStream.write(messageBytes);
        
        byte[] responseBytes = new byte[2048];
        int bytesRead = inputStream.read(responseBytes);
        String response = new String(responseBytes, 0, bytesRead, FORMAT);
        System.out.println(response);
    }

    public static void sendFile(File file, OutputStream outputStream, InputStream inputStream) throws IOException {
        long fileSize = file.length();
        byte[] fileSizeBytes = String.valueOf(fileSize).getBytes(FORMAT);
        
        outputStream.write(fileSizeBytes);
        
        byte[] buffer = new byte[4096];
        int bytesRead;
        try (FileInputStream fileInputStream = new FileInputStream(file)) {
            while ((bytesRead = fileInputStream.read(buffer)) != -1) {
                outputStream.write(buffer, 0, bytesRead);
            }
        }

        byte[] responseBytes = new byte[2048];
        bytesRead = inputStream.read(responseBytes);
        String response = new String(responseBytes, 0, bytesRead, FORMAT);
        System.out.println(response);
    }
}
