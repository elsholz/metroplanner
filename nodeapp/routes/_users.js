const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const _userRoutes = express.Router();
const { checkJwt } = require("../utils")

// This will help us connect to the database
const dbo = require("../db/conn");

_userRoutes.get("/api/_user", checkJwt, (req, res) => {
  const username = req.auth.payload.sub
  const dbConnection = dbo.getDb();
  console.log(`User ${username} requested their profile information.`)
  console.log(req.auth)
  let includePlanData = !(req.query.includePlanData === undefined)
  let includeColorThemeData = !(req.query.includeColorThemeData === undefined)

  console.log("Query Params:", req.query )

  if (username) {
    dbConnection
      .collection("users")
      .findOne({
        username: username,
      }, (findUserErr, findUserRes) => {
        if (findUserErr) {
          console.log(`Error finding user ${username}`, findUserErr)
          res.status(404)
          res.send("Not Found")
        } else {
          if (findUserRes) {
            console.log(`Found user ${username}:`, findUserRes)
            let userID = findUserRes._id
            dbConnection
              .collection("plans")
              .find({
                ownedBy: userID,
              }, {
                projection: includePlanData ? {} : {
                  _id: 1,
                }
              }, async (findUserPlansErr, findUserPlansRes) => {
                if (findUserPlansErr) {
                  console.log(`Error finding plans for user ${username}`, findUserPlansErr)
                  res.status(404)
                  res.send("Not Found")
                } else {
                  if (findUserPlansRes) {
                    let plans = await findUserPlansRes.toArray()
                    console.log(`Found plans for user ${username}:`, plans)
                    findUserRes.plans = plans
                    console.log("User plans:", findUserRes.plans)
                    dbConnection
                      .collection("plans")
                      .find({
                        ownedBy: userID,
                      }, {
                        projection: includeColorThemeData ? {planName: 1} : {
                          _id: 1
                        }
                      }, async (findUserColorThemesErr, findUserColorThemesRes) => {
                        if (findUserColorThemesErr) {
                          console.log(`Error finding color themes for user ${username}`, findUserColorThemesErr)
                          res.status(404)
                          res.send("Not Found")
                        } else {
                          if (findUserColorThemesRes) {
                            let themes = await findUserColorThemesRes.toArray()
                            console.log(`Found color themes for user ${username}:`, themes)
                            findUserRes.colorThemes = themes
                            res.status(200)
                            res.send(JSON.stringify(findUserRes))
                          } else {
                            console.log(`No error, but didn't find any color themes for user ${username}`, findUserColorThemesRes)
                            res.status(404)
                            res.send("Not Found")
                          }
                        }
                      })
                  } else {
                    console.log(`No error, but didn't find any plans for user ${username}`, findUserPlansRes)
                    res.status(404)
                    res.send("Not Found")

                  }
                }
              })
          } else {
            console.log(`No error, but didn't find user ${username}`, findUserRes)
            res.status(404)
            res.send("Not Found")
          }
        }
      })
  } else {
    res.status(400)
    res.send("Bad Request")
  }
})

module.exports = _userRoutes;
