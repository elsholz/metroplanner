const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const colorThemeRoutes = express.Router();
const mongodb = require('mongodb')

// This will help us connect to the database
const dbo = require("../db/conn");


colorThemeRoutes.route("/api/themes/:colorThemeID").get(async function (req, res) {
  const dbConnection = dbo.getDb();
  // Get records
  let themeID = new mongodb.ObjectId(req.params["colorThemeID"])

  dbConnection
    .collection("colorThemes")
    .findOne({ "_id": themeID }, (findThemeErr, findThemeRes) => {
      if (findThemeErr) {
        console.log(`Error finding theme ${themeID}`, findThemeErr)
        res.status(500)
        res.send("Error fetching listings!");
      } else {
        if (findThemeRes) {
          if (findThemeRes.public) {
            console.log(`Found theme for id ${themeID}`)
            res.status(200)
            res.send(JSON.stringify(findThemeRes));
          } else {
            console.log(`Found theme, but it isn't public, for id ${themeID}`)
            // TODO: Authentication and authorization
            res.status(403)
            res.send("Forbidden")
          }
        } else {
          console.log(`No error, but didn't find theme for id ${themeID}`)
          res.status(404)
          res.send("Not Found")
        }
      }
    });
});

module.exports = colorThemeRoutes;
