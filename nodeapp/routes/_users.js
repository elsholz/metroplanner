const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const _userRoutes = express.Router();
const { checkJwt } = require("../utils")
const { requiredScopes, claimIncludes, claimEquals } = require('express-oauth2-jwt-bearer')
const checkScopes = requiredScopes('read:messages')

// This will help us connect to the database
const dbo = require("../db/conn");

_userRoutes.get("/api/_user", checkJwt, (req, res) => {
  const username = req.auth.payload.sub
  const dbConnection = dbo.getDb();
  console.log(`User ${username} requested their profile information.`)

  if (username) {
    dbConnection
      .collection("users")
      .findOne({
        _id: username,
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
                projection: {
                  _id: 1
                }
              }, (findUserPlansErr, findUserPlansRes) => {
                if (findUserPlansErr) {
                  console.log(`Error finding plans for user ${username}`, findUserPlansErr)
                  res.status(404)
                  res.send("Not Found")
                } else {
                  if (findUserPlansRes) {
                    console.log(`Found plans for user ${username}:`, findUserPlansRes)
                    findUserRes.plans = findUserPlansRes
                    dbConnection
                      .collection("plans")
                      .find({
                        ownedBy: userID,
                      }, {
                        projection: {
                          _id: 1
                        }
                      }, (findUserColorThemesErr, findUserColorThemesRes) => {
                        if (findUserColorThemesErr) {
                          console.log(`Error finding color themes for user ${username}`, findUserColorThemesErr)
                          res.status(404)
                          res.send("Not Found")
                        } else {
                          if (findUserColorThemesRes) {
                            console.log(`Found color themes for user ${username}:`, findUserColorThemesRes)
                            findUserRes.colorThemes = findUserColorThemesRes
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
