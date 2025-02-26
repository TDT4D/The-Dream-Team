package com.github.dreamteam.services;

import com.github.dreamteam.models.Student;

import java.util.List;

public interface StudentService {
    // TODO: Move to ProjectService
    public List<Student> getStudentsByProject(Long projectId);

    public String getStudentName(Long studentId);

    // TODO: Delete this
    public Student getStudentById(Long studentId);

}
