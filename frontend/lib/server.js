const express = require('express');
const PyCommunicator = require('./server_py_interface').PyCommunicator;
const atob = require('atob');

let midiFiles = ['a', 'b', 'c', 'd'];

function saveMidis(soundtracks) {
    for(let i = 0; i < midiFiles.length; i++) {
        midiFiles[i] = soundtracks[i];
    }
}

const app = express();
app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.static('dist'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', function (req, res) {
  res.render('index');
});

py_communicator = new PyCommunicator(saveMidis);

app.post('/', function(req, res) {
    let soundtrack_id = 0;
    const ranks = [];
    while(req.body.hasOwnProperty(`rank_${soundtrack_id}`)) {
        const elem_id = `rank_${soundtrack_id}`;
        ranks[soundtrack_id] = req.body[elem_id];
        soundtrack_id++;
    }

    py_communicator.newGeneration(ranks, function(data) {
        saveMidis(data);
        res.render('index');
    });
});

app.get('/midi/*.mid', function (req, res) {
    const urlPieceis = req.originalUrl.split('/');
    const fileName = urlPieceis[urlPieceis.length - 1];
    const fileNamePieces = fileName.split('.');
    if(fileNamePieces.length !== 2) {
        console.log('Requesting invalid URL: ' +  req.originalUrl);
    }
    const soundtrackIdStr = fileNamePieces[0];
    const soundtrackId = Number(soundtrackIdStr);
    console.log(soundtrackId);
    console.log(midiFiles);
    if(soundtrackId >= 0 && soundtrackId < midiFiles.length) {
        const baseSoundtrack = midiFiles[soundtrackId];
        res.type('audio/midi');
        const arr = atob(baseSoundtrack);
        res.end(arr, 'binary');
    }
});

port = 3000;
app.listen(port, function () {
  console.log(`Listening on port ${port}!`)
});
