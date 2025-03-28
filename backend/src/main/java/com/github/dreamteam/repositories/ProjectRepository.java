package com.github.dreamteam.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.github.dreamteam.models.Project;

@Repository
public interface ProjectRepository extends MongoRepository<Project, String> {
}
