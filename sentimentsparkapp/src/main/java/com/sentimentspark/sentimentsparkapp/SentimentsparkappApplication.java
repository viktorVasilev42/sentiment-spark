package com.sentimentspark.sentimentsparkapp;

import com.sentimentspark.sentimentsparkapp.service.pythonScriptRunner;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.util.ArrayList;
import java.util.List;

@SpringBootApplication
public class SentimentsparkappApplication implements CommandLineRunner {

	public static void main(String[] args) {

		SpringApplication.run(SentimentsparkappApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {

		pythonScriptRunner pythonScriptRunner=new pythonScriptRunner(List.of("META","GOOG"));
		pythonScriptRunner.runScript();
	}
}
