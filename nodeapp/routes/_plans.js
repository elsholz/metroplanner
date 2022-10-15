const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const _userRoutes = express.Router();
const { checkJwt } = require("../utils")

// This will help us connect to the database
const dbo = require("../db/conn");

_userRoutes.get("/api/_plans/:planid", checkJwt, (req, res) => {
  let planID = new mongodb.ObjectId(req.params["planid"])

  const username = req.auth.payload.sub
  const dbConnection = dbo.getDb();
  console.log(`User ${username} requested plan data for plan with oid ${planID}.`)
  console.log(req.auth)

  if (username) {
    dbConnection
      .collection("plans")
      .findOne({
        _id: planID
      }, (findPlanErr, findPlanRes) => {
        if (findPlanErr) {
          console.log(`Error finding user ${username}`, findPlanErr)
          res.status(404)
          res.send("Not Found")
        } else {
          if (findPlanRes) {
          } else {
          }
        }
      })
  } else {
    res.status(400)
    res.send("Bad Request")
  }
})

module.exports = _userRoutes;
