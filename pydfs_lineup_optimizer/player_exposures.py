from collections import Counter
from csv import writer


class PlayerExposures:
    def __init__(self):
        self.total_exposures = Counter({})
        self.positional_exposures = {}

    def bump_exposures(self, lineup):
        for player in lineup:
            if player in self.total_exposures:
                self.total_exposures[player] += 1
            else:
                self.total_exposures[player] = 1
            self.bump_positional_exposures(player)

    def bump_positional_exposures(self, player):
        if player.lineup_position[0:-1] in player.positions:
            # strip off the int's from lineup_position for exposure
            # purposes (ie. WR1 becomes WR)
            position = player.lineup_position[0:-1]
        else:
            position = player.lineup_position
        if position in self.positional_exposures:
            if player in self.positional_exposures[position]:
                self.positional_exposures[position][player] += 1
            else:
                self.positional_exposures[position][player] = 1
        else:
            self.positional_exposures[position] = Counter({player: 1})

    def write_exposures_csv(self, csv_filename='exposures.csv', total_lineups=None):
        with open(csv_filename, 'w+') as csv_out:
            positions = []
            for position in self.positional_exposures.keys():
                positions.append(position)
                positions.append("Own")
                positions.append("")
            header = ["Player", "Ownership", ""]
            header += positions
            ownership_writer = writer(csv_out)
            ownership_writer.writerow(header)
            count = 0
            positional_own = [self.positional_exposures[x].most_common() for x in self.positional_exposures.keys()]
            for player in self.total_exposures.most_common():
                if total_lineups is not None:
                    row = [player[0], round(player[1] / total_lineups, 5), ""]
                else:
                    row = [player[0], player[1], ""]
                for _ in positional_own:
                    if count < len(_):
                        row.append(_[count][0])
                        if total_lineups is not None:
                            row.append(round(_[count][1] / total_lineups, 5))
                        else:
                            row.append(_[count][1])
                        row.append("")
                    else:
                        row.append("")
                        row.append("")
                        row.append("")
                count += 1
                ownership_writer.writerow(row)
