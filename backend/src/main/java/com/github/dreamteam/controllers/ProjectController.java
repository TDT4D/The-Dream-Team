package com.github.dreamteam.controllers;

import com.github.dreamteam.services.ProjectServiceImpl;
import com.github.dreamteam.services.StudentService;

import jakarta.servlet.http.HttpServletRequest;

import com.github.dreamteam.models.Project;
import com.github.dreamteam.models.Student;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.View;

import java.util.List;

@RestController
@RequestMapping("/projects")
public class ProjectController {

    @Autowired
    private ProjectServiceImpl projectService;

    @Autowired
    private StudentService studentService;

    @GetMapping
    public ResponseEntity<List<Project>> getProjects(@RequestParam(required = false) String status) {
        List<Project> projects = projectService.getAllProjects();
        return !projects.isEmpty()
                ? ResponseEntity.ok(projects)
                : ResponseEntity.notFound().build();
    }

    @GetMapping("/{projectId}/students")
    public ResponseEntity<List<Student>> getStudents(@PathVariable Long projectId) {
        List<Student> students = studentService.getStudentsByProject(projectId);
        return !students.isEmpty()
                ? ResponseEntity.ok(students)
                : ResponseEntity.notFound().build();
    }

    @PostMapping("/predict")
    public ModelAndView predict(HttpServletRequest request) {
        request.setAttribute(
                View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.PERMANENT_REDIRECT);
        return new ModelAndView("redirect:/ml/score/predict");
    }

    @GetMapping("/{projectId}/scores")
    public ModelAndView getScores(HttpServletRequest request, @PathVariable Long projectId,
            @RequestParam(required = false) String scoreFile) {
        request.setAttribute(
                View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.PERMANENT_REDIRECT);
        StringBuilder redirectUrl = new StringBuilder("redirect:/ml/score/scores?projectId=").append(projectId);
        if (scoreFile != null) {
            redirectUrl.append("&scoreFile=").append(scoreFile);
        }
        return new ModelAndView(redirectUrl.toString());
    }

    @GetMapping("/scores")
    public ModelAndView getAllScores(HttpServletRequest request, @RequestParam(required = false) String scoreFile) {
        request.setAttribute(
                View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.PERMANENT_REDIRECT);
        StringBuilder redirectUrl = new StringBuilder("redirect:/ml/score/scores");
        if (scoreFile != null) {
            redirectUrl.append("?scoreFile=").append(scoreFile);
        }
        return new ModelAndView(redirectUrl.toString());
    }

    @PostMapping("{projectId}/team")
    public ModelAndView buildTeam(HttpServletRequest request, @PathVariable Long projectId,
            @RequestParam(required = false) Integer size, @RequestParam(required = false) String dataFile,
            @RequestParam(required = false) String saveFile) {
        request.setAttribute(
                View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.PERMANENT_REDIRECT);
        StringBuilder redirectUrl = new StringBuilder("redirect:/ml/team/build-team?projectId=").append(projectId);
        if (size != null) {
            redirectUrl.append("&size=").append(size);
        }
        if (dataFile != null) {
            redirectUrl.append("&data=").append(dataFile);
        }
        if (saveFile != null) {
            redirectUrl.append("&saveFile=").append(saveFile);
        }
        return new ModelAndView(redirectUrl.toString());
    }
}
