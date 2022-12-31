const express = require("express");
const { ColorTheme } = require("../models/colortheme");
const { mongoose } = require("mongoose");
const { HTTP403, HTTP404, HTTP400 } = require("../utils")

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const colorThemeRoutes = express.Router();

colorThemeRoutes.route("/api/theme/:colorThemeID").get(async function (req, res) {
  const colorThemeID = new mongoose.Types.ObjectId(req.params.colorThemeID)

  const theme = await ColorTheme.findById({ _id: colorThemeID })

  if (theme) {
    if (theme.public) {
      res.status(200).json(theme)
    } else HTTP403(res)
  } else HTTP404(res)

  // const dbConnection = dbo.getDb();
  // // Get records
  // let themeID = new mongodb.ObjectId(req.params["colorThemeID"])

  // dbConnection
  //   .collection("colorThemes")
  //   .findOne({ "_id": themeID }, (findThemeErr, findThemeRes) => {
  //     if (findThemeErr) {
  //       console.log(`Error finding theme ${themeID}`, findThemeErr)
  //       res.status(500)
  //       res.send("Error fetching listings!");
  //     } else {
  //       if (findThemeRes) {
  //         if (findThemeRes.public) {
  //           console.log(`Found theme for id ${themeID}`)
  //           res.status(200)
  //           res.send(JSON.stringify(findThemeRes));
  //         } else {
  //           console.log(`Found theme, but it isn't public, for id ${themeID}`)
  //           res.status(404)
  //           res.send("Not Found")
  //         }
  //       } else {
  //         console.log(`No error, but didn't find theme for id ${themeID}`)
  //         res.status(404)
  //         res.send("Not Found")
  //       }
  //     }
  //   });
});

module.exports = colorThemeRoutes;
