const express = require("express")
const { Link } = require("../models/link")
const { Plan } = require("../models/plan")
const { PlanState } = require("../models/planstate")
const { Stats } = require("../models/stat")
const { HTTP404 } = require("../utils")

const planRoutes = express.Router()

// Get List of currently popular plans shortlinks
// planRoutes.route("/api/popularplans").get(async function (req, res) {
//   const dbConnection = dbo.getDb();
//   res.status(501)
//   res.send("Not Implemented")
// })

// Returns all public information about a plan, excluding its latest state, identified by its shortlink
planRoutes.route("/api/plan/:shortlink").get(async function (req, res) {
  const shortLink = req.params["shortlink"]
  const link = await Link.findById({
    _id: shortLink
  })

  if (link && link.active) {
    let plan = await Plan.findById({
      _id: link.plan
    })

    if (plan) {
      const stats = await Stats.findById({
        plan: link.plan,
        link: shortLink,
      }, {
        totalCount: 1,
      })

      res.status(200).json({
        plan: plan,
        stats: stats
      })
    } else HTTP404(res)

  } else HTTP404(res)
})

// Returns only the latest state of a plan identified by a public shortlink
planRoutes.route(["/api/planstate/:shortlink"]).get(async function (req, res) {
  const shortLink = req.params["shortlink"]
  const timeToHour = (new Date()).toISOString().slice(0, 13)

  const link = await Link.findById({
    _id: shortLink
  })

  if (link && link.active) {
    const plan = await Plan.findById({
      _id: link.plan
    })

    if (plan) {
      const latestStateID = plan.currentState
      const planState = await PlanState.findById({
        _id: latestStateID
      })

      if (planState) {
        res.status(200).json(planState)

        await Stats.findByIdAndUpdate({
          plan: link.plan,
          link: shortLink,
        }, {
          $inc: {
            "totalCount": 1,
            ["views." + timeToHour]: 1
          },
        })
      } else HTTP404(res)
    } else HTTP404(res)
  } else HTTP404(res)
})

module.exports = planRoutes
