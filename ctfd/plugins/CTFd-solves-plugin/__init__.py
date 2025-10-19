from flask import Blueprint, render_template

from CTFd.models import Solves
from CTFd.plugins import register_plugin_assets_directory
from CTFd.utils.challenges import get_all_challenges
from CTFd.utils.config import is_teams_mode
from CTFd.utils.decorators import admins_only
from CTFd.utils.scores import get_team_standings, get_user_standings


def _get_standings(for_team=True):
    if for_team:
        account_id_attr = "team_id"
        standings = get_team_standings(admin=True)
    else:
        account_id_attr = "user_id"
        standings = get_user_standings(admin=True)

    solves = {}
    first_bloods = {}
    first_bloods_by_challenge = {}
    for solve in Solves.query.order_by(Solves.date, Solves.id):
        account_id = getattr(solve, account_id_attr)
        challenge_id = solve.challenge_id

        solves.setdefault(account_id, {})[challenge_id] = True

        if challenge_id not in first_bloods_by_challenge:
            first_bloods_by_challenge[challenge_id] = account_id
            first_bloods.setdefault(account_id, {})[challenge_id] = True

    results = []
    for standing in standings:
        standing_dict = dict(standing)
        account_id = standing_dict.pop(account_id_attr)
        results.append({
            **standing_dict,
            "accountId": account_id,
            "solves": solves.get(account_id, {}),
            "firstBloods": first_bloods.get(account_id, {}),
        })

    return results


def load(app):
    solves_bp = Blueprint("solves", __name__, template_folder="templates")

    @solves_bp.route("/admin/solves")
    @admins_only
    def solves():
        context = {}

        context.update({"challenges": [
            c._asdict() for c in get_all_challenges(admin=True)
        ]})

        if is_teams_mode():
            context.update({"teamStandings": _get_standings(for_team=True)})
        context.update({"userStandings": _get_standings(for_team=False)})

        return render_template("solves.html", context=context)

    app.register_blueprint(solves_bp)
    register_plugin_assets_directory(app, "/plugins/solves/assets/")
