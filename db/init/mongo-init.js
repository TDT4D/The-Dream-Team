const user = fs.readFileSync(process.env.MONGODB_USERNAME_FILE, 'utf8').trim();
const password = fs.readFileSync(process.env.MONGODB_PASSWORD_FILE, 'utf8').trim();

// Create connection to mongo
const conn = new Mongo();
const db = conn.getDB('admin');

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
