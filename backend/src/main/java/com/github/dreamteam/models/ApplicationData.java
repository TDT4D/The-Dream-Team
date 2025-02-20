package com.github.dreamteam.models;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class ApplicationData {
    private Long projectId;
    private String projectName;
    private Long studentId;
    private Long chosenBatch;
    private String relation;
    private boolean staffInsertion;
    private String dropoutExplanation;
    private String whyExperience;
    private String whyProject;
}
