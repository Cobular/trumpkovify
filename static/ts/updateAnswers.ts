function doUpdateOnAnswerSubmit() {
    $.getJSON("/newQuestion", (d: { text1: string, text2: string }) => {
        $("text_1").text(d.text1);
        $("text_2").text(d.text2);
    })
}

addEventListener("answeredEvent", doUpdateOnAnswerSubmit);
