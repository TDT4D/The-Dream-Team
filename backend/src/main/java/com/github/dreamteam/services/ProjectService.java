package com.github.dreamteam.services;

import com.github.dreamteam.models.Project;

import java.util.Collection;
import java.util.List;

import org.bson.Document;

public interface ProjectService {
    public Collection<Document> getAllProjects(int limit);
}
