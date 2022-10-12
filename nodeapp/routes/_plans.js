const express = require("express");

// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.
const _planRoutes = express.Router();
const { checkJwt } = require("../utils")
const { requiredScopes } = require('express-oauth2-jwt-bearer')
const checkScopes = requiredScopes('read:messages')

// This will help us connect to the database
const dbo = require("../db/conn");

module.exports = _planRoutes;
