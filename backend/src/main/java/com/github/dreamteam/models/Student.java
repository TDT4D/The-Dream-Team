/**
 * This package has all the models for the backend. It is responsible for defining the data
 * structures used in the application.
 */
package com.github.dreamteam.models;

import java.util.List;
import java.util.Map;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

/**
 * Student represents the data structure used for storing student-related information. It includes
 * fields such as student ID, name, home university, attending university, city, CV link, degree
 */
@Document(collection = "students")
@Data
@AllArgsConstructor
public class Student {
  @Id private String id;
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
  private String fakeName; // Purely for demo purposes
}
