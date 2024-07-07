package com.sentimentspark.sentimentsparkapp.service;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import org.springframework.core.io.ClassPathResource;

public class PyScriptRunner {
    private List<String> companies;

    public PyScriptRunner(List<String> companies) {
        this.companies = companies;
    }

    public void runScript() throws IOException, InterruptedException {
        List<String> command = new ArrayList<>();
        command.add("python");
        command.add("main_script_runner.py");
        command.add("stock_analysis");
        command.addAll(companies);

        System.out.println("Executing command: " + command);

        File scriptFile = new ClassPathResource("scripts/finviz.py").getFile();
        ProcessBuilder processBuilder = new ProcessBuilder(command);
        processBuilder.directory(scriptFile.getParentFile());  // Set the working directory
        processBuilder.redirectErrorStream(true);
        Process process = processBuilder.start();

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        }

        int exitCode = process.waitFor();
        System.out.println("Process exited with code: " + exitCode);
    }
}

