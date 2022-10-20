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
}