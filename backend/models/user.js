const mongoose = require("mongoose");

// Define a schema
const Schema = mongoose.Schema;

const User = new Schema({
    username: String,
    public: Boolean,
    displayName: String,
    mailto: String,
    profilePicture: Object,
    profileViews: Number,
    likesGiven: Array,
});

module.exports = {
    User: mongoose.model('user', User)
}
