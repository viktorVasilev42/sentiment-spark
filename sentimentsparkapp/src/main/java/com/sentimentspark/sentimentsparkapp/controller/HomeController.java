package com.sentimentspark.sentimentsparkapp.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/hello")
public class HomeController {

    @GetMapping()
    public String abc() {
        return "hello";
    }
}