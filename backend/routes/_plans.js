const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const _plansRoutes = express.Router();
const { checkJwt, HTTP404, HTTP401, HTTP403 } = require("../utils")

const { createLink } = require("../common")
const { Plan } = require("../models/plan")
const { Planstate } = require("../models/planstate")
const { Link } = require("../models/link")

// This will help us connect to the database
const dbo = require("../db/conn");
const common = require("../common");
const { default: mongoose } = require("mongoose");
const { User } = require("../models/user");

_plansRoutes.get("/api/_plans/:planid", checkJwt, async (req, res) => {
  let planID = new mongodb.ObjectId(req.params["planid"])
  const userAuthId = req.auth.payload.sub

  console.log(`User ${userAuthId} requested plan data for plan with oid ${planID}.`)
  console.log(req.auth)

  let user = await User.findOne({
    username: userAuthId
  })

  if (user && userAuthId && planID) {
    let plan = await Plan.findById(planID)
    if (plan) {
      if (plan.ownedBy === userAuthId) {
        res.status(200).json(plan, false, 4)
      } else HTTP403(res)
    } else HTTP404(res)
  } else HTTP400(res)
})

_plansRoutes.post("/api/_plans", checkJwt, async (req, res) => {
  const userAuthId = req.auth.payload.sub

  let now = (new Date()).toISOString()

  let user = await User.findOne({
    username: userAuthId
  })

  if (user) {
    let lines, nodes, additionalLabels = {}
    let numberOfLines, numberOfNodes = 0
    let forkedFrom = undefined // objectid
    let planName = "Neuer Plan"

    let forkedFromPublicShortlink = false

    if (req.data.forkedFrom) {
      isOID = req.data.forkedFrom.match(/^[0-9a-fA-F]{24}$/)
      // can be either forked from a public plan (by public shortlink)
      if (!isOID) {
        let forkedFromShortlink = await Link.findById(req.data.forkedFrom)
        if (forkedFromShortlink) {
          if (forkedFromShortlink.active) {
            forkedFromPublicShortlink = true
          }
          forkedFrom = forkedFromShortlink.plan
        } else HTTP404()
      } else {
        // or directly from a plan owned by the current user
        forkedFrom = new mongoose.Types.ObjectId(req.data.forkedFrom)
      }

      // TODO: Colortheme
      let originalPlan = await Plan.findById(forkedFrom)
      if (originalPlan) {
        if (originalPlan.ownedBy === user._id || forkedFromPublicShortlink) {
          planName = originalPlan.planName + " - Gabelung"
          let originalPlanState = await Planstate.findById(originalPlan.currentState)
          if (originalPlanState) {
            lines = originalPlanState.lines
            nodes = originalPlanState.nodes
            additionalLabels = originalPlanState.additionalLabels
            numberOfLines = originalPlanState.numberOfLines
            numberOfNodes = originalPlanState.numberOfNodes
          }
        } else HTTP403(res)
      } else HTTP404(res)
    }

    // // TODO: COlor Theme
    // // let colorTheme = new mongoose.Types.ObjectId("634469a8ccfb6bf5a194fcca")
    // if (req.data.colorTheme) {
    //   console.log("Custom Color Theme supplied")
    // }

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
      ownedBy: user._id,
      planName: planName,
      colorTheme: req.data.colorTheme || "dark",//colorTheme,
      createdAt: now,
      lastModified: now,
      currentState: planstate._id,
      history: [planstate._id],
    })

    const [_plan, _planstate, _link] = await Promise.all([
      planstate.save(async (err, res) => {
        console.log(err, res)
      }),
      plan.save(async (err, res) => {
        console.log(err, res)
      }),
      common.createLink(plan._id, false, async (err, res) => {
        console.log(err, res)
      }, undefined)
    ])

    res.status(201).json({
      shortlink: _link._id,
      plan: _plan,
      planState: _planstate
    })
  } else HTTP400(res)
})

_plansRoutes.patch("/api/_plans/:planid", checkJwt, (req, res) => {
  // patch plan 

  // if currentState has changed:
  // if new currentState doesn't exist yet: create new plan state
  // else: change only currentState attribute

})


module.exports = _plansRoutes;
