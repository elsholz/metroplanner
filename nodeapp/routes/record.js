const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const recordRoutes = express.Router();
const http = require('http')
const fs = require('fs')
const mongodb = require('mongodb')

const viewer = require("../js/viewer")


// This will help us connect to the database
const dbo = require("../db/conn");

// This section will help you get a list of all the records.
recordRoutes.route("/p").get(async function (req, res) {
  // Get records
  const dbConnect = dbo.getDb();

  dbConnect
    .collection("plans")
    .find()
    .project({ planName: 1 })
    .toArray(function (err, result) {
      if (err) {
        res.send("Error fetching listings!");
      } else {
        res.json(result);
      }
    });
});

// list all plans
recordRoutes.route("/p").get(async function (req, res) {
  // Get records
  const dbConnect = dbo.getDb();

  dbConnect
    .collection("plans")
    .findAll({}, (err, result) => {
      if (err) {
        res.send("Error fetching listings!");
      } else {
        res.send(JSON.stringify(result));
      }
    });
});

recordRoutes.route("/api/p/:planid").get(async function (req, res) {
  // Get records
  const dbConnect = dbo.getDb();
  let planid = new mongodb.ObjectId(req.params["planid"])
  console.log(planid)

  dbConnect
    .collection("plans")
    .findOne({ "_id": planid }, (err, result) => {
      if (err) {
        res.send("Error fetching listings!");
      } else {
        res.send(JSON.stringify(result));
      }
    });
});
recordRoutes.route("/p/:planid").get(async function (req, res) {

  /*https.get('/api/p/' + req.params["planid"], (resp) => {
    let data = '';

    // A chunk of data has been received.
    resp.on('data', (chunk) => {
      data += chunk;
    });

    // The whole response has been received. Print out the result.
    resp.on('end', () => {
      console.log(JSON.parse(data).explanation);
    });

  }).on("error", (err) => {
    console.log("Error: " + err.message);
  });*/

  // let readStream = fs.createReadStream('./html/map_viewer.html')
  // const chunks = [];

  // readStream.on("data", function (chunk) {
  //   chunks.push(chunk);
  // });

  // readStream.on("end", function () {
  //   let html = Buffer.concat(chunks)

  //   console.log(html)
  //   //res.writeHead(200, { 'content-type': 'text/html' })
  //   html.pipe(res) // res.pipe(html)
  // });

  res.send(viewer.getHTML())

  // .pipe(res)
});

recordRoutes.route("/edit/:planid").get(async function (req, res) {
  res.writeHead(200, { 'content-type': 'text/html' })
  fs.createReadStream('./html/map_editor.html').pipe(res)
});
recordRoutes.route("/style.css").get(async function (req, res) {
  res.writeHead(200, { 'content-type': 'text/css' })
  fs.createReadStream('./css/style.css').pipe(res)
});
recordRoutes.route("/metroplanner.js").get(async function (req, res) {
  res.writeHead(200, { 'content-type': 'text/javascript' })
  fs.createReadStream('./js/metroplanner.js').pipe(res)
});
recordRoutes.route("/html_templates.js").get(async function (req, res) {
  res.writeHead(200, { 'content-type': 'text/javascript' })
  fs.createReadStream('./js/html_templates.js').pipe(res)
});

recordRoutes.route("/img/:path").get(async function (req, res) {
  res.writeHead(200, { 'content-type': 'image/png' })
  console.log(req.params)
  fs.createReadStream(req.params["path"]).pipe(res)
});

recordRoutes.route("/").get(async function (req, res) {
  res.writeHead(200, { 'content-type': 'text/html' })
  fs.createReadStream('./index.html').pipe(res)
})

// This section will help you create a new record.
recordRoutes.route("/listings/recordSwipe").post(function (req, res) {
  // Insert swipe informations
});

// This section will help you update a record by id.
recordRoutes.route("/listings/updateLike").post(function (req, res) {
  // Update likes
});

// This section will help you delete a record
recordRoutes.route("/listings/delete").delete((req, res) => {
  // Delete documents
});

module.exports = recordRoutes;
