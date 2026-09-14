# 📢 Sistema de Sugestões dos Alunos

Aplicação web desenvolvida em **Python** com **Flask** e **Jinja2** para coleta, visualização e acompanhamento de sugestões acadêmicas e estruturais enviadas pelos alunos, com controle de acesso para a equipe de coordenação/administração.

---

## 🎯 Funcionalidades

### 🎓 Alunos / Usuários Gerais
- **Listar sugestões:** Visualizar todas as sugestões registradas com status e categoria.
- **Registrar nova sugestão:** Informar título, categoria (Infraestrutura, Pedagógico, Alimentação, Outros) e descrição detalhada.
- **Visualizar detalhes:** Ler a descrição completa, data de criação e resposta oficial (caso já respondida).
- **Editar / Excluir:** Modificar ou remover uma sugestão enviada.

### 🛡️ Painel Administrativo (`/modo-adm`)
- **Autenticação:** Acesso protegido por senha para a administração.
- **Painel dedicado:** Visão geral de todas as sugestões com foco em triagem e gestão.
- **Alterar situação:** Atualizar o status da proposta (*Pendente*, *Em Análise*, *Aprovada*, *Recusada*, *Concluída*).
- **Registrar parecer:** Escrever e publicar a resposta oficial da instituição.

---

## 📁 Estrutura do Projeto

```text
meu_projeto/
│
├── app.py                      # Lógica da aplicação Flask e rotas
├── static/
│   └── style.css               # Folha de estilos personalizada
│
├── templates/
│   ├── base.html               # Layout mestre com menu de navegação
│   ├── index.html              # Listagem pública de sugestões
│   ├── nova.html               # Formulário de envio de sugestão
│   ├── detalhes.html           # Visualização completa da sugestão
│   ├── editar.html             # Formulário de edição de conteúdo (Aluno)
│   ├── login.html              # Tela de autenticação para o Modo ADM
│   ├── responder.html          # Formulário de resposta e mudança de status (ADM)
│   └── adm_dashboard.html      # Painel de controle da administração
│
└── README.md                   # Documentação do projeto