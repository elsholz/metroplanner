const express = require("express")
const { ColorTheme } = require("../models/colortheme")
const { mongoose } = require("mongoose")
const { HTTP403, HTTP404, HTTP500, JSON200 } = require("../utils")

const colorThemeRoutes = express.Router()

colorThemeRoutes.route("/api/theme/:colorThemeID").get(async function (req, res) {
  try{

  const colorThemeID = new mongoose.Types.ObjectId(req.params.colorThemeID)

  const theme = await ColorTheme.findById({ _id: colorThemeID })

  if (theme) {
    if (theme.public) {
      JSON200(res, theme, 0)
    } else HTTP403(res)
  } else HTTP404(res)

  } catch (error) {
    HTTP500(res)
  }
});

module.exports = colorThemeRoutes
