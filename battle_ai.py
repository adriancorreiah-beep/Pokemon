from __future__ import annotations

from poke_env.player import Player
from poke_env.environment.battle import Battle


class MaxDamageAI(Player):
    """A lightweight AI that prioritizes higher base power moves."""

    def choose_move(self, battle: Battle):
        if battle.available_moves:
            best_move = max(
                battle.available_moves,
                key=lambda move: ((move.base_power or 0), (move.accuracy or 100)),
            )
            return self.create_order(best_move)

        if battle.available_switches:
            best_switch = max(
                battle.available_switches, key=lambda mon: mon.current_hp_fraction
            )
            return self.create_order(best_switch)

        return self.choose_random_move(battle)
