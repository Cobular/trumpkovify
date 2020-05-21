import confetti from "canvas-confetti";
import $ from "jquery";
import sha1 from "sha1";
var answeredEvent = new CustomEvent("answeredEvent");
function buttonCallback(data) {
    if (data.status === "correct") {
        confetti(data.confetti);
        dispatchEvent(answeredEvent);
    }
}
function createMoarButtonsPlease(numberPlease) {
    var domButton = "a#button" + numberPlease;
    var domText = "#text_" + numberPlease;
    var jakesButtonBoy = "Button" + numberPlease;
    $(domButton).bind("click", function () {
        var text = $(domText).text();
        var data = {
            button: jakesButtonBoy,
            textHash: sha1(text.toLowerCase().trim()),
        };
        $.getJSON("/answerValidation", data, function (d) {
            buttonCallback(d);
        });
    });
}
createMoarButtonsPlease(1);
createMoarButtonsPlease(2);
//# sourceMappingURL=answerValidation.js.map