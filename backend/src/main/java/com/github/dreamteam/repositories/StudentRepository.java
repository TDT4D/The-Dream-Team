package com.github.dreamteam.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.github.dreamteam.models.Student;

@Repository
public interface StudentRepository extends MongoRepository<Student, String> {
}
