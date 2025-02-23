package com.github.dreamteam.services;

import com.github.dreamteam.models.Project;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProjectServiceImpl implements ProjectService {

    public List<Project> getAllProjects() {
        return List.of(
                new Project(1L, "AI-powered Chatbot",
                        "A chatbot that uses AI to answer customer queries.",
                        List.of(101L, 102L),
                        List.of("AI", "Chatbot", "NLP"),
                        List.of("Machine Learning")),

                new Project(2L, "Smart Traffic Control",
                        "A system that optimizes traffic flow using sensors and AI.",
                        List.of(103L),
                        List.of("IoT", "AI", "Traffic Management"),
                        List.of("Smart Cities")),

                new Project(3L, "Blockchain-based Voting System",
                        "A secure and transparent voting system using blockchain.",
                        List.of(101L, 104L),
                        List.of("Blockchain", "Security", "Elections"),
                        List.of("Cybersecurity")));
    }
}