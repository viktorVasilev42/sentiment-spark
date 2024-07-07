package com.sentimentspark.sentimentsparkapp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.sentimentspark.sentimentsparkapp.model.CompaniesDTO;
import com.sentimentspark.sentimentsparkapp.service.HomeService;

import lombok.RequiredArgsConstructor;

@Controller
@RequestMapping("/hello")
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
        return "home";
    }

    @PostMapping()
    public String test(
            @ModelAttribute CompaniesDTO companiesDTO
    ) throws InterruptedException {
        try {
            homeService.runFinViz(companiesDTO.getAllChecked());
        }
        catch (Exception e) {
            return "redirect:/hello";
        }

        Thread.sleep(2000);
        return "redirect:/hello?generate=true";
    }
}
