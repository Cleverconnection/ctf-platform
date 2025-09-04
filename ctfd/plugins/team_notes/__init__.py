from flask import Blueprint, render_template, request, redirect
from datetime import datetime

from CTFd.plugins import register_plugin_assets_directory
from CTFd.utils.decorators import authed_only, require_team, admins_only
from CTFd.utils.user import get_current_team, get_current_user
from CTFd.models import db, Teams


class TeamNoteLog(db.Model):
    __tablename__ = "team_notes_log"
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


def load(app):
    register_plugin_assets_directory(app, base_path="/plugins/team_notes/assets")

    team_notes_bp = Blueprint('team_notes', __name__,
                              template_folder='templates',
                              static_folder='assets')

    @team_notes_bp.route('/team_notes', methods=['GET', 'POST'])
    @authed_only
    @require_team
    def team_notes():
        team = get_current_team()
        content = team.team_notes or ""

        if request.method == 'POST':
            new_content = request.form.get('content', '')
            team.team_notes = new_content

            user = get_current_user()
            log_entry = TeamNoteLog(
                team_id=team.id,
                user_id=user.id,
                username=user.name,
                content=new_content
            )

            db.session.add(log_entry)
            db.session.commit()
            return redirect('/team_notes')

        return render_template('team_notes.html', content=content)

    @team_notes_bp.route('/admin_team_notes_clear', methods=['POST'])
    @admins_only
    def admin_team_notes_clear():
        # Limpa as anotações das equipes
        Teams.query.update({Teams.team_notes: None})
        # Limpa o histórico de logs
        TeamNoteLog.query.delete()
        db.session.commit()
        return redirect('/admin_team_notes_log')




    @team_notes_bp.route('/admin_team_notes', methods=['GET'])
    @admins_only
    def admin_team_notes():
        teams = Teams.query.order_by(Teams.name).all()
        return render_template('admin_team_notes.html', teams=teams)

    @team_notes_bp.route('/admin_team_notes_log', methods=['GET'])
    @admins_only
    def admin_team_notes_log():
        logs = TeamNoteLog.query.order_by(TeamNoteLog.timestamp.desc()).all()
        return render_template('admin_team_notes_log.html', logs=logs)

    app.register_blueprint(team_notes_bp)

