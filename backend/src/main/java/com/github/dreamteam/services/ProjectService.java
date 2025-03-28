package com.github.dreamteam.services;

import java.util.Collection;

import org.bson.Document;

public interface ProjectService {
    public Collection<Document> getAllProjects(int limit);
}
