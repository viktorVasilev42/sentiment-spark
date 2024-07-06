package com.sentimentspark.sentimentsparkapp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
@RequestMapping("/hello")
public class HomeController {

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
            @RequestParam(required = false) boolean one,
            @RequestParam(required = false) boolean two
    ) {
        System.out.println("Checkbox one: " + one);
        System.out.println("Checkbox two: " + two);
        return "redirect:/hello?generate=true";
    }
}
