package utils;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Author: Ruarcc McAloon
 * Date: 13/02/14
 * Time: 09:30
 */
public class TestData {
    private String source;

    public TestData(String source){
        this.source = source;
    }

    public List<String[]> getTestDataFromSource() throws IOException {
        List<String[]> testData = new ArrayList<String[]>();
        BufferedReader file = new BufferedReader(new FileReader(source));

        String record = file.readLine();
        if (record != null) {
            while ((record=file.readLine())!=null) {
                String fields[] = record.split(",");
                testData.add(fields);
            }
        }

        file.close();
        return testData;
    }
}
