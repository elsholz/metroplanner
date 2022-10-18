const mongoose = require("mongoose");

// Define a schema
const Schema = mongoose.Schema;

const User = new Schema({
    username: String,
    public: Boolean,
    displayName: String,
    mailto: String,
    profileViews: Number,
});

module.exports = {
    User: mongoose.model('user', User)
}
