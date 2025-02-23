package com.github.dreamteam.controllers;

import com.github.dreamteam.services.ProjectServiceImpl;
import com.github.dreamteam.services.StudentService;
import com.github.dreamteam.models.Project;
import com.github.dreamteam.models.Student;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

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
}
