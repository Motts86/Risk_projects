import itertools as iter
import numpy as np
import pandas as pd
import os

# Defines the dice of values
attack_sides_max_range = defense_sides_max_range = np.arange(4, 13)
attack_die_count_range = np.arange(1, 4)
defense_die_count_range = np.arange(1, 3)
# Initialize the list
result_list = []

# Iterates through the different scenarios
for attack_sides_max in attack_sides_max_range:
    for defense_sides_max in defense_sides_max_range:
        for attack_die_count in attack_die_count_range:
            for defense_die_count in defense_die_count_range:
                # Sets dice ranges
                attack_sides = np.arange(1, attack_sides_max+1)
                defense_sides = np.arange(1, defense_sides_max+1)

                # Generate the Cartesian products n times
                attack_possibility_set = [list(item) for item in iter.product(attack_sides, repeat=attack_die_count)]
                defense_possibility_set = [list(item) for item in iter.product(defense_sides, repeat=defense_die_count)]

                # Sort each inner list in descending order
                attack_possibility_set = [sorted(inner_list, reverse=True) for inner_list in attack_possibility_set]
                defense_possibility_set = [sorted(inner_list, reverse=True) for inner_list in defense_possibility_set]

                # Generate the Cartesian product of the Cartesian products
                cartesian_result = list(iter.product(attack_possibility_set, defense_possibility_set))

                # Initialize Variables
                cum_attacker_score, cum_defender_score, result_row = 0, 0, 0
                tie, total_victory, total_defeat, shared_losses_attacker_favored, shared_losses_defender_favored = 0, 0, 0, 0, 0

                # Iterates over tuples inside the cartesian product
                for attacker, defender in cartesian_result:
                    # Use zip_longest to iterate over pairs of values
                    attacker_set_score, defender_set_score = 0, 0
                    result_row += 1
                    for att_val, def_val in iter.zip_longest(attacker, defender, fillvalue=None):
                        # Compare att_val and def_val (replace this with your own comparison logic)
                        if att_val is not None and def_val is not None:
                            if att_val > def_val:
                                cum_attacker_score += 1
                                attacker_set_score += 1
                            else:
                                cum_defender_score += 1
                                defender_set_score += 1

                    # Increments Turn Results
                    if attacker_set_score == defender_set_score:
                        tie += 1
                    elif defender_set_score == 0:
                        total_victory += 1
                    elif attacker_set_score == 0:
                        total_defeat += 1
                    elif attacker_set_score > defender_set_score:
                        shared_losses_attacker_favored += 1
                    else:
                        shared_losses_defender_favored += 1

                result_dict = {
                    "result_set": f"{attack_die_count}d{len(attack_sides)} vs {defense_die_count}d{len(defense_sides)}",
                    "attack_sides": len(attack_sides),
                    "defense_sides": len(defense_sides),
                    "attack_die_count": attack_die_count,
                    "defense_die_count": defense_die_count,
                    "compares": result_row,
                    "cum_defender_score": cum_defender_score,
                    "cum_attacker_score": cum_attacker_score,
                    "ratio": round(cum_attacker_score / (cum_attacker_score + cum_defender_score), 2),
                    "victory": total_victory,
                    "victory_avg": round(total_victory/result_row, 2),
                    "attacker_favor": shared_losses_attacker_favored,
                    "attacker_favor_avg": round(shared_losses_attacker_favored/result_row, 2),
                    "tie": tie,
                    "ties_avg": round(tie/result_row, 2),
                    "defender_favor": shared_losses_defender_favored,
                    "defender_favor_avg": round(shared_losses_defender_favored/result_row, 2),
                    "defeat": total_defeat,
                    "defeat_avg": round(total_defeat/result_row, 2)
                }
                result_list.append(result_dict)

# Prepares DataFrame and export to .csv

df = pd.DataFrame(result_list)
script_dir = os.path.dirname(os.path.realpath(__file__))
output_file_name = "dice_odds_dictionary.csv"
output_file_path = os.path.join(script_dir, output_file_name)
df.to_csv(output_file_path, index=False)
print(f"Results exported to: {output_file_path}")