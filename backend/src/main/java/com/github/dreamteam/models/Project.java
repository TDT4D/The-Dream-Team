package com.github.dreamteam.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

@Document(collection = "projects")
@Data
@AllArgsConstructor
public class Project {
    @Id
    private Long id;
    private String name;
    private String description;
    private List<Long> batchesIds;
    private List<String> tags;
    private List<String> themes;
}