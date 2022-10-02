const http = require('http')
const mongodb = require('mongodb')
const dbo = require("../db/conn");
const fs = require('fs')

module.exports = {
    getHTML:
        function () {
            let text = fs.readFileSync('./html/map_viewer.html', 'utf8')
            return text
        }
};
