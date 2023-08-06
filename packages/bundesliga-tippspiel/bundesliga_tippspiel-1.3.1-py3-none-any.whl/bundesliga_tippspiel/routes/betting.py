"""LICENSE
Copyright 2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of bundesliga-tippspiel.

bundesliga-tippspiel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

bundesliga-tippspiel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with bundesliga-tippspiel.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

from typing import Optional, Dict
from flask import render_template, request, Blueprint
from flask_login import login_required, current_user
from bundesliga_tippspiel.utils.routes import action_route
from bundesliga_tippspiel.db.user_generated.Bet import Bet
from bundesliga_tippspiel.actions.GetMatchAction import GetMatchAction
from bundesliga_tippspiel.actions.GetBetAction import GetBetAction
from bundesliga_tippspiel.actions.GetGoalAction import GetGoalAction
from bundesliga_tippspiel.actions.PlaceBetsAction import PlaceBetsAction


def define_blueprint(blueprint_name: str) -> Blueprint:
    """
    Defines the blueprint for this route
    :param blueprint_name: The name of the blueprint
    :return: The blueprint
    """
    blueprint = Blueprint(blueprint_name, __name__)

    @blueprint.route("/bets", methods=["POST", "GET"])
    @blueprint.route("/bets/<int:matchday>", methods=["GET"])
    @login_required
    @action_route
    def bets(matchday: Optional[int] = None):
        """
        Displays all matches for a matchday with entries for betting
        :param matchday: The matchday to display
        :return: None
        """
        if request.method == "GET":
            if matchday is None:
                matchday = -1

            matchday_bets = GetBetAction(
                matchday=matchday,
                user_id=current_user.id
            ).execute()["bets"]

            matchday_matches = GetMatchAction(
                matchday=matchday
            ).execute()["matches"]

            betmap: Dict[int, Optional[Bet]] = {}
            matchday_points = 0
            for _match in matchday_matches:
                betmap[_match.id] = None
            for bet in matchday_bets:
                betmap[bet.match.id] = bet
                matchday_points += bet.evaluate(when_finished=True)

            return render_template(
                "betting/bets.html",
                matchday=matchday_matches[0].matchday,
                betmap=betmap,
                matches=matchday_matches,
                matchday_points=matchday_points
            )

        else:  # POST
            action = PlaceBetsAction.from_site_request()
            return action.execute_with_redirects(
                "betting.bets", "Tipps erfolgreich gesetzt", "betting.bets"
            )

    @blueprint.route("/match/<int:match_id>", methods=["GET"])
    @login_required
    @action_route
    def match(match_id: int):
        """
        Displays a single match
        :param match_id: The ID of the match to display
        :return: The Response
        """
        match_info = GetMatchAction(_id=match_id).execute()["match"]
        goals_info = GetGoalAction(match_id=match_id).execute()["goals"]
        bets_info = GetBetAction(match_id=match_id).execute()["bets"]
        return render_template(
            "info/match.html",
            match=match_info,
            goals=goals_info,
            bets=bets_info
        )

    return blueprint
