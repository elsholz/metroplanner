const { auth } = require('express-oauth2-jwt-bearer');
require("dotenv").config({ path: "config.env" });

// Authorization middleware. When used, the Access Token must
// exist and be verified against the Auth0 JSON Web Key Set.
const checkJwt = auth({
  audience: 'https://ich-hab-plan.de/api/',
  issuerBaseURL: `https://dev-twa5tnu1.eu.auth0.com`,
  clientID: process.env.AUTH0_CLIENT_ID,
})

module.exports = {
  checkJwt: checkJwt,
  shortLinkAlphabet: "abcdefghjkmnpqrstuwxyzABCDEFGHJKLMNPQRSTUVWXYZ_+*123456789",
  // Bad Request
  HTTP400: function(res){
    res.status(400)
    res.send("Bad Request")
  },
  // Unauthorized
  HTTP401: function(res){
    res.status(401)
    res.send("Unauthorized")
  },
  // Forbidden
  HTTP403: function(res){
    res.status(403)
    res.send("Forbidden")
  },
  // Not Found
  HTTP404: function(res){
    res.status(404)
    res.send("Not Found")
  },
  // Method Not Allowed
  HTTP405: function(res){
    res.status(405)
    res.send("Method Not Allowed")
  },
  // Conflict
  HTTP409: function(res){
    res.status(409)
    res.send("Conflict")
  },
  // Internal Server Error 
  HTTP500: function(res){
    res.status(500)
    res.send("Internal Server Error")
  },
  // Not Implemented
  HTTP501: function(res){
    res.status(501)
    res.send("Not Implemented")
  },
}