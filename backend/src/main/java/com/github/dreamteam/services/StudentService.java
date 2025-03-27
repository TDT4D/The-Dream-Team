package com.github.dreamteam.services;

import java.util.Collection;
import org.bson.Document;

public interface StudentService {
    public Collection<Document> getStudentsByProject(Long projectId);

}
