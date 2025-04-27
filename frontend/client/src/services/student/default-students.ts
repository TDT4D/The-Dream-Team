/* Types */
import { Project } from "../../types/Project";
import { Student } from "../../types/Student";

/* Components, services & etc. */
import { defaultProjects } from "../project/default-projects";

export const defaultStudents: Array<Student> = [
  {
    id: 0,
    name: "Student Test 0",
    homeUniversity: "Tuni",
    attendingUniversity: "Tuni",
    city: "Tre",
    cvLink: "",
    degreeLevelType: "bsc",
    notes: [],
    socialNetworkLinks: new Map(),
    studiesDescription: "",
    studiesField: "ITC",
    studiesType: "hard",
    whyGoodCreator: "reasons",
    whyJoinDemola: "good reasons",
    whyRole: "moti",
    applications: [],
  },
  {
    id: 1,
    name: "Student Test 1",
    homeUniversity: "Tuni",
    attendingUniversity: "Tuni",
    city: "Tre",
    cvLink: "",
    degreeLevelType: "bsc",
    notes: [],
    socialNetworkLinks: new Map(),
    studiesDescription: "",
    studiesField: "ITC",
    studiesType: "hard",
    whyGoodCreator: "reasons",
    whyJoinDemola: "good reasons",
    whyRole: "moti",
    applications: [],
  },
  {
    id: 2,
    name: "Student Test 2",
    homeUniversity: "Tuni",
    attendingUniversity: "Tuni",
    city: "Tre",
    cvLink: "",
    degreeLevelType: "bsc",
    notes: [],
    socialNetworkLinks: new Map(),
    studiesDescription: "",
    studiesField: "ITC",
    studiesType: "hard",
    whyGoodCreator: "reasons",
    whyJoinDemola: "good reasons",
    whyRole: "moti",
    applications: [],
  },
  {
    id: 3,
    name: "Student Test 3",
    homeUniversity: "Tuni",
    attendingUniversity: "Tuni",
    city: "Tre",
    cvLink: "",
    degreeLevelType: "bsc",
    notes: [],
    socialNetworkLinks: new Map(),
    studiesDescription: "",
    studiesField: "ITC",
    studiesType: "hard",
    whyGoodCreator: "reasons",
    whyJoinDemola: "good reasons",
    whyRole: "moti",
    applications: [],
  },
  {
    id: 4,
    name: "Student Test 4",
    homeUniversity: "Tuni",
    attendingUniversity: "Tuni",
    city: "Tre",
    cvLink: "",
    degreeLevelType: "bsc",
    notes: [],
    socialNetworkLinks: new Map(),
    studiesDescription: "",
    studiesField: "ITC",
    studiesType: "hard",
    whyGoodCreator: "reasons",
    whyJoinDemola: "good reasons",
    whyRole: "moti",
    applications: [],
  },
];

export const hashCode = (str: string): number => {
  let h: number = 0;
  [...str].forEach((c) => {
    h = 31 * h + c.charCodeAt(0);
    h ^= h >> 16;
    h &= 0xffffffff;
  });
  return h & ~0x80000000;
};

export const defaultStudentsForEachProject = (projectId: Project["id"]) => {
  const projectAsString = defaultProjects
    .filter((p) => p.id === projectId)
    .map((p) => JSON.stringify(p))[0];

  const students: Student[] = [];
  defaultStudents.forEach((student) => {
    if (hashCode(JSON.stringify(student) + projectAsString) >= 0x3fffffff)
      students.push(student);
  });
  return students;
};
