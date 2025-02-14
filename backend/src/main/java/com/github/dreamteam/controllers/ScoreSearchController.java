package com.github.dreamteam.controllers;

import com.github.dreamteam.services.ScoreSearchService;
import org.springframework.web.bind.annotation.*;
import org.bson.Document;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.Collection;


@RestController
@RequestMapping("/scores")
public class ScoreSearchController {

    @Autowired
    private ScoreSearchService scoreSearchService;


    @GetMapping("/")
    public String index() {
        return "Greetings from scores api!";
    }

    @GetMapping("/{projectId}")
    public Collection<Document> searchScores(@PathVariable String projectId) {
        return scoreSearchService.searchScores(projectId);
    }

}