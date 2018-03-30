var MidiPlayer = require('midi-player-js');
var Soundfont = require('soundfont-player');
var ac = new AudioContext()

function initMidiPlayer(instrument, soundId, playerOnload) {
    const midiPlayer = new MidiPlayer.Player(function(event) {
        if(event.name == 'Note on' && event.velocity > 0) {
            instrument.play(event.noteName, ac.currentTime, { gain: event.velocity/100 });
        };
    });

    const url = 'http://localhost:3000/midi-example/' + soundId + '.mid';
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'arraybuffer';
    request.send(null);
    request.onreadystatechange = function() {
        if (request.readyState === 4 && request.status === 200) {
            const fileContent = request.response;
            midiPlayer.loadArrayBuffer(fileContent);
            playerOnload();
        }
    };
    return midiPlayer;
}

function initSoundPlayer(browserPlayer, soundId) {
    Soundfont.instrument(ac, 'clavinet').then(function(instrument) {
        const onloadFunc = function() { browserPlayer.playerOnload(soundId) };
        browserPlayer.players[soundId] = initMidiPlayer(instrument, soundId, onloadFunc);
    });
}

const browserPlayer = {
    playState: [],
    players: [],
    clickPlayButton: function(soundId) {
        const elem = this.getElement(soundId);
        if(this.playState[soundId]) {
            this.playState[soundId] = false;
            elem.innerHTML = '&#9654; Play';
            this.players[soundId].stop();
        }
        else {
            this.playState[soundId] = true;
            elem.innerHTML = '&#9632; Stop';
            this.players[soundId].play();
        }
    },
    getElement: function(soundId) {
        const elemId = `play-button-${soundId}`;
        return document.getElementById(elemId);
    },
    playerOnload: function(soundId) {
        const elem = this.getElement(soundId);
        elem.innerHTML = '&#9654; Play';
        const self = this;
        const elemSoundId = soundId;
        elem.onclick = function() { self.clickPlayButton(elemSoundId) };
    }
};

window.onload = function() {
    let soundId = 0;
    while(document.getElementById(`play-button-${soundId}`)) {
        const elem = browserPlayer.getElement(soundId);
        browserPlayer.playState[soundId] = false;
        initSoundPlayer(browserPlayer, soundId);
        soundId++;
    }
};
