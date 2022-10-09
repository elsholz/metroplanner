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


recordRoutes.route("/api/themes/:colorThemeID").get(async function (req, res) {
  // Get records
  let themeID = new mongodb.ObjectId(req.params["colorThemeID"])

  dbConnection
    .collection("colorThemes")
    .findOne({ "_id": themeID}, (err, result) => {
      if (err) {
        res.send("Error fetching listings!");
      } else {
        res.send(JSON.stringify(result));
      }
    });
});

module.exports = recordRoutes;
