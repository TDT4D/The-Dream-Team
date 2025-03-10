package com.github.dreamteam;

import org.springframework.data.mongodb.config.AbstractMongoClientConfiguration;

import com.mongodb.MongoClientSettings;
import com.mongodb.ConnectionString;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MongoClientConfig extends AbstractMongoClientConfiguration {

    private static final Logger LOGGER = LoggerFactory.getLogger(MongoClientConfig.class);

    @Value("${spring.data.mongodb.database}")
    private String databaseName;

    @Value("${spring.data.mongodb.uri}")
    private String connectionString;

    @Override
    protected String getDatabaseName() {
        return databaseName;
    }

    @Bean
    public MongoClientSettings mongoClientSettings() {
        // Log connection string, but leave out credentials
        String redactedString = connectionString.replaceAll("://[^:]+:([^@]+)@", "://<credentials>@");
        LOGGER.info("Connecting to MongoDB at {}", redactedString);
        return MongoClientSettings.builder()
                .applyConnectionString(new ConnectionString(connectionString))
                .build();
    }
}