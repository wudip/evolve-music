const express = require('express')
const path = require('path');

const app = express()
app.set('view engine', 'ejs')
app.use(express.static('public'));
app.use(express.static('dist'));

app.get('/', function (req, res) {
  res.render('index');
})

port = 3000
app.listen(port, function () {
  console.log(`Listening on port ${port}!`)
})