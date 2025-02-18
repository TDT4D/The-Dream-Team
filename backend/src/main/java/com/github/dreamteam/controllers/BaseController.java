package com.github.dreamteam.controllers;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/")
public class BaseController {

    @RequestMapping("/")
    public String index() {
        return "Greetings from Spring Boot!";
    }

}