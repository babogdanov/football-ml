import { readFile, writeFile } from "fs/promises";

const trainingDataStr = await readFile("./out/training_data/sample-2022-2023.json", {
  encoding: "utf-8",
});

const trainingData = JSON.parse(trainingDataStr);
console.log(trainingData)
const teamMap = new Map();

trainingData.forEach((match) => {
  const relevantKeys = Object.keys(match).filter((key) =>
    key.startsWith("team_one")
  );
  const fieldsArr = relevantKeys.map((key) => {
    const i = key.lastIndexOf("_");
    const trimmedKey = key.slice(i + 1);
    return {
      [trimmedKey]: match[key],
    };
  });

  const teamStats = Object.assign({}, ...fieldsArr);
  teamMap.set(teamStats.id, teamStats);
});

const teamStats = Array.from(teamMap.values());
await writeFile('./out/training_data/teams-2022-2023.json', JSON.stringify(teamStats));
