import java.io.IOException;
import java.util.Scanner;

public class tester {
    static Scanner input = new Scanner(System.in);
    public static void main(String[] args) throws IOException {
                    
       
        String file ="C:/Programming/Server/tester.pdf";

        packetHandler filer = new packetHandler(file);

        System.out.println(filer.getfiletype());
        System.out.println(filer.getfilename());

        byte[] endBytes = "<END>".getBytes();
        String endString = new String(endBytes);
        System.out.println(endBytes);


    }
    
}
