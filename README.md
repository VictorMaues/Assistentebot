# 🕵️‍♂️ CamufladoBot - Automação de Registro de Ponto

O **CamufladoBot** é um robô de automação desenvolvido em Python para automatizar o registro de frequência no portal **Mentorh** (Defensoria Pública do Estado do Pará) integrado ao Telegram.

O robô utiliza o **Playwright** em modo *headless* (navegador invisível) para realizar o login, acessar a área de ponto eletrônico, efetuar a batida de entrada/saída, confirmar a caixa de diálogo do sistema e enviar o comprovante em foto diretamente no chat do Telegram.

---

## 📌 Funcionalidades

- 🟢 **Batida de Entrada:** Efetua o registro de entrada e retorna a imagem de comprovante.
- 🔴 **Batida de Saída:** Efetua o registro de saída e retorna a imagem de comprovante.
- 🧪 **Modo Teste:** Simula o login e navegação no portal até a tela de ponto sem registrar o ponto real.
- 🔐 **Segurança:** Credenciais e tokens armazenados em variáveis de ambiente (`.env`).
- 🧹 **Limpeza Automática:** Remove comprovantes locais após envio no Telegram para economizar espaço.

---

## 🚀 Como Iniciar o Bot no Terminal

### 1. Ativar o Ambiente Virtual e Rodar

Abra o terminal na pasta do projeto `/home/victor/Documentos/Assistentebot` e execute:

```bash
# Ativa o ambiente virtual
source venv/bin/activate

# Executa o bot
python bot.py
```

*Ou execute diretamente pelo interpretador do ambiente virtual:*

```bash
./venv/bin/python bot.py
```

---

### 🌙 Rodar em Segundo Plano no Linux (Sem fechar o bot ao fechar o terminal)

Para manter o bot funcionando mesmo após fechar a janela do terminal:

```bash
nohup ./venv/bin/python bot.py > bot.log 2>&1 &
```

Para verificar se o bot está rodando em segundo plano:
```bash
ps aux | grep bot.py
```

Para parar a execução do bot em segundo plano:
```bash
pkill -f bot.py
```

---

## 💬 Comandos do Bot no Telegram

Envie qualquer um destes comandos na conversa com o bot no Telegram:

| Comando | Descrição |
| :--- | :--- |
| **`/start`** | Exibe a mensagem de boas-vindas e a lista de comandos disponíveis. |
| **`/entrada`** | Acessa o portal, registra o ponto de **ENTRADA**, confirma o diálogo e envia a foto comprovante. |
| **`/saida`** | Acessa o portal, registra o ponto de **SAÍDA**, confirma o diálogo e envia a foto comprovante. |
| **`/teste`** | Executa o teste de login e navegação até a tela de ponto sem efetuar a batida. |

---

## ⚙️ Configuração das Variáveis de Ambiente (`.env`)

Crie ou edite o arquivo `.env` na raiz do projeto com as suas credenciais:

```env
TELEGRAM_TOKEN=SEU_TOKEN_DO_TELEGRAM
MEU_LOGIN=SEU_CPF_OU_MATRICULA
MINHA_SENHA=SUA_SENHA_DO_PORTAL
URL_PORTAL=https://mentorh.defensoria.pa.def.br/csp/dpepa/portal/novo/index.csp
```

---

## 🛠️ Dependências do Projeto

O projeto necessita das seguintes bibliotecas Python (já instaladas no `venv`):
- `python-telegram-bot`
- `playwright`
- `python-dotenv`

Para reinstalar o Playwright caso necessário:
```bash
playwright install chromium
```

---

## 📂 Estrutura de Arquivos

```text
Assistentebot/
│── bot.py           # Código principal do robô
│── .env             # Credenciais privadas (não versionar no Git)
│── .gitignore       # Arquivos ignorados pelo Git
│── README.md        # Documentação do projeto
└── venv/            # Ambiente virtual Python
```
