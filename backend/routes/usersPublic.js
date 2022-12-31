const express = require("express")
const { mongoose } = require("mongoose")
const { Plan } = require("../models/plan")
const { User } = require("../models/user")
const { HTTP404 } = require("../utils")

const publicUsersRoutes = express.Router()

// // Returns list of users matching criteria, may be paginated in future versions
// // Query String Parameters:
// //  ?search={search text} 
// publicUsersRoutes.get("/api/users", async (res, req) => {
// 
// })

// Returns user profile, iff profile is set to be publicly visible
publicUsersRoutes.get("/api/users/:userid", async (req, res) => {
    console.log("req::", req.params)
    const userID = new mongoose.Types.ObjectId(req.params.userid)
    let detail = !(req.query.detail === undefined)

    let user = null;

    if (detail) {
        user = await User.findByIdAndUpdate({
            _id: userID
        }, {
            $inc: { "profileViews": 1 }
        })
    }
    else {
        user = await User.findById({ _id: userID })
    }

    let userPlans = await Plan.find({
        ownedBy: userID
    }, {
        _id: 1
    })

    if (user) {
        if (user.public && detail) {
            res.status(200).json({
                _id: user._id,
                public: user.public,
                displayName: user.displayName,
                likesGiven: user.likesGiven,
                mailto: user.mailto,
                profileViews: user.profileViews,
                profilePicture: user.profilePicture,
                userPlans: userPlans,
            })
        } else {
            res.status(200).json({
                pic: user.profilePicture,
                _id: user._id,
                public: user.public,
                displayName: user.displayName,
            })
        }
    } else HTTP404(res)
})

module.exports = publicUsersRoutes
