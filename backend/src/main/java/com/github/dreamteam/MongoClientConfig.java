package com.github.dreamteam;

// TODO: imports
import org.springframework.data.mongodb.config.AbstractMongoClientConfiguration;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MongoClientConfig extends AbstractMongoClientConfiguration {

    // TODO: implement methods
    @Override
    protected String getDatabaseName() {
        return "FIXME";
    }
}