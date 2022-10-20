const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const _linksRoutes = express.Router();
const { checkJwt } = require("../utils")

// This will help us connect to the database
const dbo = require("../db/conn");


module.exports = _linksRoutes;
