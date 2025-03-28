package com.github.dreamteam;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.mongo.DataMongoTest;
import org.testcontainers.junit.jupiter.Testcontainers;

import com.github.dreamteam.models.ApplicationData;
import com.github.dreamteam.models.Project;
import com.github.dreamteam.models.Student;
import com.github.dreamteam.repositories.ProjectRepository;
import com.github.dreamteam.repositories.StudentRepository;

@DataMongoTest
@Testcontainers
public class DatabaseIntegrationTest extends AbstractContainerBaseTest {

    @Autowired
    private StudentRepository studentRepository;

    @Autowired
    private ProjectRepository projectRepository;

    static private Student mockStudent;
    static private Project mockProject;

    @BeforeAll
    static void initialSetup() {
        mockStudent = new Student(
                "999", "Test Student", "Test University", "Test Attending University",
                "Test City", "http://cv.com/test",
                "Bachelor", List.of("Note1", "Note2"),
                Map.of("LinkedIn", "http://linkedin.com/test"),
                "Test Studies Description",
                "Test Studies Field", "Test Studies Type",
                "Test Why Good Creator",
                "Test Why Join Demola",
                "Test Why Role",
                List.of(new ApplicationData(
                        "999", "Test Project", "1", 1L, "Candidate",
                        false, "", "Test Love AI",
                        "Test Project fits my goals")));

        mockProject = new Project("999", "Test Project", "Test Description",
                List.of(1L, 2L),
                List.of("AI", "Machine Learning"), List.of("Technology"));
    }

    @BeforeEach
    void setUp() {
        studentRepository.deleteAll();
        projectRepository.deleteAll();
        init();
    }

    @Test
    void testMongoDbConnection() {
        var studentCount = studentRepository.count();
        var projectCount = projectRepository.count();

        assertThat(studentCount).isGreaterThan(0);
        assertThat(projectCount).isGreaterThan(0);
    }

    @Test
    void testInsertAndCheckCount() {
        var countBefore = studentRepository.count();
        studentRepository.save(mockStudent);
        var countAfter = studentRepository.count();

        assertThat(countAfter).isGreaterThan(countBefore);
    }

    @Test
    void testInsertAndRetrieveStudent() {
        studentRepository.save(mockStudent);
        var mockStudentId = mockStudent.getId();
        var retrievedStudent = studentRepository.findById(mockStudentId).orElse(null);

        assertThat(retrievedStudent).isNotNull();
        assertThat(retrievedStudent.getName()).isEqualTo(mockStudent.getName());
    }

    @Test
    void testInsertAndRetrieveProject() {
        projectRepository.save(mockProject);
        var retrievedProject = projectRepository.findById(mockProject.getId()).orElse(null);

        assertThat(retrievedProject).isNotNull();
        assertThat(retrievedProject.getName()).isEqualTo(mockProject.getName());
    }

}
