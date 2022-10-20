const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const planRoutes = express.Router();

// This will help us connect to the database
const dbo = require("../db/conn");

// Get List of currently popular plans shortlinks
planRoutes.route("/api/popularplans").get(async function (req, res) {
  const dbConnection = dbo.getDb();
  res.status(501)
  res.send("Not Implemented")
})

// Returns all public information about a plan, excluding its latest state, identified by its shortlink
planRoutes.route("/api/plan/:shortlink").get(async function (req, res) {
  const dbConnection = dbo.getDb();
  let shortLink = req.params["shortlink"]
  console.log("GET for /api/plan/" + shortLink)

  dbConnection
    .collection("links")
    .findOne({
      _id: shortLink,
    }, (findLinkErr, findLinkRes) => {
      if (findLinkErr) {
        console.log("Error finding link " + shortLink, findLinkErr)
        res.status(500)
        res.send("Error getting shortlink!");
      } else {
        if (findLinkRes) {
          console.log("Found link.", findLinkRes)
          if (findLinkRes.active) {
            let planID = findLinkRes.plan
            console.log("planID:", planID, "shortLink:", shortLink)
            dbConnection
              .collection("plans")
              .findOne({
                _id: planID
              }, {
                projection: {
                  _id: 0,
                  planName: 1,
                  colorTheme: 1,
                  createdAt: 1,
                  lastModified: 1,
                  ownedBy: 1,
                  forkedFrom: 1,
                }
              }, (findPlanErr, findPlanRes) => {
                if (findPlanErr) {
                  console.log("Error finding plan.", findPlanErr)
                  res.status(500)
                  res.send("Error fetching plan data!");
                } else {
                  if (findPlanRes) {
                    console.log("Found plan.", findPlanRes)
                    res.status(200)
                    res.send(JSON.stringify(findPlanRes));
                  } else {
                    console.log(`No Error but didn't find plan ${planID}.`)
                    res.status(404)
                    res.send("Not Found")
                  }
                }
              })
          } else {
            console.log(`Link ${shortLink} found, but inactive.`)
            // Requires authentication and authorization, which isn't currently implemented.
            res.status(501)
            res.send("Not Implemented")
          }
        } else {
          console.log(`No Error, but didn't find link ${shortLink}.`)
          res.status(404)
          res.send("Not Found")
        }
      }
    });
})

// Returns only the latest state of a plan identified by a public shortlink
planRoutes.route(["/api/plandata/:shortlink"]).get(async function (req, res) {
  const dbConnection = dbo.getDb();
  let shortLink = req.params["shortlink"]
  console.log("GET for /api/plandata/" + shortLink)
  let timeToHour = (new Date()).toISOString().slice(0, 13)

  dbConnection
    .collection("links")
    .findOne({
      _id: shortLink,
    }, (findLinkErr, findLinkRes) => {
      if (findLinkErr) {
        console.log("Error finding link " + shortLink, findLinkErr)
        res.status(500)
        res.send("Error getting shortlink!");
      } else {
        if (findLinkRes) {
          console.log("Found link.", findLinkRes)
          if (findLinkRes.active) {
            let planID = findLinkRes.plan
            console.log("planID:", planID, "shortLink:", shortLink)
            dbConnection
              .collection("stats")
              .updateOne({
                _id: {
                  "plan": planID,
                  "link": shortLink,
                },
              }, {
                $inc: {
                  ["views." + timeToHour]: 1
                }
              }, {
                upsert: true
              }, (updateStatsErr, updateStatsRes) => {
                console.log("update stats res:", updateStatsRes)
                if (updateStatsErr) {
                  console.log("Error updating stats.", updateStatsErr)
                } else {
                  console.log("Updated stats.")
                }
                dbConnection
                  .collection("plans")
                  .findOne({
                    _id: planID
                  }, {
                    projection: {
                      currentState: 1,
                    }
                  }, (findPlanErr, findPlanRes) => {
                    if (findPlanErr) {
                      console.log("Error finding plan.", findPlanErr)
                      res.status(500)
                      res.send("Error fetching plan data!");
                    } else {
                      if (findPlanRes) {
                        let latestStateID = findPlanRes.currentState
                        console.log("Found plan.", findPlanRes)
                        console.log("latest state id:", latestStateID)
                        dbConnection
                          .collection("plan_states")
                          .findOne({
                            "_id": latestStateID
                          }, {
                            projection: {
                              _id: 0,
                            }
                          }, (findPlanStateErr, findPlanStateRes) => {
                            if (findPlanStateErr) {
                              console.log(`Error getting plan state ${latestStateID}`)
                              res.status(404)
                              res.send("Not Found")
                            } else {
                              if (findPlanStateRes) {
                                console.log(`Found plan state ${latestStateID}`)
                                res.status(200)
                                findPlanStateRes.shortlink = shortLink
                                res.send(JSON.stringify(findPlanStateRes));
                              } else {
                                console.log(`No error but didn't find plan state ${latestStateID}`)
                                res.status(404)
                                res.send("Not Found")
                              }
                            }
                          })
                      } else {
                        console.log(`No Error but didn't find plan ${planID}.`)
                        res.status(404)
                        res.send("Not Found")
                      }
                    }
                  })
              })
          } else {
            // won't return this in the public api, even if user is authorized
            console.log(`Link ${shortLink} found, but inactive.`)
            res.status(404)
            res.send("Not Found")
          }
        } else {
          console.log(`No Error, but didn't find link ${shortLink}.`)
          res.status(404)
          res.send("Not Found")
        }
      }
    });
});

module.exports = planRoutes;
