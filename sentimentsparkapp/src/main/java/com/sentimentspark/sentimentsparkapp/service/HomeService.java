package com.sentimentspark.sentimentsparkapp.service;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.springframework.stereotype.Service;
import org.springframework.util.ResourceUtils;

import com.sentimentspark.sentimentsparkapp.model.StocksDTO;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class HomeService {
    public void runFinViz(List<String> targets) throws IOException, InterruptedException {
	    PyScriptRunner pythonScriptRunner = new PyScriptRunner(targets);
	    pythonScriptRunner.runScript("finviz");
    }

    public void runMarketWatch(List<String> targets) throws IOException, InterruptedException {
	    PyScriptRunner pythonScriptRunner = new PyScriptRunner(targets);
	    pythonScriptRunner.runScript("market_watch");
    }

    public void runStockAnalysis(List<String> targets) throws IOException, InterruptedException {
	    PyScriptRunner pythonScriptRunner = new PyScriptRunner(targets);
	    pythonScriptRunner.runScript("stock_analysis");
    }

    public List<StocksDTO> readStockData() throws IOException {
        List<StocksDTO> result = new ArrayList<>();
        String path = ResourceUtils.getFile("classpath:market_data/stock_data.csv").getAbsolutePath();
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            br.readLine();

            String line;
            while ((line = br.readLine()) != null) {
                String[] fields = line.split(",");
                result.add(new StocksDTO(fields[0], Float.parseFloat(fields[1]), fields[2]));
            }
        }
        return result;
    }

    public List<String> getSubplotPaths() throws FileNotFoundException {
        String subplotsPath = ResourceUtils.getFile("classpath:plots/subplots/").getAbsolutePath();
        File directory = new File(subplotsPath);
        File[] files = directory.listFiles();

        List<String> imagePaths = new ArrayList<>();
        if (files != null) {
            for (File file : files) {
                if (file.isFile()) {
                    imagePaths.add("/plots/subplots/" + file.getName());
                }
            }
        }

        return imagePaths;
    }
}
