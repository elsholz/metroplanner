const express = require("express")
const { ColorTheme } = require("../models/colortheme")
const { mongoose } = require("mongoose")
const { HTTP403, HTTP404 } = require("../utils")

const colorThemeRoutes = express.Router()

colorThemeRoutes.route("/api/theme/:colorThemeID").get(async function (req, res) {
  const colorThemeID = new mongoose.Types.ObjectId(req.params.colorThemeID)

  const theme = await ColorTheme.findById({ _id: colorThemeID })

  if (theme) {
    if (theme.public) {
      res.status(200).json(theme)
    } else HTTP403(res)
  } else HTTP404(res)

});

module.exports = colorThemeRoutes
