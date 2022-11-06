const { response } = require("express");
const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const publicUsersRoutes = express.Router();

// This will help us connect to the database
const dbo = require("../db/conn");

// Returns list of users matching criteria, may be paginated in future versions
// Query String Parameters:
//  ?search={search text} 
publicUsersRoutes.get("/api/users", async (res, req) => {

})

// Returns single user profile, iff profile is set to be publicly visible
publicUsersRoutes.get("/api/users/:username", async (res, req) => {

})

module.exports = publicUsersRoutes;


// Get stats for a plan (all shortlinks included)
publicUsersRoutes.route("/api/user/:userid").get(async function (req, res) {
    let userID = req.params["userid"]
    console.log(`Stats for shortlink >${userID}< requested.`)

    const dbConnection = dbo.getDb();

    dbConnection
        .collection("users")
        .findOne({
            _id: userID
        }, {
            projection: {
                _id: 1,
                username: 0,
            }
        }, (findUserErr, findUserRes) => {
            if (findUserErr) {
                console.log(`Error finding shortlink ${shortLink}`)
                res.status(500)
                res.send("Internal Server Error")
            } else {
                if (findUserRes) {
                    if (findUserRes.public) {
                        res.status(200)
                        res.send(JSON.stringify(findUserRes))
                    } else {
                        res.status(404)
                        res.send("Not Found")
                    }
                } else {
                    console.log(`No error occurred, nut nothing was found for shortlink ${shortLink}`)
                    res.status(404)
                    res.send("Not Found")
                }
            }
        })
});

