import asyncio
import json
import datetime as dt
from datetime import datetime
from app.events.match_processor import get_matches_for_team
from app.database import Column, PkModel, db, reference_col, relationship, DateTime

num_teams = 23
num_players_per_team = 2
num_teams_per_division = 11

class Player(PkModel):
    """A role for a user."""

    __tablename__ = "player"
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(80))
    username = Column(db.String(80))
    rating = Column(db.Integer)

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'),
        nullable=False)


    def __init__(self, **kwargs):
        """Create instance."""
        super().__init__(**kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Player({self.name})>"

class PlayerStat(PkModel):
    """A role for a user."""

    __tablename__ = "player_statistic"
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(80))
    kills = Column(db.Integer)
    placement = Column(db.Integer)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'),
        nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'),
        nullable=False)


    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(**kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<PlayerStat({self.name})>"

class Match(PkModel):
    """A role for a user."""

    __tablename__ = "match"
    id = Column(db.Integer, primary_key=True)
    external_id = Column(db.Integer)
    player_stats = relationship("PlayerStat", backref="match", lazy=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'),
        nullable=False)


    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(**kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Match({self.external_id})>"

class Team(PkModel):
    """A role for a user."""

    __tablename__ = "team"
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(80))
    players = relationship("Player", backref="team", lazy=True)
    division = Column(db.Integer)
    matches = relationship("Match", backref="team", lazy=True)
    player_stats = relationship("PlayerStat", backref="team", lazy=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'),
        nullable=False)


    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(**kwargs)

    def __repr__(self):
        return "Team {}, {} Rating".format(self.name, self.rating)

    async def refresh_stats(self, startTimestamp=None, endTimestamp=None):
        all_matches = await get_matches_for_team(self, startTimestamp=startTimestamp, endTimestamp=endTimestamp)
        for match in all_matches:
            player_stats = []
            match_data = json.dumps(match)
            match_data = json.loads(match_data)
            for stat in match_data['stats']:
                player_stat = PlayerStat(stat['player']['uno'], stat['playerStats']['kills'], stat['playerStats']['teamPlacement'])
                player_stats.append(player_stat)
            match = Match(match_data['id'], player_stats)
            self.add_match(match)
        #for stat in stats:
        #    player_kills = stat['playerStats']['kills']
        #    team_placement = stat['playerStats']['teamPlacement']
        #asyncio.get_event_loop().run_until_complete(get_team_matches(self))
        #asyncio.run(get_team_matches(self))

    def add_match(self, match):
        if self.matches is None:
            self.matches = []

        if match.external_id in [match.external_id for match in self.matches]:
            return

        self.matches.append(match)
        print("added match {}".format(match.external_id))


    @property
    def rating(self):
        rating = 0
        for match in self.matches:
            for stat in match.player_stats:
                rating += stat.kills
        return rating

class Event(PkModel):
    """A role for a user."""

    __tablename__ = "event"
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(80))
    teams = relationship("Team", backref="event", lazy=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

    @property
    def num_divisions(self):
        if len(self.teams) == 0:
            return 0
        return sorted(self.teams, key=lambda team: team.division, reverse=True)[0].division

    def seed_teams(self):
        # To return a new list, use the sorted() built-in function...
        sorted_teams = sorted(self.teams, key=lambda team: team.rating, reverse=True)
        current_division = 0
        for i, team in enumerate(sorted_teams):
            if i % num_teams_per_division == 0:
                current_division += 1
            team.division = current_division
            print("Team {} is in Division #{}".format(team.name, team.division))
        num_divisions = current_division
        print("Num Divisions: {}".format(num_divisions))

    async def refresh_stats(self):
        for team in self.teams:
            print("{} - {}".format(self.start_time, self.end_time))
            await team.refresh_stats(self.start_time, self.end_time)
            #match_stats = await get_team_matches(team)
            #for stat in stats:
            #    player_kills = stat['playerStats']['kills']
            #    team_placement = stat['playerStats']['teamPlacement']
            #team.refresh_stats()

    @property
    def leaderboard(self):
        sorted_teams = sorted(self.teams, key=lambda team: team.rating, reverse=True)
        for team in sorted_teams:
            print("{} - {} Score".format(team, team.rating))
        return sorted_teams


    def __repr__(self):
        return "{}: {} teams are registered".format(self.name, len(self.teams))
