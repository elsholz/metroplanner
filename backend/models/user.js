const mongoose = require("mongoose");

// Define a schema
const Schema = mongoose.Schema;
const validator = require('validator')

const User = new Schema({
    username: String,
    public: Boolean,
    displayName: {
        type: String,
        validate: /^.{3,16}$/
    },
    mailto: {
        type: String,
        validate: [ validator.isEmail, 'invalid email' ]
    },
    profilePicture: String,
    profileViews: Number,
    likesGiven: {
        type: Schema.Types.Array,
        items: {
            type: Schema.Types.ObjectId
        }
    },
});

module.exports = {
    User: mongoose.model('user', User)
}
