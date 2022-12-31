const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const ColorTheme = new Schema({
    themeName: String,
    public: Boolean,
    forkedFrom: Object,
    ownedBy: Object,
    themeData: Object,
});

module.exports = {
    ColorTheme: mongoose.model('color_theme', ColorTheme)
}
