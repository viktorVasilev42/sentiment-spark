package com.sentimentspark.sentimentsparkapp.controller;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.List;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.sentimentspark.sentimentsparkapp.model.CompaniesDTO;
import com.sentimentspark.sentimentsparkapp.model.StocksDTO;
import com.sentimentspark.sentimentsparkapp.service.HomeService;

import lombok.RequiredArgsConstructor;

@Controller
@RequestMapping("/home")
@RequiredArgsConstructor
public class HomeController {
    private final HomeService homeService;

    @GetMapping()
    public String abc(
            @RequestParam(defaultValue = "0") int scraper,
            @RequestParam(defaultValue = "false") boolean generate,
            Model model
    ) {
        model.addAttribute("scraper", scraper);
        model.addAttribute("generate", generate);

        try {
            List<String> imagePaths = homeService.getSubplotPaths();
            model.addAttribute("subplots", imagePaths);
        }
        catch (FileNotFoundException e) {
            System.out.println("Error loading subplots");
        }

        try {
            List<StocksDTO> stocksDataList = homeService.readStockData();
            model.addAttribute("stocksDataList", stocksDataList);
        }
        catch (IOException e) {
            System.out.println("Error loading stock data from csv");
        }

        return "home";
    }

    @PostMapping("/0")
    public String postFinviz(
            @ModelAttribute CompaniesDTO companiesDTO
    ) throws InterruptedException {
        try {
            homeService.runFinViz(companiesDTO.getAllChecked());
        }
        catch (Exception e) {
            return "redirect:/home";
        }

        Thread.sleep(2000);
        return "redirect:/home?generate=true";
    }

    @PostMapping("/1")
    public String postMarketWatch(
            @ModelAttribute CompaniesDTO companiesDTO
    ) throws InterruptedException {
        try {
            homeService.runMarketWatch(companiesDTO.getAllChecked());
        }
        catch (Exception e) {
            return "redirect:/home";
        }

        Thread.sleep(2000);
        return "redirect:/home?generate=true&scraper=1";
    }

    @PostMapping("/2")
    public String postStockAnalysis(
            @ModelAttribute CompaniesDTO companiesDTO
    ) throws InterruptedException {
        try {
            homeService.runStockAnalysis(companiesDTO.getAllChecked());
        }
        catch (Exception e) {
            return "redirect:/home";
        }

        Thread.sleep(2000);
        return "redirect:/home?generate=true&scraper=2";
    }
}
