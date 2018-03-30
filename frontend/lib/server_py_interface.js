const child_process = require('child_process');

function PyCommunicator() {
    console.log('Init python process');
    const path = '../backend/evolve_music/__init__.py';
    console.log(path);
    this.process = child_process.spawn('python3', [path]);
    this.process.stdout.on('data', (data) => {
        console.log('Vivaldi sucks:');
        console.log(data.toString());
    });
    this.process.stdout.on('end', function() {
        console.log('End:');
    });
}

/**
 * Proceeds to new generation in the evolution
 * @param ranks [Array] user's ranking of current iteration
 * @param to_call [function] function to call when response with new generation is acheived
 */
PyCommunicator.prototype.newGeneration = function (ranks, to_call) {
    console.log('New iteration');
    console.log(JSON.stringify(ranks));
    console.log('Sent');
    this.process.stdout.on('data', (data) => {
        console.log('Data:');
        console.log(data.toString());
        to_call(data.toString());
    });
    this.process.stdin.write(JSON.stringify(ranks) + '\n');
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