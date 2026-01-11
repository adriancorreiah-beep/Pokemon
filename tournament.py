from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from battle_ai import MaxDamageAI


@dataclass(frozen=True)
class TeamEntry:
    name: str
    team: str


def load_team(path: Path) -> TeamEntry:
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"Team file {path} is empty.")
    return TeamEntry(name=path.stem, team=content)


async def run_round_robin(
    teams: List[TeamEntry], battle_format: str, battles_per_match: int
) -> Dict[str, Dict[str, int]]:
    results: Dict[str, Dict[str, int]] = {
        entry.name: {"wins": 0, "losses": 0, "draws": 0} for entry in teams
    }

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            team_a = teams[i]
            team_b = teams[j]

            player_a = MaxDamageAI(
                team=team_a.team,
                battle_format=battle_format,
                max_concurrent_battles=1,
                save_replays=False,
            )
            player_b = MaxDamageAI(
                team=team_b.team,
                battle_format=battle_format,
                max_concurrent_battles=1,
                save_replays=False,
            )

            start_a = player_a.n_won_battles
            start_b = player_b.n_won_battles

            await player_a.battle_against(player_b, n_battles=battles_per_match)

            wins_a = player_a.n_won_battles - start_a
            wins_b = player_b.n_won_battles - start_b
            draws = battles_per_match - wins_a - wins_b

            results[team_a.name]["wins"] += wins_a
            results[team_a.name]["losses"] += wins_b
            results[team_a.name]["draws"] += draws

            results[team_b.name]["wins"] += wins_b
            results[team_b.name]["losses"] += wins_a
            results[team_b.name]["draws"] += draws

            print(
                f"{team_a.name} vs {team_b.name}: "
                f"{wins_a}-{wins_b} ({draws} draws)"
            )

    return results


def print_standings(results: Dict[str, Dict[str, int]]) -> None:
    print("\nFinal Standings")
    print("===============")
    sorted_results = sorted(
        results.items(),
        key=lambda item: (item[1]["wins"], -item[1]["losses"]),
        reverse=True,
    )
    for name, record in sorted_results:
        print(
            f"{name}: {record['wins']}W/"
            f"{record['losses']}L/"
            f"{record['draws']}D"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a Showdown round robin tournament between PokePaste teams."
    )
    parser.add_argument(
        "--format",
        default="gen9ou",
        help="Showdown format (e.g. gen9ou, gen9randombattle).",
    )
    parser.add_argument(
        "--team-file",
        action="append",
        type=Path,
        required=True,
        help="Path to a team file in PokePaste format. Repeat for multiple teams.",
    )
    parser.add_argument(
        "--battles",
        type=int,
        default=1,
        help="Number of battles per matchup (default: 1).",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    teams = [load_team(path) for path in args.team_file]

    if len(teams) < 2:
        raise ValueError("Provide at least two team files for a round robin.")

    results = await run_round_robin(teams, args.format, args.battles)
    print_standings(results)


if __name__ == "__main__":
    asyncio.run(main())
