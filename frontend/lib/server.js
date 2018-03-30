const express = require('express');
const PyCommunicator = require('./server_py_interface').PyCommunicator;

const app = express();
app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.static('dist'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', function (req, res) {
  res.render('index');
});

py_communicator = new PyCommunicator();

app.post('/', function(req, res) {
    let soundtrack_id = 0;
    const ranks = [];
    while(req.body.hasOwnProperty(`rank_${soundtrack_id}`)) {
        const elem_id = `rank_${soundtrack_id}`;
        ranks[soundtrack_id] = req.body[elem_id];
        soundtrack_id++;
    }
    py_communicator.newGeneration(ranks, function(data) { res.render('index'); });
});

port = 3000;
app.listen(port, function () {
  console.log(`Listening on port ${port}!`)
});

app.get('/midi/', function (req, res) {
    res.render('index');
});
