"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const canvas_confetti_1 = __importDefault(require("canvas-confetti"));
const jquery_1 = __importDefault(require("jquery"));
const answeredEvent = new CustomEvent("answeredEvent");
function buttonCallback(data) {
    if (data.status === "correct") {
        canvas_confetti_1.default(data.confetti);
        dispatchEvent(answeredEvent);
    }
}
function createMoarButtonsPlease(numberPlease) {
    const domButton = `a#button${numberPlease}`;
    const domText = `#text_${numberPlease}`;
    const jakesButtonBoy = `Button${numberPlease}`;
    jquery_1.default(domButton).bind("click", () => {
        const text = jquery_1.default(domText).text();
        const data = {
            button: jakesButtonBoy,
            textHash: text.toLowerCase().trim(),
        };
        jquery_1.default.getJSON("/answerValidation", data, (d) => {
            buttonCallback(d);
        });
    });
}
createMoarButtonsPlease(1);
createMoarButtonsPlease(2);
