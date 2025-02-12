//index.js
const express = require('express');
const app = express();
const path = require("path");
const cors = require('cors');
require("dotenv").config();


app.use(cors());
app.use(express.static(path.join(__dirname, process.env.BUILD_PATH || '../client/build')));

// TODO: NUKE THIS
app.get('**', (req, res) => {
    res.redirect("/")
})

app.listen(3000, () => {
    console.log('server listening on port 8080')
})