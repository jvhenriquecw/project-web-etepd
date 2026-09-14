from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, abort

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_qualquer_aqui'

# Dados em memória
sugestoes = []
proximo_id = 1
SENHA_ADMIN = 'admin123'

# Disponibiliza a variável is_admin em todos os arquivos HTML
@app.context_processor
def injetar_admin():
    return dict(is_admin=session.get('is_admin', False))

# Decorador para proteger rotas do Admin
def login_admin_necessario(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('modo_adm'))
        return f(*args, **kwargs)
    return decorada

# 1. Listar todas as sugestões (Página inicial)
@app.route('/')
def listar_sugestoes():
    return render_template('index.html', sugestoes=sugestoes)

# 2. Nova sugestão (Aluno)
@app.route('/nova', methods=['GET', 'POST'])
def nova_sugestao():
    global proximo_id
    if request.method == 'POST':
        nova = {
            'id': proximo_id,
            'titulo': request.form.get('titulo'),
            'categoria': request.form.get('categoria'),
            'descricao': request.form.get('descricao'),
            'situacao': 'Pendente',
            'resposta': None,
            'data_criacao': datetime.now().strftime('%d/%m/%Y %H:%M')
        }
        sugestoes.append(nova)
        proximo_id += 1
        return redirect(url_for('listar_sugestoes'))
    return render_template('nova.html')

# 3. Ver detalhes da sugestão
@app.route('/sugestao/<int:id_sugestao>')
def detalhes_sugestao(id_sugestao):
    sugestao = next((s for s in sugestoes if s['id'] == id_sugestao), None)
    if not sugestao:
        abort(404)
    return render_template('detalhes.html', sugestao=sugestao)

# 4. Editar sugestão (Aluno)
@app.route('/sugestao/<int:id_sugestao>/editar', methods=['GET', 'POST'])
def editar_sugestao(id_sugestao):
    sugestao = next((s for s in sugestoes if s['id'] == id_sugestao), None)
    if not sugestao:
        abort(404)

    if request.method == 'POST':
        sugestao['titulo'] = request.form.get('titulo')
        sugestao['categoria'] = request.form.get('categoria')
        sugestao['descricao'] = request.form.get('descricao')
        return redirect(url_for('detalhes_sugestao', id_sugestao=sugestao['id']))

    return render_template('editar.html', sugestao=sugestao)

# 5. Excluir sugestão
@app.route('/sugestao/<int:id_sugestao>/excluir', methods=['POST'])
def excluir_sugestao(id_sugestao):
    global sugestoes
    sugestoes = [s for s in sugestoes if s['id'] != id_sugestao]
    return redirect(url_for('listar_sugestoes'))

# 6. Painel/Login do Modo ADM
@app.route('/modo-adm', methods=['GET', 'POST'])
def modo_adm():
    erro = None
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == SENHA_ADMIN:
            session['is_admin'] = True
            return redirect(url_for('modo_adm'))
        erro = 'Senha incorreta.'

    if session.get('is_admin'):
        return render_template('adm_dashboard.html', sugestoes=sugestoes)

    return render_template('login.html', erro=erro)

# 7. Logout do Modo ADM
@app.route('/modo-adm/logout')
def logout_admin():
    session.pop('is_admin', None)
    return redirect(url_for('listar_sugestoes'))

# 8. Responder sugestão (Exclusivo ADM)
@app.route('/modo-adm/sugestao/<int:id_sugestao>/responder', methods=['GET', 'POST'])
@login_admin_necessario
def responder_sugestao(id_sugestao):
    sugestao = next((s for s in sugestoes if s['id'] == id_sugestao), None)
    if not sugestao:
        abort(404)

    if request.method == 'POST':
        sugestao['situacao'] = request.form.get('situacao')
        sugestao['resposta'] = request.form.get('resposta')
        return redirect(url_for('modo_adm'))

    return render_template('responder.html', sugestao=sugestao)

if __name__ == '__main__':
    app.run(debug=True)