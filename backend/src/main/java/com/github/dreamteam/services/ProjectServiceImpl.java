package com.github.dreamteam.services;

import com.github.dreamteam.exceptions.EntityNotFoundException;
import com.mongodb.client.MongoCollection;
import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

@Service
public class ProjectServiceImpl implements ProjectService {

        private static final Logger LOGGER = LoggerFactory.getLogger(ProjectServiceImpl.class);
        private final MongoCollection<Document> projectCollection;
        // TODO: Add index

        public ProjectServiceImpl(MongoTemplate mongoTemplate) {
                this.projectCollection = mongoTemplate.getCollection("projects");
        }

        public Collection<Document> getAllProjects(int limit) {
                LOGGER.info("Fetching all projects from MongoDB with limit {}", limit);
                // connect to MongoDB and fetch all projects
                List<Document> projects = projectCollection.find().limit(limit).into(new ArrayList<>());
                if (projects.isEmpty()) {
                        throw new EntityNotFoundException("No projects found");
                }
                return projects;
        }
}