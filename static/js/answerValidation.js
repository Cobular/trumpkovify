"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var canvas_confetti_1 = __importDefault(require("canvas-confetti"));
var jquery_1 = __importDefault(require("jquery"));
var answeredEvent = new CustomEvent("answeredEvent");
function buttonCallback(data) {
    if (data.status === "correct") {
        canvas_confetti_1.default(data.confetti);
        dispatchEvent(answeredEvent);
    }
}
function createMoarButtonsPlease(numberPlease) {
    var domButton = "a#button" + numberPlease;
    var domText = "#text_" + numberPlease;
    var jakesButtonBoy = "Button" + numberPlease;
    jquery_1.default(domButton).bind("click", function () {
        var text = jquery_1.default(domText).text();
        var data = {
            button: jakesButtonBoy,
            textHash: text.toLowerCase().trim(),
        };
        jquery_1.default.getJSON("/answerValidation", data, function (d) {
            buttonCallback(d);
        });
    });
}
createMoarButtonsPlease(1);
createMoarButtonsPlease(2);
