/** The main package for the Dreamteam application. */
package com.github.dreamteam;

import static org.assertj.core.api.Assertions.assertThat;

import com.github.dreamteam.models.ApplicationData;
import com.github.dreamteam.models.Project;
import com.github.dreamteam.models.Student;
import com.github.dreamteam.repositories.ProjectRepository;
import com.github.dreamteam.repositories.StudentRepository;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.mongo.DataMongoTest;
import org.testcontainers.junit.jupiter.Testcontainers;

/**
 * This class is responsible for testing the integration of the database with the application. It
 * uses Testcontainers to create a MongoDB container for testing purposes.
 *
 * <p>It includes tests for checking the connection to the database, inserting and retrieving data,
 * and ensuring that the data is stored correctly.
 */
@DataMongoTest
@Testcontainers
public class DatabaseIntegrationTest extends AbstractContainerBaseTest {

  @Autowired private StudentRepository studentRepository;

  @Autowired private ProjectRepository projectRepository;

  private static Student mockStudent;
  private static Project mockProject;

  /**
   * Initial setup for the test class. This method is executed once before all tests in the class.
   * It initializes the mock data for the student and project objects that will be used in the
   * tests.
   */
  @BeforeAll
  static void initialSetup() {
    mockStudent =
        new Student(
            "999",
            "Test Student",
            "Test University",
            "Test Attending University",
            "Test City",
            "http://cv.com/test",
            "Bachelor",
            List.of("Note1", "Note2"),
            Map.of("LinkedIn", "http://linkedin.com/test"),
            "Test Studies Description",
            "Test Studies Field",
            "Test Studies Type",
            "Test Why Good Creator",
            "Test Why Join Demola",
            "Test Why Role",
            List.of(
                new ApplicationData(
                    "999",
                    "Test Project",
                    "1",
                    1L,
                    "Candidate",
                    false,
                    "",
                    "Test Love AI",
                    "Test Project fits my goals")),
            "Test Fake Name");

    mockProject =
        new Project(
            "999",
            "Test Project",
            "Test Description",
            List.of(1L, 2L),
            List.of("AI", "Machine Learning"),
            List.of("Technology"));
  }

  /**
   * Setup method for each test. This method is executed before each test in the class. It
   * initializes the database by deleting all existing records and importing mock data from JSON
   * files.
   */
  @BeforeEach
  void setUp() {
    studentRepository.deleteAll();
    projectRepository.deleteAll();
    init();
  }

  /**
   * Test to check the connection to the MongoDB database. It verifies that the student and project
   * repositories are not null and that the initial counts of students and projects are greater than
   * zero.
   */
  @Test
  void testMongoDbConnection() {
    var studentCount = studentRepository.count();
    var projectCount = projectRepository.count();

    assertThat(studentCount).isGreaterThan(0);
    assertThat(projectCount).isGreaterThan(0);
  }

  /**
   * Test to check the count of students in the database. It verifies that the count of students
   * after inserting a mock student is greater than the count before insertion.
   */
  @Test
  void testInsertAndCheckCount() {
    var countBefore = studentRepository.count();
    studentRepository.save(mockStudent);
    var countAfter = studentRepository.count();

    assertThat(countAfter).isGreaterThan(countBefore);
  }

  /**
   * Test to check the count of projects in the database. It verifies that the count of projects
   * after inserting a mock project is greater than the count before insertion.
   */
  @Test
  void testInsertAndRetrieveStudent() {
    studentRepository.save(mockStudent);
    var mockStudentId = mockStudent.getId();
    var retrievedStudent = studentRepository.findById(mockStudentId).orElse(null);

    assertThat(retrievedStudent).isNotNull();
    assertThat(retrievedStudent.getName()).isEqualTo(mockStudent.getName());
  }

  /**
   * Test to check the insertion and retrieval of a project from the database. It verifies that the
   * project is saved correctly and can be retrieved by its ID.
   */
  @Test
  void testInsertAndRetrieveProject() {
    projectRepository.save(mockProject);
    var retrievedProject = projectRepository.findById(mockProject.getId()).orElse(null);

    assertThat(retrievedProject).isNotNull();
    assertThat(retrievedProject.getName()).isEqualTo(mockProject.getName());
  }
}
