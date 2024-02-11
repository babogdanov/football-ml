import { readFile, writeFile } from "fs/promises";
import { exit } from "process";
// 1. get standings for all relevant teams
// 2. get all matches between relevant teams
// 3. one row of data should contain details of a match, as well as the standings stats for one team

const BASE_PATH = "https://api.sportmonks.com/v3/football";
const LEAGUE_ID = 501;
// 2023/4, 2022/3, 2021/2
const SEASONS_IDS = [21787, 19735, 18369];
const CURR_SEASON_ID = 19735;
const PREV_SEASON_IDS = [17141, 18369];

const CLEAN_SHEET_ID = 194,
  GOALS_CONCEDED_ID = 88,
  GOALS_ID = 52,
  POSSESSION_ID = 45,
  YELLOW_CARDS_ID = 84,
  RED_CARDS_ID = 83;

const generateDiffStats = (
  statsOne,
  statsTwo,
  fieldsToSkip = ["id", "name"]
) => {
  const keySet = new Set(
    Object.keys(statsOne).filter(
      (key) => statsTwo[key] && !fieldsToSkip.includes(key)
    )
  );

  const res = Object.assign(
    {},
    ...Array.from(keySet.values()).map((key) => ({
      [key]: statsOne[key] - statsTwo[key],
    }))
  );

  fieldsToSkip.forEach((key) => {
    res[`team_one_${key}`] = statsOne[key];
    res[`team_two_${key}`] = statsTwo[key];
  });
  
  return res;
};

const fetchData = async (path) => {
  const resJson = await fetch(`${BASE_PATH}/${path}`, {
    headers: {
      Authorization:
        "uKnWNffDfG3SHlOSDvy4ylQ85csDDu1ghK7EY0icOMxfBBQ4ER2rFHMwS6NH",
    },
  });

  let res = await resJson.json();
  const { data } = res;

  while (res?.pagination?.has_more) {
    console.log(`fetching ${res.pagination.next_page}`);
    const nextResJson = await fetch(res.pagination.next_page, {
      headers: {
        Authorization:
          "uKnWNffDfG3SHlOSDvy4ylQ85csDDu1ghK7EY0icOMxfBBQ4ER2rFHMwS6NH",
      },
    });

    res = await nextResJson.json();
    data.push(...res.data);
  }

  return data;
};

/* const getStandings = async () => {
  await Promise.all(
    SEASONS_IDS.map(async (seasonId) => {
      const standings = await fetchData(
        //&filters=standingLeagues:271
        `standings/seasons/${seasonId}`
      );

      await writeFile(`./out/standings-${seasonId}.json`, JSON.stringify(standings));
    })
  );
}; */

const getTeamsWithStats = async () => {
  const currSeasonStandings = (await fetchData(
    `standings/seasons/${CURR_SEASON_ID}?filters=standingLeagues:${LEAGUE_ID}`
  )).filter(standing => standing.group_id);

  const prevSeasonStandings = (await fetchData(
    `standings/seasons/${PREV_SEASON_IDS[0]}?filters=standingLeagues:${LEAGUE_ID}`
  )).filter(standing => standing.group_id);

  const teamStatsMap = new Map();
  await Promise.all(
    currSeasonStandings.map(async (standing) => {
      const data = await fetchData(
        `teams/${standing.participant_id}?include=statistics.details&filters=teamStatisticSeasons:${PREV_SEASON_IDS[0]}`
      );

      const prevSeasonStanding = prevSeasonStandings.find(prev => prev.participant_id === standing.participant_id)
      // Some teams in the current season might not have stats in the previous season
      if (!prevSeasonStanding) {
        console.log(`skipping ${standing.participant_id}`)
        return
      }
      console.log(prevSeasonStanding, standing.participant_id)
      let statistics = [];
      try {
        statistics = data.statistics[0].details;
      } catch (e) {
        console.error(e);
        console.log(data, standing.participant_id);
      }
      const cleanSheetPercentage = statistics.find(
        (stat) => stat.type_id === CLEAN_SHEET_ID
      )?.value?.all?.percentage;
      const goals = statistics.find((stat) => stat.type_id === GOALS_ID)?.value
        ?.all?.average;
      const goalsConceded = statistics.find(
        (stat) => stat.type_id === GOALS_CONCEDED_ID
      )?.value?.all?.average;
      const possession = statistics.find(
        (stat) => stat.type_id === POSSESSION_ID
      )?.value?.average;
      const yellowCards =
        statistics.find((stat) => stat.type_id === YELLOW_CARDS_ID)?.value
          ?.average ?? 0;
      const redCards =
        statistics.find((stat) => stat.type_id === RED_CARDS_ID)?.value
          ?.average ?? 0;

      const features = {
        id: standing.participant_id,
        name: data.name,
        rank: prevSeasonStanding.position,
        points: prevSeasonStanding.points,
        cleanSheetPercentage,
        goals,
        goalsConceded,
        possession,
        yellowCards,
        redCards,
      };

      teamStatsMap.set(standing.participant_id, features);
    })
  );

  return teamStatsMap;
};

const getFixtures = async () => {
  const teamStatsMap = await getTeamsWithStats();

  const fixtures = await fetchData(
    `fixtures?include=scores&filters=fixtureLeagues:${LEAGUE_ID};fixtureSeasons:${CURR_SEASON_ID}`
  );

  const trainingData = fixtures
    .map((fixture) => {
      const score = fixture.scores.filter(
        (score) => score.description === "CURRENT"
      );
      if (!score || score.length === 0) {
        return null;
      }
      const [teamOneData, teamTwoData] = score;
      const teamOneStats = teamStatsMap.get(teamOneData.participant_id);
      const teamTwoStats = teamStatsMap.get(teamTwoData.participant_id);

      // Some stats from the previous season might be missing
      if (!teamOneStats || !teamTwoStats) {
        return undefined;
      }
      
      let matchOutcome;
      if (teamOneData.score.goals > teamTwoData.score.goals) {
        matchOutcome = 2;
      } else if (teamOneData.score.goals < teamTwoData.score.goals) {
        matchOutcome = 0;
      } else {
        matchOutcome = 1;
      }

      return {
        ...generateDiffStats(teamOneStats, teamTwoStats),
        matchOutcome,
      };
    })
    .filter((data) => !!data);

  await writeFile(
    "./out/training_data/diff-2022-2023.json",
    JSON.stringify(trainingData)
  );
  return trainingData;
};

const fixtures = await getFixtures();
console.log(fixtures);
