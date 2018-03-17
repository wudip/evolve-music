module.exports = {
  entry: './lib/browser.js',
  output: {
    filename: './bundle.js'
  },
  target: 'web',
  node: {
    fs: "empty",
    module: "empty"
  }
};