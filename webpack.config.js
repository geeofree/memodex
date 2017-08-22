const ExtractTextPlugin = require('extract-text-webpack-plugin')
const webpack           = require('webpack')
const path              = require('path')

const ExtractCSS = new ExtractTextPlugin('style.css')
const WebpackHMR = new webpack.HotModuleReplacementPlugin()

const DevPath       = path.join(__dirname, 'dist')
const EntryPath     = path.join(DevPath, 'app.js')
const FlaskViewPath = path.join(__dirname, 'memodex', 'views', 'app', 'static', 'app')

module.exports = {
  entry: EntryPath,
  output: {
    path: FlaskViewPath,
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: 'babel-loader',
        exclude: /node_modules/
      },
      {
        test: /\.s(a|c)ss$/,
        use: ExtractCSS.extract(['css-loader', 'postcss-loader', 'sass-loader'])
      }
    ]
  },
  devServer: {
    hot: true,
    port: 3000,
    compress: true,
    contentBase: DevPath
  },
  plugins: [
    ExtractCSS,
    WebpackHMR
  ]
}
