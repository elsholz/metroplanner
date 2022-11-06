// recordRoutes is an instance of the express router.
// We use it to define our routes.
// The router will be added as a middleware and will take control of requests starting with path /listings.

// This will help us connect to the database
const dbo = require("./db/conn");
const { shortLinkAlphabet } = require("./utils")

const { Link } = require("./models/link")
const { Stats } = require("./models/stat")

async function createLink(forplan, active, fun, shortlink) {
  if (!shortlink) {
    let randomString = ''
    const length = 12
    for (let i = 0; i < length; i++) {
      randomString += shortLinkAlphabet.charAt(Math.floor(Math.random() * charactersLength));
    }
    shortlink = randomString
  } else {
    for (let i = 0; i < shortlink.length; i++) {
      if (!(shortlink.charAt(i) in shortLinkAlphabet))
        return false
    }

  }

  let link = new Link({
    _id: shortlink,
    plan: forplan,
    active: active === true
  })

  return await link.save(fun)
}


module.exports = {
  createLink: createLink
}
