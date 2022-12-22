// DEPRECATED, only return stats when shortlink is accessed.


const express = require("express");
const { default: mongoose } = require("mongoose");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.

const publicStatsRoutes = express.Router();

// This will help us connect to the database
const dbo = require("../db/conn");
const { Link } = require("../models/link");
const { Stats } = require("../models/stat");

// Get stats for a plan (all shortlinks included)
publicStatsRoutes.route("/api/stats/:shortlink").get(async function (req, res) {
  let shortLink = req.params["shortlink"]
  console.log(`Stats for shortlink >${shortLink}< requested.`)
  let allViews = !(req.query.allViews === undefined)

  // console.log(Link.findOne((res, req) => {console.log(null, req)}))


  let link = await Link.findById(shortLink, //(err, res) => {
    //console.log("Res::", err, res)
  )

  if (link.active) {
    let stats = await Stats.findById({
      plan: link.plan,
      link: shortLink,
    })
    if (stats)
    res.status(200).json(stats.views)
  } else {
    res.status(404).send('Not Found')
  }




  return




  await new Promise(resolve => setTimeout(resolve, 1000));

  const dbConnection = dbo.getDb();

  dbConnection
    .collection("links")
    .findOne({ _id: shortLink }, (findShortLinkErr, findShortLinkRes) => {
      if (findShortLinkErr) {
        console.log(`Error finding shortlink ${shortLink}`)
        res.status(500)
        res.send("Internal Server Error")
      } else {
        if (findShortLinkRes) {
          dbConnection
            .collection("stats")
            .findOne({
              _id: {
                "plan": findShortLinkRes.plan,
                "link": shortLink
              }
            }, (findStatsErr, findStatsRes) => {
              if (findStatsErr) {
                console.log(findStatsErr)
                res.status(500)
                res.send("Internal Server Error");
              } else {
                if (findStatsRes) {
                  console.log(`Found stats for plan ${findShortLinkRes.plan} and link ${shortLink}.`, findStatsRes)
                  res.status(200)
                  if (allViews) {
                    // res.send(JSON.stringify(Array.from(findStatsRes.views).slice(- (process.env.MAX_VIEWS || 100))));
                    res.send(JSON.stringify(findStatsRes.views));
                  } else {
                    // return all views
                    res.send(JSON.stringify({
                      totalViewCount: Object.values(findStatsRes.views).reduce((a, b) => a + b, 0)
                    }));
                  }
                } else {
                  console.log(findStatsRes)
                  res.status(404)
                  res.send("Not Found");
                }
              }
            });
        } else {
          console.log(`No error occurred, nut nothing was found for shortlink ${shortLink}`)
          res.status(404)
          res.send("Not Found")
        }
      }
    })
});

module.exports = publicStatsRoutes;
