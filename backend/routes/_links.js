const express = require("express");
const { Mongoose } = require("mongoose");
const { Link } = require("../models/link");
const { Plan } = require("../models/plan");
const { Stats } = require("../models/stat");
const { User } = require("../models/user");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const _linksRoutes = express.Router();
const { checkJwt, HTTP403, HTTP404, HTTP400 } = require("../utils")

_linksRoutes.get("/api/_links/:planid", checkJwt, async (req, res) => {
    // -> return all links for a plan, including stats
    let userAuthId = req.auth.payload.sub
    const planID = new Mongoose.Types.ObjectId(req.params.planid)

    if (userAuthId) {
        let user = await User.findOne({
            username: userAuthId
        })
        if (user) {
            let plan = await Plan.findById(planID)
            if (plan) {
                if (plan.ownedBy === user._id) {
                    let planShortlinks = await Link.find({
                        plan: plan._id
                    })
                    let result = []
                    if (planShortlinks) {
                        await planShortlinks.forEach(async (link) => {
                            let linkstats = await Stats.findById({
                                plan: plan._id,
                                link: link._id
                            })
                            if (linkstats) {
                                result.push({
                                    link: link,
                                    stats: linkstats
                                })
                            } else HTTP404(res)
                        })
                        // TODO: Await loop
                        res.status(200).json(result)
                    } else HTTP404(res)
                } else HTTP403(res)
            } else HTTP404(res)
        } else HTTP404(res)
    } else HTTP400(res)
})

_linksRoutes.post("/api/_links", checkJwt, async (req, res) => {
    // -> create a new shortlink for a plan
})

_linksRoutes.patch("/api/_links/:shortlink", checkJwt, async (req, res) => {
    // -> update an existing shortlink (currently only means: make it public or private)
})

module.exports = _linksRoutes;
