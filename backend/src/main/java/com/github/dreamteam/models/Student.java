package com.github.dreamteam.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;
import java.util.Map;

@Document(collection = "students")
@Data
@AllArgsConstructor
public class Student {
    @Id
    private Long id;
    private String name;
    private String homeUniversity;
    private String attendingUniversity;
    private String city;
    private String cvLink;
    private String degreeLevelType;
    private List<String> notes;
    private Map<String, String> socialNetworkLinks;
    private String studiesDescription;
    private String studiesField;
    private String studiesType;
    private String whyGoodCreator;
    private String whyJoinDemola;
    private String whyRole;
    private List<ApplicationData> applications;
}
