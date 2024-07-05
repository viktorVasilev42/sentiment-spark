package com.sentimentspark.sentimentsparkapp.service;

import java.io.IOException;
import java.util.List;

public class pythonScriptRunner {
    private List<String> companies;

    public pythonScriptRunner(List<String> companies) {
        this.companies = companies;
    }
    public void runScript() throws IOException, InterruptedException {
        StringBuilder var=new StringBuilder();
        for(int i=0;i<companies.size();i++){
            var.append(companies.get(i));
            var.append(' ');
        }
        Runtime.getRuntime().exec("python finviz.py " +var.toString()).waitFor();
        System.out.println("abc");
    }
}
