const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const _plansRoutes = express.Router();
const { checkJwt } = require("../utils")

const { createLink } = require("../common")
const { Plan } = require("../models/plan")
const { Planstate } = require("../models/planstate")
const { Link } = require("../models/link")

// This will help us connect to the database
const dbo = require("../db/conn");
const common = require("../common");
const { default: mongoose } = require("mongoose");
const { User } = require("../models/user");

_plansRoutes.get("/api/_plans/:planid", checkJwt, (req, res) => {
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

_plansRoutes.post("/api/_plans", checkJwt, async (req, res) => {
  const userAuthId = req.auth.payload.sub

  let now = (new Date()).toISOString()

  let user = await User.findOne({
    username: userAuthId
  })
  
  // objectId
  let lines, nodes, additionalLabels = {}
  let numberOfLines, numberOfNodes = 0
  let forkedFrom = undefined// objectid
  let planName = "Neuer Plan"

  // TODO: Fork from public link
  if (req.data.forkedFrom) {
    forkedFrom = new mongoose.Types.ObjectId(req.data.forkedFrom)
    let originalPlan= await Plan.findById(forkedFrom)
    planName = "Gabelung von " + originalPlan.planName 

    let originalPlanState = await Planstate.findById(originalPlan.currentState)
    lines = originalPlanState.lines
    nodes= originalPlanState.nodes
    additionalLabels= originalPlanState.additionalLabels
    numberOfLines = originalPlanState.numberOfLines
    numberOfNodes= originalPlanState.numberOfNodes
  }

  // TODO: COlor Theme
  let colorTheme = new mongoose.Types.ObjectId("634469a8ccfb6bf5a194fcca")
  if (req.data.colorTheme) {
    console.log("Custom Color Theme supplied")
  }

  let planstate = new Planstate({
    _id: new mongoose.Types.ObjectId(),
    createdAt: now,
    nodes: nodes,
    lines: lines,
    additionalLabels: additionalLabels,
    numberOfNodes: numberOfNodes,
    numberOfLines: numberOfLines,
  })

  let plan = new Plan({
    _id: new mongoose.Types.ObjectId(),
    forkedFrom: forkedFrom,// Schema.ObjectId,
    ownedBy: user,
    planName: planName,
    colorTheme: colorTheme,
    createdAt: now,
    lastModified: now,
    currentState: planstate._id,
    history: [planstate._id],
  })

  const [_plan, _planstate, _link] = await Promise.all([
    planstate.save(async (err, res) => {

    }),
    plan.save(async (err, res) => {

    }),
    common.createLink(plan._id, false, async (err, res) => {

    }, undefined)
  ])

  res.status(201).json({
    shortlink: _link._id,
    plan: _plan,
    planState: _planstate
  })
})


module.exports = _plansRoutes;
