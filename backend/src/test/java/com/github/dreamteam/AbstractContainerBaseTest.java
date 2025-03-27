// package com.github.dreamteam;

// import org.springframework.test.context.DynamicPropertyRegistry;
// import org.springframework.test.context.DynamicPropertySource;
// import org.testcontainers.containers.MongoDBContainer;
// import org.testcontainers.utility.DockerImageName;
// import org.testcontainers.utility.MountableFile;

// public class AbstractContainerBaseTest {

//     protected static final MongoDBContainer mongoDBContainer;

//     static {
//         mongoDBContainer = new MongoDBContainer(DockerImageName.parse("mongo:7.0.16"));
//         mongoDBContainer.start();
//         mongoDBContainer.copyFileToContainer(MountableFile.forClasspathResource("/mongo/article.json"),
//                 "/article.json");
//         try {
//             mongoDBContainer.execInContainer("mongoimport", "-d", "test", "-c", "article", "--file", "/article.json",
//                     "--jsonArray");
//         } catch (Exception e) {
//             // logger
//         }
//     }

//     @DynamicPropertySource
//     static void mongoDbProperties(DynamicPropertyRegistry registry) {
//         registry.add("spring.data.mongodb.uri", mongoDBContainer::getReplicaSetUrl);
//     }
// }