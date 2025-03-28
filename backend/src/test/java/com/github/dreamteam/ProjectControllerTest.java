package com.github.dreamteam;

import static org.mockito.Mockito.*;
import static org.assertj.core.api.Assertions.assertThat;

import com.github.dreamteam.services.ProjectServiceImpl;
import com.github.dreamteam.services.StudentService;
import com.github.dreamteam.controllers.ProjectController;
import jakarta.servlet.http.HttpServletRequest;
import org.bson.Document;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpStatus;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.View;
import java.util.List;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
class ProjectControllerTests {

    @Mock
    private ProjectServiceImpl projectService;

    @Mock
    private StudentService studentService;

    @Mock
    private HttpServletRequest request;

    @InjectMocks
    private ProjectController projectController;

    @BeforeEach
    void setUp() {
        reset(projectService, studentService, request);
    }

    @Test
    void testGetProjectsWithoutLimit() {
        when(projectService.getAllProjects(0)).thenReturn(List.of(new Document("name", "Project A")));
        
        var projects = projectController.getProjects(Optional.empty(), Optional.empty());
        
        assertThat(projects).hasSize(1);
        assertThat(projects.iterator().next().get("name")).isEqualTo("Project A");
    }

    @Test
    void testGetProjectsWithLimit() {
        when(projectService.getAllProjects(2)).thenReturn(List.of(new Document("name", "Project A"), new Document("name", "Project B")));
        
        var projects = projectController.getProjects(Optional.empty(), Optional.of(2));
        
        assertThat(projects).hasSize(2);
    }

    @Test
    void testGetStudentsByProject() {
        when(studentService.getStudentsByProject(101L)).thenReturn(List.of(new Document("name", "John Doe")));
        
        var students = projectController.getStudents(101L);
        
        assertThat(students).hasSize(1);
        assertThat(students.iterator().next().get("name")).isEqualTo("John Doe");
    }

    @Test
    void testPredictRedirect() {
        var response = projectController.predict(request);
        
        assertThat(response.getViewName()).isEqualTo("redirect:/ml/score/predict");
        verify(request).setAttribute(View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.PERMANENT_REDIRECT);
    }

    @Test
    void testGetScoresRedirect() {
        var response = projectController.getScores(request, 101L, Optional.of("file.csv"));
        
        assertThat(response.getViewName()).isEqualTo("redirect:/ml/score/scores?projectId=101&scoreFile=file.csv");
        verify(request).setAttribute(View.RESPONSE_STATUS_ATTRIBUTE, HttpStatus.PERMANENT_REDIRECT);
    }
}
