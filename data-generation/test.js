import { readFile, writeFile } from "fs/promises";

const trainingDataStr = await readFile("./out/training_data/sample-2022-2023.json", {
  encoding: "utf-8",
});

const trainingData = JSON.parse(trainingDataStr);
const outcomes = new Map([[1,0],[2,0],[0,0]])
trainingData.forEach(({matchOutcome}) => {
  const freq = outcomes.get(matchOutcome)
  outcomes.set(matchOutcome, freq + 1)
})

console.log(outcomes.entries())
