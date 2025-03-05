const user = process.env.MONGODB_USERNAME ?? fs.readFileSync(process.env.MONGODB_USERNAME_FILE, 'utf8').trim();
const password = process.env.MONGODB_PASSWORD ?? fs.readFileSync(process.env.MONGODB_PASSWORD_FILE, 'utf8').trim();

// Create connection to mongo
const conn = new Mongo();
const db = conn.getDB(process.env.MONGODB_INITDB_DATABASE);

// Auth as the root user
db.auth({
    user: process.env.MONGODB_INITDB_ROOT_USERNAME,
    pwd: process.env.MONGODB_INITDB_ROOT_PASSWORD
});

// Create the user
db.createUser({
  user: user,
  pwd: password,
  roles: [
    {
      role: 'readWrite',
      db: process.env.MONGODB_DATABASE
    }
  ]
});

// Create new database
const newDb = db.getSiblingDB(process.env.MONGODB_DATABASE);

// Create collections
newDb.createCollection('students');
newDb.createCollection('projects');

// Create indices
// TODO: Add indices