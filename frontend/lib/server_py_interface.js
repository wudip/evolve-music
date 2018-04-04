const child_process = require('child_process');

function PyCommunicator() {
    console.log('Init python process');
    const path = '__init__.py';
    console.log(path);
    this.process = child_process.spawn('python3', [path], {cwd: '../backend/evolve_music/'});
    this.process.stderr.on('data', (data) => {
        console.log('Error:');
        console.log(data.toString());
    });
    this.process.on('close', function() {
        console.log('EXIT');
    });
    this.received_data = '';
}

/**
 * Proceeds to new generation in the evolution
 * @param ranks [Array] user's ranking of current iteration
 * @param to_call [function] function to call when response with new generation is acheived
 */
PyCommunicator.prototype.newGeneration = function (ranks, to_call) {
    console.log('New iteration');
    console.log(JSON.stringify(ranks));
    console.log('Sending');
    this.process.stdout.on('data', (data) => {
        //console.log('Data:');
        //console.log(data.toString());
        this.received_data += data.toString();
        let json_data = undefined;
        try {
            json_data = JSON.parse(this.received_data);
        } catch (e) {
            return;
        }
        this.received_data = '';
        to_call(json_data);
    });
    this.process.stdin.write(JSON.stringify(ranks) + '\n');
    console.log('Sent');
};

/**
 * @return best soundtrack in current generation
 */
PyCommunicator.prototype.getBest = function () {
    console.log('Get best');
    this.process.stdin.end();
    this.process.stdout.on('data', function (data) {
        console.log('END');
        console.log(data.toString());
    });
};

module.exports = {
    PyCommunicator: PyCommunicator
};