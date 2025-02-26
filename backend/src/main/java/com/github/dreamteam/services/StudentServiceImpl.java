package com.github.dreamteam.services;

import com.github.dreamteam.models.ApplicationData;
import com.github.dreamteam.models.Student;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class StudentServiceImpl implements StudentService {

        private final Map<Long, List<Student>> projectApplicants = new ConcurrentHashMap<>();
        private final Map<Long, Student> studentMap = new ConcurrentHashMap<>();

        public StudentServiceImpl() {
                // Populate mock data
                List<Student> project1Students = List.of(
                                new Student(1L, "Alice Johnson", "Harvard University", null, "New York",
                                                "https://example.com/cv/alice.pdf", "Master's Degree",
                                                List.of("Great team player", "Creative thinker"),
                                                Map.of("LinkedIn", "https://linkedin.com/alicejohnson"),
                                                "Computer Science major with a focus on AI", "Computer Science",
                                                "Degree student", "Problem-solving, leadership, and coding",
                                                "Excited about working on real-world challenges", "Project Manager",
                                                List.of(new ApplicationData(1L, "AI Ethics Challenge", 1L, 101L,
                                                                "Interested", false, null,
                                                                "I have experience with AI research",
                                                                "This topic aligns with my thesis"))),
                                new Student(2L, "Bob Smith", "MIT", "Stanford University", "Boston",
                                                "https://example.com/cv/bob.pdf", "Bachelor’s Degree",
                                                List.of("Quick learner", "Strong analytical skills"),
                                                Map.of("GitHub", "https://github.com/bobsmith"),
                                                "Electrical Engineering with a minor in Robotics",
                                                "Engineering and technology",
                                                "Exchange student", "Good at breaking down complex problems",
                                                "Looking for hands-on experience", "Technical Lead",
                                                List.of(new ApplicationData(1L, "AI Ethics Challenge", 2L, 101L,
                                                                "Potential", false, null,
                                                                "I’ve worked on AI ethics before",
                                                                "I want to explore this further"))),
                                new Student(3L, "Charlie Davis", "Oxford University", null, "London",
                                                "https://example.com/cv/charlie.pdf", "Doctorate",
                                                List.of(),
                                                Map.of("Twitter", "https://twitter.com/charliedavis"),
                                                "Social Sciences research on human behavior", "Social Sciences",
                                                "Degree student", "Empathetic communicator and researcher",
                                                "Eager to collaborate with diverse teams", "Researcher",
                                                List.of(new ApplicationData(2L, "Mental Health Awareness", 3L, 202L,
                                                                "Selected", true, null,
                                                                "I have a background in psychology",
                                                                "Mental health is an important issue"))),
                                new Student(4L, "Diana Brown", "Stanford University", null, "San Francisco",
                                                "https://example.com/cv/diana.pdf", "Master's Degree",
                                                List.of("Detail-oriented", "Strong writing skills"),
                                                Map.of("Portfolio", "https://dianabrown.com"),
                                                "Journalism and Communications", "Journalism and Communications",
                                                "Degree student", "Passionate about storytelling",
                                                "Interested in social impact projects", "Content Creator",
                                                List.of(new ApplicationData(2L, "Mental Health Awareness", 4L, 202L,
                                                                "Interested", false, null,
                                                                "I have written about mental health",
                                                                "I want to raise awareness"))),
                                new Student(5L, "Eve White", "University of Tokyo", null, "Tokyo",
                                                "https://example.com/cv/eve.pdf", "Bachelor’s Degree",
                                                List.of("Fluent in Japanese", "Experience in event planning"),
                                                Map.of("Instagram", "https://instagram.com/evewhite"),
                                                "International Relations with a focus on East Asia",
                                                "International Relations",
                                                "Degree student", "Culturally sensitive and adaptable",
                                                "Passionate about cross-cultural communication", "Community Manager",
                                                List.of(new ApplicationData(2L, "Mental Health Awareness", 5L, 202L,
                                                                "Potential", false, null,
                                                                "I have organized mental health events",
                                                                "I want to help others"))));

                List<Student> project2Students = List.of(
                                new Student(6L, "Frank Green", "University of Sydney", null, "Sydney",
                                                "https://example.com/cv/frank.pdf", "Bachelor’s Degree",
                                                List.of("Experience in public speaking", "Strong leadership skills"),
                                                Map.of("YouTube", "https://youtube.com/frankgreen"),
                                                "Political Science with a minor in Economics", "Political Science",
                                                "Degree student", "Passionate about social justice",
                                                "Interested in policy analysis", "Policy Analyst",
                                                List.of(new ApplicationData(2L, "Mental Health Awareness", 6L, 202L,
                                                                "Interested", false, null,
                                                                "I have studied mental health policies",
                                                                "I want to contribute to this cause"))),
                                new Student(7L, "Grace Lee", "University of Toronto", null, "Toronto",
                                                "https://example.com/cv/grace.pdf", "Bachelor’s Degree",
                                                List.of("Experience in graphic design", "Creative problem solver"),
                                                Map.of("Behance", "https://behance.com/gracelee"),
                                                "Visual Arts with a focus on digital media", "Visual Arts",
                                                "Degree student", "Innovative and artistic",
                                                "Interested in social impact projects", "Visual Designer",
                                                List.of(new ApplicationData(2L, "Mental Health Awareness", 7L, 202L,
                                                                "Potential", false, null,
                                                                "I have designed mental health campaigns",
                                                                "I want to create awareness"))),
                                new Student(8L, "Henry Young", "University of Melbourne", null, "Melbourne",
                                                "https://example.com/cv/henry.pdf", "Bachelor’s Degree",
                                                List.of("Experience in web development", "Strong coding skills"),
                                                Map.of("CodePen", "https://codepen.com/henryyoung"),
                                                "Computer Science with a focus on web development", "Computer Science",
                                                "Degree student", "Tech-savvy and innovative",
                                                "Interested in social impact projects", "Web Developer",
                                                List.of(new ApplicationData(2L, "Mental Health Awareness", 8L, 202L,
                                                                "Interested", false, null,
                                                                "I have built mental health websites",
                                                                "I want to make a difference"))),
                                new Student(9L, "Ivy Brown", "University of California", null, "Los Angeles",
                                                "https://example.com/cv/ivy.pdf", "Bachelor’s Degree",
                                                List.of("Experience in marketing", "Strong communication skills"),
                                                Map.of("LinkedIn", "https://linkedin.com/ivybrown"),
                                                "Business Administration with a focus on social entrepreneurship",
                                                "Business Administration",
                                                "Degree student", "Entrepreneurial and strategic thinker",
                                                "Interested in social impact projects", "Marketing Specialist",
                                                List.of(new ApplicationData(2L, "Mental Health Awareness", 9L, 202L,
                                                                "Potential", false, null,
                                                                "I have marketed mental health campaigns",
                                                                "I want to raise awareness"))));

                List<Student> project3Students = List.of(
                                new Student(10L, "Jack White", "University of London", null, "London",
                                                "https://example.com/cv/jack.pdf", "Bachelor’s Degree",
                                                List.of("Experience in event planning", "Strong organizational skills"),
                                                Map.of("Twitter", "https://twitter.com/jackwhite"),
                                                "Event Management with a focus on sustainability", "Event Management",
                                                "Degree student", "Passionate about eco-friendly practices",
                                                "Interested in event planning", "Event Coordinator",
                                                List.of(new ApplicationData(3L, "Eco-Friendly Expo", 10L, 303L,
                                                                "Selected", true, null,
                                                                "I have organized eco-friendly events",
                                                                "I want to promote sustainability")))
                );


                // Populate project-based applicants
                projectApplicants.put(1L, project1Students);
                projectApplicants.put(2L, project2Students);
                projectApplicants.put(3L, project3Students);

                // Populate global student map
                project1Students.forEach(student -> studentMap.put(student.getId(), student));
                project2Students.forEach(student -> studentMap.put(student.getId(), student));
                project3Students.forEach(student -> studentMap.put(student.getId(), student));
        }

        public List<Student> getStudentsByProject(Long projectId) {
                return projectApplicants.getOrDefault(projectId, List.of());
        }

        public Student getStudentById(Long studentId) {
                return studentMap.get(studentId);
        }

        public String getStudentName(Long studentId) {
                Student student = studentMap.get(studentId);
                return (student != null) ? student.getName() : null;
        }
}
