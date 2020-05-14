import confetti from "canvas-confetti";

export type JakeIsBabyRage = {
    readonly confetti: confetti.Options;
    readonly status: "correct" | "incorrect" | "fail";
}

export type JakeIsGainingCompetence = {
    readonly button: string;
    readonly textHash: string;
}
