package com.sentimentspark.sentimentsparkapp;

import java.util.List;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.sentimentspark.sentimentsparkapp.service.PythonScriptRunner;

@SpringBootApplication
public class SentimentsparkappApplication implements CommandLineRunner {

	public static void main(String[] args) {

		SpringApplication.run(SentimentsparkappApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {

		PythonScriptRunner pythonScriptRunner = new PythonScriptRunner(List.of("META","GOOG"));
		pythonScriptRunner.runScript();
	}
}
