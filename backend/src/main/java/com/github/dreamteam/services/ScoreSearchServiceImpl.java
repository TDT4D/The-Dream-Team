package com.github.dreamteam.services;

import java.util.Collection;
import java.util.ArrayList;
import java.util.List;
import org.bson.Document;
import org.springframework.stereotype.Service;

@Service
public class ScoreSearchServiceImpl implements ScoreSearchService {

    @Override
    public Collection<Document> searchScores(String projectId) {
        List<Document> scores = new ArrayList<>();
        Document score = new Document();
        score.put("projectId", projectId);
        score.put("score", 100);
        scores.add(score);
        return scores;
    }
}