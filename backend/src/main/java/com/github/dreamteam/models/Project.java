package com.github.dreamteam.models;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "projects")
@Data
@AllArgsConstructor
public class Project {
  @Id private String id;
  private String name;
  private String description;
  private List<Long> batchesIds;
  private List<String> tags;
  private List<String> themes;
}
