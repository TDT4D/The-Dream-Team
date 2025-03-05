//index.js
const express = require('express');
const app = express();
const path = require("path");
const cors = require('cors');

app.use(cors());
app.use(express.static(path.join(__dirname, process.env.BUILD_PATH || '../client/dist')));

app.get("/api", (req, res) => {
    fetch("http://localhost:8080").then(d => d.text()).then(d => res.send(d))
})

app.get("/api/projects", (req, res) => {
    res.send(
        [
            {
                id: 1,
                name: "test 1"
            },
            {
                id: 2,
                name: "test 2"
            },
            {
                id: 3,
                name: "test 3"
            },
            {
                id: 4,
                name: "test 4"
            },
            {
                id: 5,
                name: "test 5"
            },
            {
                id: 6,
                name: "test 6"
            },
        ]
    );
});

app.get("/api/projects/:id/students", (req, res) => {
    console.log(req.headers)
    res.send([
        {
            id: 0,
            name: "Student Test 0" + req.params.id,
        },
        {
            id: 1,
            name: "Student Test 1" + req.params.id,
        },
        {
            id: 2,
            name: "Student Test 2" + req.params.id,
        },
        {
            id: 3,
            name: "Student Test 3" + req.params.id,
        },
        {
            id: 4,
            name: "Student Test 4" + req.params.id,
        },
    ]);
})

// TODO: NUKE THIS
app.get('**', (req, res) => {
    res.redirect("/")
})

app.listen(3000, () => {
    console.log('server listening on port 3000')
})