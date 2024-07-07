package com.sentimentspark.sentimentsparkapp;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.core.io.ClassPathResource;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

@SpringBootApplication
public class SentimentsparkappApplication implements CommandLineRunner {

	public static void main(String[] args) {

		SpringApplication.run(SentimentsparkappApplication.class, args);

	}

	@Override
	public void run(String... args) throws Exception {
		List<String> command = new ArrayList<>();
		command.add("python");
		command.add("market_trends_script.py");

		File scriptFile = new ClassPathResource("scripts/finviz.py").getFile();
		ProcessBuilder processBuilder = new ProcessBuilder(command);
		processBuilder.directory(scriptFile.getParentFile());
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
