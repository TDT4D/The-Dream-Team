package com.github.dreamteam;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Map;
import java.util.Optional;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.mongo.DataMongoTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.testcontainers.containers.MongoDBContainer;
import org.testcontainers.junit.jupiter.Testcontainers;

import com.github.dreamteam.models.ApplicationData;
import com.github.dreamteam.models.Project;
import com.github.dreamteam.models.Student;
import com.github.dreamteam.repositories.ProjectRepository;
import com.github.dreamteam.repositories.StudentRepository;

@ExtendWith(SpringExtension.class)
@DataMongoTest
@Testcontainers
public class MongoTestContainerTest {

    static MongoDBContainer mongoDBContainer = new MongoDBContainer("mongo:7.0.16");

    @Autowired
    private StudentRepository studentRepository;

    @Autowired
    private ProjectRepository projectRepository;

    @BeforeAll
    static void setUp() {
        mongoDBContainer.start();
        System.setProperty("spring.data.mongodb.uri", mongoDBContainer.getReplicaSetUrl());
    }

    @Test
    void testInsertAndFindStudents() {
        Student student = new Student(
                1L, "John Doe", "Harvard University", "Stanford University",
                "San Francisco", "http://cv.com/john",
                "Master", List.of("Note1", "Note2"),
                Map.of("LinkedIn", "http://linkedin.com/john"),
                "Computer Science Studies",
                "Computer Science", "Full-time",
                "Good team player",
                "Passionate about innovation",
                "Great at software development",
                List.of(new ApplicationData(101L, "AI Research", 1L, 1L, "Candidate", false, "", "Love AI", "Project fits my goals"))
        );

        studentRepository.save(student);

        Optional<Student> found = studentRepository.findById(1L);
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("John Doe");
    }

    @Test
    void testInsertAndFindProjects() {
        Project project = new Project(
                101L, "AI Research", "An AI-focused project",
                List.of(1L, 2L), List.of("AI", "ML"), List.of("Technology")
        );

        projectRepository.save(project);

        Optional<Project> found = projectRepository.findById(101L);
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("AI Research");
    }
}
