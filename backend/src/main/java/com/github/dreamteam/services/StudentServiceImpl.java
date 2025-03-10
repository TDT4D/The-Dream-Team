package com.github.dreamteam.services;

import com.github.dreamteam.exceptions.EntityNotFoundException;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.model.Filters;
import org.bson.conversions.Bson;
import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

@Service
public class StudentServiceImpl implements StudentService {

        private static final Logger LOGGER = LoggerFactory.getLogger(ProjectServiceImpl.class);
        private final MongoCollection<Document> studentCollection;

        public StudentServiceImpl(MongoTemplate mongoTemplate) {
                this.studentCollection = mongoTemplate.getCollection("students");
        }

        public Collection<Document> getStudentsByProject(Long projectId) {
                LOGGER.info("Fetching all students from MongoDB for project {}", projectId);
                Bson filter = Filters.eq("applications.projectId", projectId);
                List<Document> students = studentCollection.find(filter).into(new ArrayList<>());
                if (students.isEmpty()) {
                        throw new EntityNotFoundException("No students found for project " + projectId);
                }
                return students;
        }

        // TODO: Clean up
        // public Student getStudentById(Long studentId) {
        // return studentMap.get(studentId);
        // }

        // public String getStudentName(Long studentId) {
        // Student student = studentMap.get(studentId);
        // return (student != null) ? student.getName() : null;
        // }
}
