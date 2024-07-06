package com.sentimentspark.sentimentsparkapp;

import java.util.List;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import com.sentimentspark.sentimentsparkapp.service.PyScriptRunner;

@SpringBootApplication
public class SentimentsparkappApplication implements CommandLineRunner {

	public static void main(String[] args) {

		SpringApplication.run(SentimentsparkappApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {

		// PyScriptRunner pythonScriptRunner = new PyScriptRunner(List.of("META","GOOG"));
		// pythonScriptRunner.runScript();
	}
}
