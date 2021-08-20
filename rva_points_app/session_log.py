import csv

from rva_points_app.rva_system.rva_system import *


class RacerResultEntry:
    def __init__(self, name, race_count, average_position, obtained_points, official_score, played_tracks, participation_multiplier, team=None):
        self.name = name
        self.race_count = race_count
        self.average_position = average_position
        self.obtained_points = obtained_points
        self.official_score = official_score
        self.played_tracks = played_tracks
        self.participation_multiplier = participation_multiplier
        self.team = team


class RacerEntry:
    def __init__(self, position, name, car, race_time, best_lap, finished, cheating, team=None):
        self.position = int(position)
        self.name = name
        self.car = car
        self.race_time = race_time
        self.best_lap = best_lap
        self.finished = finished
        self.cheating = cheating
        self.team = team


class Race:
    def __init__(self, track, racers_count, racers):
        self.track = track
        self.racers_count = racers_count
        self.racers = racers

    def get_racer_entry_by_name(self, racer_name):
        match = None
        for racer_entry in self.racers:
            if racer_entry.name == racer_name:
                match = racer_entry
        return match

    def get_racer_names(self):
        names = []
        for racer_entry in self.racers:
            names.append(racer_entry.name)
        return names

    def get_racer_position(self, racer_name):
        racer_entry = self.get_racer_entry_by_name(racer_name)
        if racer_entry is None:
            return 0
        else:
            return racer_entry.position

    def get_racer_car(self, racer_name):
        racer_entry = self.get_racer_entry_by_name(racer_name)
        if racer_entry is None:
            return 0
        else:
            return racer_entry.car


class Session:
    def __init__(self, host, rvgl_version, protocol, date, time, physics, races, rva_system, teams=False):
        self.host = host
        self.version = rvgl_version
        self.protocol = protocol
        self.date = date
        self.time = time
        self.physics = physics
        self.races = races
        self.rva_system = rva_system
        self.teams = teams

    def get_racer_result_entries(self):
        racer_result_entries = []
        for racer_name in self.get_racers():
            racer_result_entries.append(
                RacerResultEntry(racer_name,
                                 self.get_race_count_of(racer_name),
                                 self.get_average_position_of(racer_name),
                                 self.get_obtained_points(racer_name),
                                 self.get_official_score_of(racer_name),
                                 self.get_tracks_played_by(racer_name),
                                 self.get_participation_multiplier(racer_name),
                                 self.get_team_of(racer_name)
                                 )
            )

        if self.teams:  # Sort by PA
            racer_result_entries.sort(key=lambda r: r.obtained_points, reverse=True)
        else:  # Sort by PO (singles)
            racer_result_entries.sort(key=lambda r: r.official_score, reverse=True)

        return racer_result_entries

    def get_rva_results(self):
        rva_results = []
        header = ["Pos", "Racer"]
        if self.teams:
            header = header + ["Team"] + self.get_tracks() + ["CC", "PA"]
        else:
            header = header + self.get_tracks() + ["PP", "PA", "CC", "MP", "PO"]

        rva_results.append(header)

        position = 1
        racer_result_entries = self.get_racer_result_entries()
        for result_entry in racer_result_entries:
            racer_positions_line = [str(position), result_entry.name]

            if self.teams:
                racer_positions_line.append(result_entry.team)

            for race in self.races:
                if result_entry.name in race.get_racer_names():
                    car_bonus = self.rva_system.get_car_bonus(race.get_racer_car(result_entry.name))
                    racer_position = ""
                    if car_bonus is None:
                        racer_position = racer_position + "'"

                    racer_position = racer_position + str(race.get_racer_position(result_entry.name))
                    racer_positions_line.append(racer_position)
                else:
                    racer_positions_line.append(str())

            if self.teams:
                racer_positions_line.append(result_entry.race_count)
                racer_positions_line.append(str(result_entry.obtained_points).replace(".", CONFIG["decimal_number_separator"]))
            else:
                racer_positions_line.append(str(result_entry.average_position).replace(".", CONFIG["decimal_number_separator"]))
                racer_positions_line.append(str(result_entry.obtained_points).replace(".", CONFIG["decimal_number_separator"]))
                racer_positions_line.append(result_entry.race_count)
                racer_positions_line.append(str(result_entry.participation_multiplier).replace(".", CONFIG["decimal_number_separator"]))
                racer_positions_line.append(str(result_entry.official_score).replace(".", CONFIG["decimal_number_separator"]))

            rva_results.append(racer_positions_line)
            position = position + 1

            racer_cars_line = [str(), str()]
            if self.teams:
                racer_cars_line.append(str())

            last_car_used = None
            for race in self.races:
                if result_entry.name in race.get_racer_names():
                    car_used = race.get_racer_car(result_entry.name)
                    if car_used == last_car_used:
                        racer_cars_line.append(str())
                    else:
                        car = race.get_racer_car(result_entry.name)
                        if car.startswith("Clockwork"):
                            car = car.split(" ", 1)[1]

                        racer_cars_line.append(car)
                    last_car_used = car_used
                else:
                    racer_cars_line.append(str())
            racer_cars_line.append(" ")

            rva_results.append(racer_cars_line)
        return rva_results

    def get_racer_entries_of(self, racer_name):
        entries = []
        for race in self.races:
            for racer_entry in race.racers:
                if racer_entry.name == racer_name:
                    entries.append(racer_entry)

        return entries

    def get_tracks(self):
        tracks = []
        for race in self.races:
            tracks.append(race.track)
        return tracks

    def get_tracks_played_by(self, racer_name):
        played_tracks = []
        for race in self.races:
            if racer_name in race.get_racer_names():
                played_tracks.append(race.track)
        return played_tracks

    def get_racers(self):
        racers = []
        for race in self.races:
            for racer_entry in race.racers:
                if not racer_entry.name in racers:
                    racers.append(racer_entry.name)
        return racers

    def get_team_of(self, racer_name):
        racer_entries = self.get_racer_entries_of(racer_name)
        if len(racer_entries) == 0:
            return None
        else:
            return racer_entries[0].team

    " Returns the average position of a racer in this session, or 0 if the racer was not found. "
    def get_average_position_of(self, racer_name):
        race_count = self.get_race_count_of(racer_name)
        if race_count == 0:
            return 0

        racer_entries = self.get_racer_entries_of(racer_name)

        positions_sum = 0
        for racer_entry in racer_entries:
            positions_sum = positions_sum + racer_entry.position

        return round(float(positions_sum / race_count), 2)

    def get_participation_multiplier(self, racer_name):
        return round(float(self.get_race_count_of(racer_name) / len(self.races)), 2)

    def get_obtained_points(self, racer_name):
        obtained_points = 0
        for racer_entry in self.get_racer_entries_of(racer_name):
            obtained_points = obtained_points + self.rva_system.get_racer_score(racer_entry)

        return round(obtained_points, 0)

    def get_official_score_of(self, racer_name):
        official_score = self.get_obtained_points(racer_name) / self.get_average_position_of(racer_name)
        official_score = official_score * self.get_participation_multiplier(racer_name)
        official_score = official_score * self.rva_system.NORMALIZER_CONSTANT
        return round(official_score, 2)

    def get_race_count_of(self, racer_name):
        races_played = self.get_tracks_played_by(racer_name)
        return len(races_played)


class SessionLog:
    def __init__(self, csv_path, teams=False):
        self.FULL_LOG = []
        self.SESSION_INFO = []
        self.SESSION_RACES = []

        self.csv_path = csv_path
        self.teams = teams

        self.__load()

    def get_session(self):
        return self.__get_session()

    def __load(self):
        with open(self.csv_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"')

            for row in reader:
                self.FULL_LOG.append(row)
            self.__sanitize(self.FULL_LOG)

            for row in self.FULL_LOG[:2]:
                self.SESSION_INFO.append(row)

            first = True
            race = []
            racers = []
            for row in self.FULL_LOG[2:]:
                if row[0] == "#":
                    continue
                if not first and row[0] == "Results":
                    race.append(racers)
                    self.SESSION_RACES.append(race)
                    race = []
                    racers = []
                    race.append(row)
                else:
                    if row[0] == "Results":
                        race.append(row)
                    else:
                        racers.append(row)

                    first = False
            race.append(racers)
            self.SESSION_RACES.append(race)

    def __get_session(self):
        races = self.__get_races()
        rva_system = RVASystem(len(races[0].racers))

        return Session(self.SESSION_INFO[1][2],  # Host
                       self.SESSION_INFO[0][1],  # RVGL Version
                       self.SESSION_INFO[0][2],  # Protocol (i.e: p2p)
                       self.SESSION_INFO[1][1].split(" ")[1],  # Date
                       self.SESSION_INFO[1][1].split(" ")[0],  # Time
                       self.SESSION_INFO[1][3],  # Physics (Simulation, Arcade, Console or Junior RC)
                       races,  # List containing all races played in this session
                       rva_system,  # An RVA system instance, in order to calculate stuff for us
                       self.teams
                       )

    def __get_races(self):
        races = []
        for row in self.SESSION_RACES:
            track = row[0][1]
            racers_count = row[0][2]

            racers = []
            for racer_row in row[1]:
                position = racer_row[0]
                name = racer_row[1]
                car = racer_row[2]
                race_time = racer_row[3]
                best_lap = racer_row[4]
                finished = racer_row[5] == "true"
                cheating = racer_row[6] == "true"

                if self.teams:
                    team_tag = name.split(" ")[0]
                    racers.append(RacerEntry(position, name, car, race_time, best_lap, finished, cheating, team_tag))
                else:
                    racers.append(RacerEntry(position, name, car, race_time, best_lap, finished, cheating))

            races.append(Race(track, racers_count, racers))

        return races  # There's a None value at the end of the array

    " Search for duplicate session lines and remove them "
    @staticmethod
    def __sanitize(log):
        read_host = False
        for line in log:
            if line[0] == "Session" and not read_host:
                read_host = True
            elif line[0] == "Session":
                log.remove(line)
