package com.github.dreamteam.services;

import com.github.dreamteam.models.Student;

import java.util.Collection;
import java.util.List;

import org.bson.Document;

public interface StudentService {
    public Collection<Document> getStudentsByProject(Long projectId);

    // public String getStudentName(Long studentId);

    // TODO: Delete this
    // public Student getStudentById(Long studentId);

}
