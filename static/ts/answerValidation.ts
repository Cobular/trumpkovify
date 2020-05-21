import confetti from "canvas-confetti";
import $ from "jquery";
import { JakeIsBabyRage, JakeIsGainingCompetence } from "./types";
import sha1 from "sha1"

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
            textHash: sha1(text.toLowerCase().trim()),
        };
        $.getJSON("/answerValidation", data, (d: JakeIsBabyRage) => {
            buttonCallback(d);
        })
    })
}

createMoarButtonsPlease(1);
createMoarButtonsPlease(2);
