# 🕵️‍♂️ CamufladoBot - Automação de Registro de Ponto

O **CamufladoBot** é um robô de automação desenvolvido em Python para automatizar o registro de frequência no portal **Mentorh** (Defensoria Pública do Estado do Pará) integrado ao Telegram.

O robô utiliza o **Playwright** em modo *headless* (navegador invisível) para realizar o login, navegar no menu do portal, efetuar a batida de entrada/saída, confirmar a caixa de diálogo do sistema e enviar o comprovante em foto diretamente no chat do Telegram.

---

## 📌 Funcionalidades

- 🟢 **Batida de Entrada:** Acessa o portal, clica em bater ponto, confirma o diálogo e envia a foto comprovante.
- 🔴 **Batida de Saída:** Acessa o portal, clica em bater ponto, confirma o diálogo e envia a foto comprovante.
- 🧪 **Modo Teste:** Simula o login e a navegação até a tela de registro de ponto sem realizar a batida real.
- ❓ **Boas-Vindas:** Mensagem explicativa com todos os comandos disponíveis ao enviar `/start`.
- 🔐 **Segurança:** Credenciais e tokens protegidos em variáveis de ambiente (`.env`).
- 🧹 **Limpeza Automática:** Apaga as imagens de comprovante locais após o envio no Telegram.

---

## 🚀 Como Executar o Bot no Terminal

### 1. Execução em Primeiro Plano (Terminal Aberto)

Navegue até a pasta do projeto e execute:

```bash
# Ativar o ambiente virtual
source venv/bin/activate

# Executar o bot
python bot.py
```

*Ou diretamente via interpretador do ambiente virtual:*

```bash
./venv/bin/python bot.py
```

> **Para parar:** Pressione **`Ctrl + C`** no terminal.

---

### 2. Execução em Segundo Plano no Linux (Background 24/7)

Para manter o bot funcionando mesmo após fechar a janela do terminal:

```bash
nohup ./venv/bin/python bot.py > bot.log 2>&1 &
```

#### 🔍 Como verificar se o bot está rodando:
```bash
ps aux | grep bot.py
```

#### 📜 Como acompanhar os logs em tempo real:
```bash
tail -f bot.log
```

#### 🛑 Como parar a execução em segundo plano:

* **Opção Rápida:**
  ```bash
  pkill -f bot.py
  ```

* **Opção por ID de Processo (PID):**
  ```bash
  # 1. Encontre o PID
  ps aux | grep bot.py

  # 2. Encerre o processo (substitua 12345 pelo PID encontrado)
  kill 12345
  ```

---

## 💬 Comandos do Bot no Telegram

| Comando | Descrição |
| :--- | :--- |
| **`/start`** | Exibe a mensagem de boas-vindas e o menu de ajuda com todos os comandos. |
| **`/entrada`** | Registra o ponto de **ENTRADA**, confirma a batida e envia o comprovante em foto. |
| **`/saida`** | Registra o ponto de **SAÍDA**, confirma a batida e envia o comprovante em foto. |
| **`/teste`** | Efetua login e acessa a tela de ponto para testar a conexão sem bater o ponto. |

---

## ⚙️ Configuração das Variáveis de Ambiente (`.env`)

O arquivo `.env` deve ser criado na raiz do projeto com as credenciais do portal e o token do Telegram:

```env
TELEGRAM_TOKEN=8018571220:AAGiY_oHNZFWXeexJ2Gj1R2O1GptI4fevBQ
MEU_LOGIN=02151683214
MINHA_SENHA=SUA_SENHA_AQUI
URL_PORTAL=https://mentorh.defensoria.pa.def.br/csp/dpepa/portal/novo/index.csp
```

---

## 🛠️ Dependências do Projeto

As dependências já estão instaladas no ambiente virtual (`venv`):
- `python-telegram-bot` (Comunicação com a API do Telegram)
- `playwright` (Automação web do Chromium)
- `python-dotenv` (Leitura de variáveis de ambiente do `.env`)

Caso precise reinstalar o navegador do Playwright:
```bash
./venv/bin/playwright install chromium
```

---

## 📂 Estrutura do Projeto

```text
Assistentebot/
│── bot.py           # Código principal do robô
│── .env             # Credenciais e tokens privados (não versionar)
│── .gitignore       # Arquivos ignorados pelo Git (.env, venv, comprovantes)
│── README.md        # Documentação completa do projeto
│── bot.log          # Arquivo de logs gerado quando rodado em segundo plano
└── venv/            # Ambiente virtual com as dependências instaladas
```
