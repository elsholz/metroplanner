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
const dbConnection = dbo.getDb();

// Get stats for a plan (all shortlinks included)
recordRoutes.route(["/api/stats/:planID"]).get(async function (req, res) {
  let planID = req.params["planID"]

  dbConnection
    .collection("stats")
    .find({ "plan": planID }, (err, result) => {
      if (err) {
        console.log(err)
        res.send("Error fetching listings!");
      } else {
        res.send(JSON.stringify(result));
      }
    });
});

module.exports = recordRoutes;
