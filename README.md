# Pokemon Showdown Round Robin Battle AI

This project provides a simple battle AI powered by the [poke-env](https://github.com/hsahovic/poke-env) Showdown client. It loads PokePaste-formatted teams and runs a round robin tournament where every team battles every other team in your chosen Showdown format.

## Requirements

- Python 3.10+
- A network connection to access the public Pokémon Showdown server

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Prepare one or more teams in **PokePaste** format (one team per file). Then run:

```bash
python tournament.py \
  --format gen9ou \
  --team-file teams/team_a.txt \
  --team-file teams/team_b.txt \
  --team-file teams/team_c.txt
```

By default each matchup plays one battle. To increase the number of battles per matchup:

```bash
python tournament.py --format gen9ou --battles 3 --team-file teams/team_a.txt --team-file teams/team_b.txt
```

## Input format (PokePaste)

Each team file uses standard PokePaste formatting. Example:

```
Talonflame @ Flyinium Z
Ability: Gale Wings
EVs: 252 Atk / 4 Def / 252 Spe
Jolly Nature
- Brave Bird
- Flare Blitz
- Swords Dance
- Roost
```

Each Pokémon block is separated by one or more blank lines. The file can contain any number of Pokémon, typically 6.
