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

## 🤖 Como Criar seu Próprio Bot no Telegram (BotFather)

Para utilizar este programa, você precisa criar o seu próprio bot no Telegram e obter um **Token de Acesso**. Siga o passo a passo abaixo:

1. **Abra o Telegram** e pesquise pelo usuário oficial **`@BotFather`** (ou acesse [t.me/BotFather](https://t.me/BotFather)).
2. Clique em **Começar** ou envie o comando `/start`.
3. Crie um novo bot enviando o comando:
   ```text
   /newbot
   ```
4. **Defina o Nome do Bot:** O BotFather solicitará um nome visível (exemplo: `Meu Ponto Bot`).
5. **Defina o Username do Bot:** O BotFather solicitará um nome de usuário único que **obrigatoriamente deve terminar com `bot`** (exemplo: `MeuPontoOficial_bot`).
6. **Copie o Token de API:** O BotFather enviará uma mensagem de confirmação com um token no formato:
   `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz...`
7. Cole esse token no arquivo `.env` no campo `TELEGRAM_TOKEN`.

> 💡 **Dica (Opcional):** Para cadastrar o menu de comandos automáticos no Telegram, envie `/setcommands` para o `@BotFather`, escolha seu bot e envie o texto abaixo:
> ```text
> start - Boas-vindas e ajuda
> entrada - Registrar ponto de entrada
> saida - Registrar ponto de saída
> teste - Testar conexão sem bater ponto
> ```

---

## 📦 Requisitos e Instalação

### Requisitos Prévios
- **Python 3.8** ou superior instalado.

### Passo a Passo de Instalação

Navegue até a pasta do projeto no terminal e siga as etapas:

1. **Criar e Ativar o Ambiente Virtual (`venv`):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Instalar as Dependências do Python:**
   ```bash
   pip install python-telegram-bot playwright python-dotenv
   ```

   **Dependências instaladas:**
   - `python-telegram-bot`: Comunicação com a API do Telegram.
   - `playwright`: Automação e navegação web em modo invisível.
   - `python-dotenv`: Leitura de variáveis de ambiente a partir do arquivo `.env`.

3. **Instalar os Navegadores do Playwright (Chromium):**
   ```bash
   playwright install chromium
   ```

   *(Opcional no Linux)* Caso esteja em um ambiente de servidor sem interface gráfica e falte dependências do sistema:
   ```bash
   playwright install-deps chromium
   ```

---

## ⚙️ Configuração das Variáveis de Ambiente (`.env`)

Crie um arquivo chamado `.env` na raiz do projeto e insira o seu token gerado pelo BotFather juntamente com suas credenciais do portal:

```env
TELEGRAM_TOKEN=SEU_TOKEN_GERADO_PELO_BOTFATHER
MEU_LOGIN=SEU_CPF_OU_MATRICULA
MINHA_SENHA=SUA_SENHA_DO_PORTAL
URL_PORTAL=https://mentorh.defensoria.pa.def.br/csp/dpepa/portal/novo/index.csp
```

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
