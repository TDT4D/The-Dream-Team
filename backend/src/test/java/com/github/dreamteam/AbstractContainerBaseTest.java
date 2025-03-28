package com.github.dreamteam;

import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.MongoDBContainer;
import org.testcontainers.utility.DockerImageName;
import org.testcontainers.utility.MountableFile;

public class AbstractContainerBaseTest {

    protected static final MongoDBContainer mongoDBContainer;

    static {
        mongoDBContainer = new MongoDBContainer(DockerImageName.parse("mongo:7.0.16"));
        mongoDBContainer.start();
        mongoDBContainer.copyFileToContainer(MountableFile.forClasspathResource("/mock_students.json"),
                "/mock_students.json");
        mongoDBContainer.copyFileToContainer(MountableFile.forClasspathResource("/mock_projects.json"),
                "/mock_projects.json");
        init();
    }

    protected static final void init() {
        try {
            mongoDBContainer.execInContainer("mongoimport", "-d", "testdb", "-c", "students", "--file", "/mock_students.json",
            "--jsonArray");
    mongoDBContainer.execInContainer("mongoimport", "-d", "testdb", "-c", "projects", "--file", "/mock_projects.json",
            "--jsonArray");
        } catch (Exception e) {
            // logger
        }
    }

    @DynamicPropertySource
    static void mongoDbProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.data.mongodb.uri", mongoDBContainer::getReplicaSetUrl);
        registry.add("spring.data.mongodb.database", () -> "testdb");
    }
}