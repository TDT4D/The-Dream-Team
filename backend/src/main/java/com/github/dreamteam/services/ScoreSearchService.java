package com.github.dreamteam.services;

import java.util.Collection;
import org.bson.Document;

public interface ScoreSearchService {
    Collection<Document> searchScores(String projectId);
}