const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const recordRoutes = express.Router();
const http = require('http')
const fs = require('fs')
const mongodb = require('mongodb')

// This will help us connect to the database
const dbo = require("../db/conn");

// Returns a plan given a shortlink. This will not publish the plan ID to the user.
recordRoutes.route(["/api/p/:shortlink"]).get(async function (req, res) {
  const dbConnection = dbo.getDb();
  let shortLink = req.params["shortlink"]

  console.log("GET for /api/p/" + shortLink)

  dbConnection
    .collection("links")
    .findOne({
      "_id": shortLink,
    }, (findLinkErr, findLinkRes) => {
      if (findLinkErr) {
        console.log(findLinkErr)
        res.send("Error getting shortlink!");
      } else {
        console.log(findLinkRes)

        let planID = new mongodb.ObjectId(findLinkRes._id)
        dbConnection
          .collection("stats")
          .updateOne({
            _id: {
              "plan": planID,
              "link": shortLink,
            },
          }, {
            $push: {
              views: (new Date()).toISOString()
            }
          }, (updateStatsErr, updateStatsRes) => {
            if (updateStatsErr) {
              console.log(updateStatsErr)
              res.send("Error updating stats!");
            } else {
              dbConnection
                .collection("plans")
                .findOne({
                  _id: planID
                }, (findPlanErr, findPlanRes) => {
                  if (findPlanErr) {
                    console.log(findPlanErr)
                    res.send("Error fetching plan data!");
                  } else {
                    let latestStateID = new mongodb.ObjectId(findPlanRes.history[-1])
                    dbConnection
                      .collection("planStates")
                      .findOne({
                        "_id": latestStateID
                      }, (findPlanStateErr, findPlanStateRes) => {
                        res.send(JSON.stringify(findPlanStateRes));
                      })
                  }
                })
            }
          })
      }
    });
});

module.exports = recordRoutes;
