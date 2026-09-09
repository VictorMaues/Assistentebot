import os
import json
import asyncio
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
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

def obter_dados_belem():
    """Busca o horário atual e a temperatura em Belém - PA via Open-Meteo API"""
    now = datetime.now(ZoneInfo("America/Belem"))
    horario_str = now.strftime("%d/%m/%Y às %H:%M:%S")

    url = "https://api.open-meteo.com/v1/forecast?latitude=-1.4558&longitude=-48.4902&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode())
    
    current = data.get("current", {})
    temp = current.get("temperature_2m")
    sensacao = current.get("apparent_temperature")
    umidade = current.get("relative_humidity_2m")
    code = current.get("weather_code")

    wmo_map = {
        0: "Céu limpo ☀️",
        1: "Predominantemente ensolarado 🌤️",
        2: "Parcialmente nublado ⛅",
        3: "Nublado ☁️",
        45: "Nevoeiro 🌫️",
        48: "Nevoeiro 🌫️",
        51: "Garoa leve 🌧️",
        53: "Garoa moderada 🌧️",
        55: "Garoa densa 🌧️",
        61: "Chuva leve 🌧️",
        63: "Chuva moderada 🌧️",
        65: "Chuva forte 🌧️",
        80: "Pancadas de chuva leves 🌦️",
        81: "Pancadas de chuva moderadas 🌦️",
        82: "Pancadas de chuva violentas ⛈️",
        95: "Tempestade ⛈️",
    }
    condicao = wmo_map.get(code, "Condição variável 🌤️")

    return {
        "horario": horario_str,
        "temperatura": temp,
        "sensacao": sensacao,
        "umidade": umidade,
        "condicao": condicao
    }

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

async def comando_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        info = await asyncio.to_thread(obter_dados_belem)
        mensagem = (
            f"📍 *Belém - PA*\n\n"
            f"🕒 *Horário Atual:* {info['horario']}\n"
            f"🌡️ *Temperatura:* {info['temperatura']}°C\n"
            f"🔥 *Sensação Térmica:* {info['sensacao']}°C\n"
            f"💧 *Umidade:* {info['umidade']}%\n"
            f"🌤️ *Condição:* {info['condicao']}"
        )
    except Exception as e:
        now = datetime.now(ZoneInfo("America/Belem"))
        horario_str = now.strftime("%d/%m/%Y às %H:%M:%S")
        mensagem = (
            f"📍 *Belém - PA*\n\n"
            f"🕒 *Horário Atual:* {horario_str}\n"
            f"⚠️ *Temperatura:* Não foi possível obter a temperatura no momento."
        )
    await update.message.reply_text(mensagem, parse_mode="Markdown")

async def comando_horario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.now(ZoneInfo("America/Belem"))
    hoje_inicio = now.replace(hour=8, minute=0, second=0, microsecond=0)
    hoje_fim = now.replace(hour=14, minute=0, second=0, microsecond=0)

    horario_atual_str = now.strftime("%H:%M:%S")

    if now < hoje_inicio:
        mensagem = (
            f"⏳ *Status da Jornada (08:00 às 14:00)*\n\n"
            f"🕒 *Horário Atual:* {horario_atual_str}\n"
            f"⚠️ *Ainda não foi iniciada a contagem do dia.* O expediente começa às 08:00."
        )
    elif now >= hoje_fim:
        mensagem = (
            f"✅ *Status da Jornada (08:00 às 14:00)*\n\n"
            f"🕒 *Horário Atual:* {horario_atual_str}\n"
            f"🎉 *Jornada de hoje finalizada!* Você já cumpriu as 6 horas de trabalho do dia."
        )
    else:
        decorrido = now - hoje_inicio
        restante = hoje_fim - now

        segundos_cump = int(decorrido.total_seconds())
        horas_cump = segundos_cump // 3600
        minutos_cump = (segundos_cump % 3600) // 60

        segundos_falt = int(restante.total_seconds())
        horas_falt = segundos_falt // 3600
        minutos_falt = (segundos_falt % 3600) // 60

        # Barra de progresso visual
        total_segundos = 6 * 3600
        pct = min(100, int((segundos_cump / total_segundos) * 100))
        blocos = pct // 10
        barra = "▓" * blocos + "░" * (10 - blocos)

        str_cumprido = f"{horas_cump}h {minutos_cump}min" if horas_cump > 0 else f"{minutos_cump}min"
        str_falta = f"{horas_falt}h {minutos_falt}min" if horas_falt > 0 else f"{minutos_falt}min"

        mensagem = (
            f"📊 *Status da Jornada (08:00 às 14:00)*\n\n"
            f"🕒 *Horário Atual:* {horario_atual_str}\n"
            f"⏱️ *Horas cumpridas:* {str_cumprido}\n"
            f"⏳ *Horas restantes:* {str_falta}\n\n"
            f"Progresso: `[{barra}] {pct}%`"
        )

    await update.message.reply_text(mensagem, parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mensagem = (
        "👋 *Bem-vindo ao CamufladoBot!*\n\n"
        "Eu sou seu assistente para automação de registro de ponto no portal Mentorh.\n\n"
        "📌 *Comandos disponíveis:*\n"
        "🟢 /entrada - Registra seu ponto de ENTRADA e envia o comprovante.\n"
        "🔴 /saida - Registra seu ponto de SAÍDA e envia o comprovante.\n"
        "🧪 /teste - Testa a conexão e exibe a tela de ponto sem bater o ponto.\n"
        "🕒 /time - Exibe o horário atual e a temperatura em Belém - PA.\n"
        "⏰ /horario - Exibe o tempo cumprido e restante do expediente (08:00 às 14:00).\n"
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

    # Registra os comandos /start, /entrada, /saida, /teste, /time e /horario
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("entrada", bater_entrada))
    app.add_handler(CommandHandler("saida", bater_saida))
    app.add_handler(CommandHandler("teste", teste_bot))
    app.add_handler(CommandHandler("time", comando_time))
    app.add_handler(CommandHandler(["horario", "horario"], comando_horario))

    print("CamufladoBot operando nas sombras... Pressione Ctrl+C para parar.")
    app.run_polling()

if __name__ == "__main__":
    main()