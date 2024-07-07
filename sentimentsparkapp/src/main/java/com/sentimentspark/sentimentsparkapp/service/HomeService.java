package com.sentimentspark.sentimentsparkapp.service;

import java.io.IOException;
import java.util.List;

import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class HomeService {

    public void runFinViz(List<String> targets) throws IOException, InterruptedException {
	    PyScriptRunner pythonScriptRunner = new PyScriptRunner(targets);
	    pythonScriptRunner.runScript();
    }
}
