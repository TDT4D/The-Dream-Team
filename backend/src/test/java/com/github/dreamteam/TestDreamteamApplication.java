package com.github.dreamteam;

import org.springframework.boot.SpringApplication;

public class TestDreamteamApplication {

	public static void main(String[] args) {
        // SpringApplication.run(DreamteamApplication.class, args);
		SpringApplication app = new SpringApplication(TestDreamteamApplication.class);
		// app.addInitializers(new TestContainerInitializer());
		app.run(args);
	}

}
