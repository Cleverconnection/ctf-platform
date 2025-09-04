from flask import Blueprint, request, jsonify
from CTFd.models import db
from datetime import datetime

def load(app):
    feedback_bp = Blueprint(
        "feedback",
        __name__,
        template_folder="templates",
        static_folder="static",
        url_prefix="/feedback"
    )

    @feedback_bp.route("/submit", methods=["POST"])
    def submit_feedback():
        data = request.get_json()
        challenge_id = data.get("challenge_id")
        rating = data.get("rating")
        comment = data.get("comment")

        app.logger.info(
            f"[Feedback] Challenge={challenge_id}, Rating={rating}, Comment={comment}"
        )

        return jsonify({"success": True, "message": "Feedback registrado!"})

    app.register_blueprint(feedback_bp)
    app.logger.info("✅ Plugin ctfd-simple-feedback carregado com sucesso")
