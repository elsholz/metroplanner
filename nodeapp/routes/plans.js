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
recordRoutes.route(["/api/p/:shortlink", "/api/plan/:planid"]).get(async function (req, res) {
  const dbConnection = dbo.getDb();

  let shortLink = req.params["shortlink"]
  let planID = req.params["planid"]

  function updateStatsAndGetPlanData(planID, link) {
    dbConnection
      .collection("stats")
      .updateOne({
        _id: {
          "plan": findRes._id,
          "link": link,
        },
      }, {
        $push: {
          views: {
            // TODO
            user: undefined,
            at: (new Date()).toISOString()
          }
        }
      }, (updateErr, updateRes) => {
        if (updateErr) {
          console.log(updateErr)
          res.send("Error updating stats!");
        } else {
          dbConnection
            .collection("plans")
            .findOne({
              _id: planID
            }, (planErr, planRes) => {
              if (planErr) {
                console.log(planErr)
                res.send("Error fetching plan data!");
              } else {
                res.send(JSON.stringify(findRes));
              }
            })
        }
      })
  }
  if (planID) {
    updateStatsAndGetPlanData(planID, planID)
  } else {
    dbConnection
      .collection("links")
      .findOne({
        "_id": shortLink,
      }, (findErr, findRes) => {
        if (findErr) {
          console.log(findErr)
          res.send("Error getting shortlink!");
        } else {
          planID = findRes._id
          updateStatsAndGetPlanData(planID, shortLink)
        }
      });
  }


});

module.exports = recordRoutes;
