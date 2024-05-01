import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class packetHandler {
    String filetype;
    byte[] content;
    String filename;

    public packetHandler(String filepath) throws IOException{
        Path path = Paths.get(filepath);
        filetype = identifyFileType(path);
        content = readFileAsBytes(filepath);
        File file = new File(filepath);
        filename = file.getName();
    }

    public static String identifyFileType(Path path) throws IOException {
    
        String fileType = Files.probeContentType(path);
        return fileType != null ? fileType : "Unknown";
    }

    public static byte[] readFileAsBytes(String path) throws IOException {
         FileInputStream fis = new FileInputStream(path);
         byte[] bytes = new byte[(int) new File(path).length()];
         fis.read(bytes);
         fis.close();

        return bytes;
    }

    public String getfiletype(){
        return this.filetype;
    }

    public byte[] getContent(){
        return this.content;
    }

    public String getfilename(){
        return this.filename;
    }
    
}
