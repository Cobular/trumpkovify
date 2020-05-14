import confetti from "canvas-confetti";
import $ from "jquery";
import { JakeIsBabyRage, JakeIsGainingCompetence } from "./types";

const answeredEvent = new CustomEvent("answeredEvent")

function buttonCallback(data: JakeIsBabyRage): void {
    if (data.status === "correct") {
        confetti(data.confetti);
        dispatchEvent(answeredEvent);
    }
}

function createMoarButtonsPlease(numberPlease: number) {
    const domButton = `a#button${numberPlease}`;
    const domText = `#text_${numberPlease}`;
    const jakesButtonBoy = `Button${numberPlease}`;

    $(domButton).bind("click", () => {
        const text = $(domText).text();
        const data: JakeIsGainingCompetence = {
            button: jakesButtonBoy,
            textHash: text.toLowerCase().trim(),
        };
        $.getJSON("/answerValidation", data, (d: JakeIsBabyRage) => {
            buttonCallback(d);
        })
    })
}

createMoarButtonsPlease(1);
createMoarButtonsPlease(2);
