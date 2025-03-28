package com.github.dreamteam.controllers;

import com.github.dreamteam.services.ProjectServiceImpl;
import com.github.dreamteam.services.StudentService;

import jakarta.servlet.http.HttpServletRequest;

import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.github.dreamteam.exceptions.EntityNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.View;

import java.util.Collection;
import java.util.Optional;

@RestController
@RequestMapping("/projects")
public class ProjectController {

    private static final Logger LOGGER = LoggerFactory.getLogger(ProjectController.class);

    @Autowired
    private ProjectServiceImpl projectService;

    @Autowired
    private StudentService studentService;

    @GetMapping
    public Collection<Document> getProjects(@RequestParam(required = false) Optional<String> status,
            @RequestParam(required = false) Optional<Integer> limit) {
        if (limit.isPresent()) {
            return projectService.getAllProjects(limit.get());
        } else {
            return projectService.getAllProjects(0);
        }
    }

    @GetMapping("/{projectId}/students")
    public Collection<Document> getStudents(@PathVariable Long projectId) {
        return studentService.getStudentsByProject(projectId);
    }

    @PostMapping("/predict")
    public ModelAndView predict(HttpServletRequest request) {
        request.setAttribute(
                View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.PERMANENT_REDIRECT);
        return new ModelAndView("redirect:/ml/score/predict");
    }

    @GetMapping("/{projectId}/scores")
    public ModelAndView getScores(HttpServletRequest request, @PathVariable Long projectId,
            @RequestParam(required = false) Optional<String> scoreFile) {
        request.setAttribute(
                View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.PERMANENT_REDIRECT);
        StringBuilder redirectUrl = new StringBuilder("redirect:/ml/score/scores?projectId=").append(projectId);
        if (scoreFile.isPresent()) {
            redirectUrl.append("&scoreFile=").append(scoreFile.get());
        }
        return new ModelAndView(redirectUrl.toString());
    }

    @GetMapping("/scores")
    public ModelAndView getAllScores(HttpServletRequest request, @RequestParam(required = false) Optional<String> scoreFile) {
        request.setAttribute(
                View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.PERMANENT_REDIRECT);
        StringBuilder redirectUrl = new StringBuilder("redirect:/ml/score/scores");
        if (scoreFile.isPresent()) {
            redirectUrl.append("?scoreFile=").append(scoreFile.get());
        }
        return new ModelAndView(redirectUrl.toString());
    }

    @PostMapping("{projectId}/team")
    public ModelAndView buildTeam(HttpServletRequest request, @PathVariable Long projectId,
            @RequestParam(required = false) Optional<Integer> size, @RequestParam(required = false) Optional<String> dataFile,
            @RequestParam(required = false) Optional<String> saveFile) {
        request.setAttribute(
                View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.PERMANENT_REDIRECT);
        StringBuilder redirectUrl = new StringBuilder("redirect:/ml/team/build-team?projectId=").append(projectId);
        if (size.isPresent()) {
            redirectUrl.append("&size=").append(size.get());
        }
        if (dataFile.isPresent()) {
            redirectUrl.append("&data=").append(dataFile.get());
        }
        if (saveFile.isPresent()) {
            redirectUrl.append("&saveFile=").append(saveFile.get());
        }
        return new ModelAndView(redirectUrl.toString());
    }

    @ExceptionHandler(EntityNotFoundException.class)
    @ResponseStatus(value = HttpStatus.NOT_FOUND, reason = "MongoDB didn't find any document.")
    public final void handleNotFoundExceptions(EntityNotFoundException e) {
        LOGGER.info("=> Movie not found: {}", e.toString());
    }

    @ExceptionHandler(RuntimeException.class)
    @ResponseStatus(value = HttpStatus.INTERNAL_SERVER_ERROR, reason = "Internal Server Error")
    public final void handleAllExceptions(RuntimeException e) {
        LOGGER.error("=> Internal server error.", e);
    }
}
