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

        self.TRACK_NAMES = self.__load_track_names()

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

    def resolve_racer_positions_line(self, racer):
        positions = []
        for race in self.races:
            if racer not in race.get_racer_names():
                positions.append(str())
                continue

            car_bonus = self.rva_system.get_car_bonus(race.get_racer_car(racer))

            # Car was invalid for whatever reason, so we prepend "'" to the position
            if car_bonus is None:
                positions.append(f"'{str(race.get_racer_position(racer))}'")
                continue

            positions.append(str(race.get_racer_position(racer)))

        return positions

    def resolve_racer_cars_line(self, racer):
        cars = []
        last_car_used = None
        for race in self.races:
            # The category is Random, therefore we ignore cars for results
            if self.rva_system.category_class_number == 6:
                cars.append(str())
                continue

            # Player didn't play this race, so we ignore
            if racer not in race.get_racer_names():
                cars.append(str())
                continue

            car_used = race.get_racer_car(racer)

            # Player hasn't changed cars, so we skip
            if car_used == last_car_used:
                cars.append(str())
                continue

            # If the car is a clockwork trim 'Clockwork' from its name and leave the rest,
            # except if it's just 'Clockwork'. This only has aesthetic purposes.
            if not car_used == "Clockwork" and car_used.startswith("Clockwork"):
                cars.append(car_used.split(" ", 1)[1])
            else:
                cars.append(car_used)

            last_car_used = car_used

        # We append a blank space at the end of the line
        cars.append(" ")
        return cars

    def get_rva_singles_results_arr(self):
        rva_results = [["Pos", "Racer"] + self.get_track_short_names_arr() + ["PP", "PA", "CC", "MP", "PO"]]

        pos = 1
        racer_result_entries = self.get_racer_result_entries()
        for result_entry in racer_result_entries:
            racer_name = result_entry.name
            racer_positions_line = [str(pos), racer_name]
            racer_positions_line += self.resolve_racer_positions_line(racer_name)
            racer_positions_line.append(str(result_entry.average_position).replace(".", CONFIG["decimal_number_separator"]))
            racer_positions_line.append(str(result_entry.obtained_points).replace(".", CONFIG["decimal_number_separator"]))
            racer_positions_line.append(result_entry.race_count)
            racer_positions_line.append(str(result_entry.participation_multiplier).replace(".", CONFIG["decimal_number_separator"]))
            racer_positions_line.append(str(result_entry.official_score).replace(".", CONFIG["decimal_number_separator"]))

            racer_cars_line = [str(), str()]
            racer_cars_line += self.resolve_racer_cars_line(racer_name)

            rva_results.append(racer_positions_line)
            rva_results.append(racer_cars_line)

            pos += 1

        return rva_results

    def get_rva_teams_results_arr(self):
        rva_results = [["Pos", "Racer", "Team"] + self.get_track_short_names_arr() + ["CC", "PA"]]

        pos = 1
        for result_entry in self.get_racer_result_entries():
            racer_name = result_entry.name

            try:
                racer_positions_line = [str(pos), racer_name.split(" ", 1)[1], result_entry.team]
            except IndexError:
                raise InvalidRacerTeam(racer_name)

            racer_positions_line += self.resolve_racer_positions_line(racer_name)
            racer_positions_line.append(result_entry.race_count)
            racer_positions_line.append(str(result_entry.obtained_points).replace(".", CONFIG["decimal_number_separator"]))

            racer_cars_line = [str(), str(), str()]
            racer_cars_line += self.resolve_racer_cars_line(racer_name)

            rva_results.append(racer_positions_line)
            rva_results.append(racer_cars_line)

            pos += 1

        return rva_results

    def get_racer_entries_of(self, racer_name):
        entries = []
        for race in self.races:
            for racer_entry in race.racers:
                if racer_entry.name == racer_name:
                    entries.append(racer_entry)

        return entries

    def get_track_short_names_arr(self):
        tracks = []
        for race in self.races:
            track_short_name = str()
            try:
                track_short_name = self.__get_track_short_name(race.track)
            except TrackShortNameNotFound:
                pass

            tracks.append(track_short_name)

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

        for race in self.races:
            for racer_entry in race.racers:
                if racer_entry.name == racer_name:
                    obtained_points = obtained_points + self.rva_system.get_racer_score(racer_entry, race)

        return round(obtained_points, 0)

    def get_official_score_of(self, racer_name):
        official_score = self.get_obtained_points(racer_name) / self.get_average_position_of(racer_name)
        official_score = official_score * self.get_participation_multiplier(racer_name)
        official_score = official_score * self.rva_system.NORMALIZER_CONSTANT
        return round(official_score, 2)

    def get_race_count_of(self, racer_name):
        races_played = self.get_tracks_played_by(racer_name)
        return len(races_played)

    def __get_track_short_name(self, track_name):
        actual_name = track_name.encode('cp1252').decode('utf8')  # Blame the '•' in Museum 3
        for track_key in self.TRACK_NAMES:
            if actual_name in [track_key, f"{track_key} R", f"{track_key} M", f"{track_key} RM"]:
                return self.TRACK_NAMES[track_key]

        raise TrackShortNameNotFound(actual_name)

    @staticmethod
    def __load_track_names():
        with open(os.path.join(os.getcwd(), "data", "track_names.yaml")) as fh:
            return yaml.load(fh, Loader=yaml.FullLoader)


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
        rva_system = RVASystem()

        return Session(self.SESSION_INFO[1][2],  # Host
                       self.SESSION_INFO[0][1],  # RVGL Version
                       self.SESSION_INFO[0][2],  # Protocol (i.e: p2p)
                       self.SESSION_INFO[1][1].split(" ")[1],  # Date
                       self.SESSION_INFO[1][1].split(" ")[0],  # Time
                       self.SESSION_INFO[1][3],  # Physics (Simulation, Arcade, Console or Junior RC)
                       races,  # List containing all races played in this session
                       rva_system,  # An RVA system instance, in order to calculate stuff for us
                       self.teams  # Whether this was an RVA teams session or not
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

    " Search for duplicate session lines and remove them, as for RVA results we ignore lap counts. "
    @staticmethod
    def __sanitize(log):
        i = len(log) - 1
        read_host = False
        while i > 2:
            if log[i][0] == "Session" and not read_host:
                read_host = True
            elif log[i][0] == "Session":
                log.remove(log[i])
            else:
                i = i - 1
