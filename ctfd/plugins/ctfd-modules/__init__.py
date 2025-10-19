import os
from flask import request, redirect, url_for
from sqlalchemy import Column, String

from CTFd.models import Challenges, db
from CTFd.plugins import register_plugin_assets_directory
from CTFd.plugins.migrations import upgrade

from .blueprint import load_bp
from .patches.admin import (
    patch_admin_challenges_listing,
    patch_create_new_challenge,
    patch_update_challenge
)
from .patches.navbar import patch_navbar


def load(app):
    """Carrega o plugin CTFd Modules e cria a coluna 'module' automaticamente."""

    print("<<<<< CTFd Modules Plugin: inicializando >>>>>", flush=True)

    # 🔧 Garante que a coluna 'module' exista na tabela challenges
    with app.app_context():
        try:
            connection = db.engine.raw_connection()
            cursor = connection.cursor()
            cursor.execute("SHOW COLUMNS FROM challenges LIKE 'module';")
            exists = cursor.fetchone()
            if not exists:
                print("🔧 Adicionando coluna 'module' à tabela challenges...", flush=True)
                cursor.execute("ALTER TABLE challenges ADD COLUMN module VARCHAR(80) DEFAULT NULL;")
                connection.commit()
                print("✅ Coluna 'module' criada com sucesso.", flush=True)
            else:
                print("ℹ️  Coluna 'module' já existe. Nenhuma alteração necessária.", flush=True)
            cursor.close()
            connection.close()
        except Exception as e:
            print(f"⚠️  Erro ao verificar/criar coluna 'module': {e}", flush=True)

    # Redireciona /challenges → /modules
    @app.before_request
    def check_challenges_endpoint():
        if request.endpoint == 'challenges.listing':
            return redirect(url_for('modules.listing'))

    # Registrar diretório de assets estáticos
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_name = os.path.basename(dir_path)
    register_plugin_assets_directory(
        app,
        base_path=f"/plugins/{dir_name}/assets/",
        endpoint="module_assets",
    )

    # Atualiza modelo e migração
    if not hasattr(Challenges, 'module'):
        setattr(Challenges, 'module', Column(String(80)))
    try:
        upgrade(plugin_name="challenge_modules")
    except Exception as e:
        print(f"ℹ️  Migração Alembic ignorada: {e}", flush=True)

    # Hotfixes para interface administrativa
    patch_admin_challenges_listing(app)
    patch_create_new_challenge(app)
    patch_update_challenge(app)

    # Hotfix da navbar
    patch_navbar(app)

    # Registra o blueprint principal
    bp = load_bp()
    app.register_blueprint(bp)

    print("<<<<< CTFd Modules Plugin loaded successfully >>>>>", flush=True)
