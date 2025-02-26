package com.github.dreamteam.controllers;

import com.github.dreamteam.models.Student;
import com.github.dreamteam.services.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/students")
public class StudentController {

    @Autowired
    private StudentService service;

    // TODO: Delete this
    @GetMapping("/{studentId}")
    public ResponseEntity<Student> getStudentById(@PathVariable Long studentId) {
        Student student = service.getStudentById(studentId);
        return (student != null)
                ? ResponseEntity.ok(student)
                : ResponseEntity.notFound().build();
    }

    @GetMapping("/{studentId}/name")
    public ResponseEntity<String> getStudentName(@PathVariable Long studentId) {
        String studentName = service.getStudentName(studentId);
        return (studentName != null)
                ? ResponseEntity.ok(studentName)
                : ResponseEntity.notFound().build();
    }
}
