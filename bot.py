import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from playwright.async_api import async_playwright

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
MEU_LOGIN = os.getenv("MEU_LOGIN")
MINHA_SENHA = os.getenv("MINHA_SENHA")
URL_PORTAL = os.getenv("URL_PORTAL", "https://mentorh.defensoria.pa.def.br/csp/dpepa/portal/novo/index.csp")

async def automatizar_ponto(tipo: str) -> str:
    """Função que controla o navegador invisível"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # 1. Acessa o site (usa domcontentloaded para evitar travamentos em requisições de fundo)
            await page.goto(URL_PORTAL, wait_until="domcontentloaded", timeout=30000)
            
            # 2. Faz o Login (Com os seletores CSS #login, #senha e #acessar)
            await page.wait_for_selector("#login", state="attached", timeout=15000)
            await page.fill("#login", MEU_LOGIN)
            await page.fill("#senha", MINHA_SENHA)
            await page.click("#acessar")
            
            # 3. Aguarda o portal carregar e abre o menu 'Registrar Ponto' (menu="100.3.6.40")
            await page.wait_for_selector('a[menu="100.3.6.40"]', state="attached", timeout=15000)
            await page.evaluate("""() => {
                const el = document.querySelector('a[menu="100.3.6.40"]') || Array.from(document.querySelectorAll('a')).find(a => a.innerText.includes('Registrar Ponto'));
                if (el) el.click();
            }""")
            
            # Aguarda a tela de registro de ponto carregar e o botão estar visível
            await page.wait_for_selector("#bater_ponto", state="visible", timeout=15000)
            
            # 4. Clica no botão de bater o ponto e confirma o diálogo
            if tipo in ["entrada", "saida"]:
                print(f"Clicando em #bater_ponto para {tipo}...")
                await page.click("#bater_ponto")
                await asyncio.sleep(1)
                
                # Clica no botão 'Sim' da caixa de diálogo de confirmação que aparece na tela
                print("Confirmando a caixa de diálogo (clicando no botão 'Sim')...")
                await page.evaluate("""() => {
                    const buttons = Array.from(document.querySelectorAll('.divVerify button, #divMessage button, button'));
                    const simBtn = buttons.find(b => b.innerText.trim() === 'Sim');
                    if (simBtn) simBtn.click();
                }""")
                
                # Aguarda o servidor registrar o ponto e atualizar o sistema
                await asyncio.sleep(4)
            
            # 5. Tira um print como comprovante
            caminho_print = f"comprovante_{tipo}.png"
            await page.screenshot(path=caminho_print)
            
            return caminho_print
            
        except Exception as e:
            return f"ERRO: {str(e)}"
        finally:
            await browser.close()

# Comandos do Telegram
async def bater_entrada(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🕵️‍♂️ CamufladoBot acessando o servidor para registrar a ENTRADA...")
    
    resultado = await automatizar_ponto("entrada")
    
    if resultado.startswith("ERRO"):
        await update.message.reply_text(f"❌ Falha ao registrar:\n{resultado}")
    else:
        with open(resultado, "rb") as foto:
            await update.message.reply_photo(photo=foto, caption="✅ Ponto de ENTRADA registrado com sucesso!")
        os.remove(resultado)

async def bater_saida(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🕵️‍♂️ CamufladoBot acessando o servidor para registrar a SAÍDA...")
    
    resultado = await automatizar_ponto("saida")
    
    if resultado.startswith("ERRO"):
        await update.message.reply_text(f"❌ Falha ao registrar:\n{resultado}")
    else:
        with open(resultado, "rb") as foto:
            await update.message.reply_photo(photo=foto, caption="✅ Ponto de SAÍDA registrado com sucesso! Bom descanso.")
        os.remove(resultado)

async def teste_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🧪 Executando teste de conexão, login e navegação até a tela de ponto...")

    resultado = await automatizar_ponto("teste")

    if resultado.startswith("ERRO"):
        await update.message.reply_text(f"❌ Falha no teste:\n{resultado}")
    else:
        with open(resultado, "rb") as foto:
            await update.message.reply_photo(photo=foto, caption="✅ Teste aprovado! Tela de ponto acessada e comprovante gerado.")
        os.remove(resultado)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensagem = (
        "👋 *Bem-vindo ao CamufladoBot!*\n\n"
        "Eu sou seu assistente para automação de registro de ponto no portal Mentorh.\n\n"
        "📌 *Comandos disponíveis:*\n"
        "🟢 /entrada - Registra seu ponto de ENTRADA e envia o comprovante.\n"
        "🔴 /saida - Registra seu ponto de SAÍDA e envia o comprovante.\n"
        "🧪 /teste - Testa a conexão e exibe a tela de ponto sem bater o ponto.\n"
        "❓ /start - Exibe esta mensagem de ajuda."
    )
    await update.message.reply_text(mensagem, parse_mode="Markdown")

def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN não encontrado no arquivo .env!")

    app = (
        Application.builder()
        .token(TOKEN)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .build()
    )

    # Registra os comandos /start, /entrada, /saida e /teste
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("entrada", bater_entrada))
    app.add_handler(CommandHandler("saida", bater_saida))
    app.add_handler(CommandHandler("teste", teste_bot))

    print("CamufladoBot operando nas sombras... Pressione Ctrl+C para parar.")
    app.run_polling()

if __name__ == "__main__":
    main()