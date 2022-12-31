const express = require("express");
const { mongoose } = require("mongoose");
const { Plan } = require("../models/plan");
const { User } = require("../models/user");
const { HTTP403, HTTP404, HTTP400 } = require("../utils")

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const publicUsersRoutes = express.Router();

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

// publicUsersRoutes.route("/api/user/:userid").get(async function (req, res) {
//     let userID = req.params["userid"]
//     console.log(`Stats for shortlink >${userID}< requested.`)
// 
//     const dbConnection = dbo.getDb();
// 
//     dbConnection
//         .collection("users")
//         .findOne({
//             _id: userID
//         }, {
//             projection: {
//                 _id: 1,
//                 username: 0,
//             }
//         }, (findUserErr, findUserRes) => {
//             if (findUserErr) {
//                 console.log(`Error finding shortlink ${shortLink}`)
//                 res.status(500)
//                 res.send("Internal Server Error")
//             } else {
//                 if (findUserRes) {
//                     if (findUserRes.public) {
//                         res.status(200)
//                         res.send(JSON.stringify(findUserRes))
//                     } else {
//                         res.status(404)
//                         res.send("Not Found")
//                     }
//                 } else {
//                     console.log(`No error occurred, nut nothing was found for shortlink ${shortLink}`)
//                     res.status(404)
//                     res.send("Not Found")
//                 }
//             }
//         })
// });

module.exports = publicUsersRoutes;
