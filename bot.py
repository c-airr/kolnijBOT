import discord
from discord import app_commands
from discord.ext import commands
from adb_bot import pierdzielnij_numer
import asyncio
import json
import os
import sys

def resource_path(relative_path: str) -> str:
    """Zwraca ścieżkę do plików obok .exe lub obok .py"""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

SETUP_PATH = resource_path("setup.json")
SHORTCUTS_PATH = resource_path("shortcuts.json")

with open(SETUP_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

TOKEN = config.get("token")
if not TOKEN:
    raise ValueError("Nie znaleziono tokena w pliku setup.json")

ALLOWED_USERS = config.get("ALLOWED_USERS", [])

with open(SHORTCUTS_PATH, "r", encoding="utf-8") as f:
    shortcuts = json.load(f)

BLOKOWANE_NUMERY = {
    "997", "998", "999", "112", "986", "911", "000", "111",
    "110", "119", "113", "122", "133", "144", "118", "117",
    "15", "17", "18", "101", "102", "103", "104", "995",
    "996", "987", "992", "991", "993", "994"
}

def sprawdz_numer(numer: str) -> bool:
    return numer not in BLOKOWANE_NUMERY

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"check {client.user} - ready")


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install
@tree.command(name="kolnij", description="kolnij na numer")
@app_commands.describe(ilosc="Ile razy zadzwonić (1-5)")
async def kolnij_command(interaction: discord.Interaction, numer: str, ilosc: int = 1):
    if any(zakazany in numer for zakazany in ["+", "#", "*"]):
        await interaction.response.send_message("nie ma kurwa dzwonienia do chinduskuf gamoniu", ephemeral=True)
        return

    if not sprawdz_numer(numer):
        await interaction.followup.send("ja ci kurwa dam zaraz guwniarzu mały")
        return
    if interaction.user.id not in ALLOWED_USERS:
        await interaction.response.send_message("oj byczku nie masz whitelisty", ephemeral=True)
        return

    ilosc = max(1, min(ilosc, 5))

    numer_info = shortcuts.get(numer.lower(), {"numer": numer, "czas": 6})
    numer_do_dzwonienia = numer_info.get("numer", numer)
    czas_polaczenia = numer_info.get("czas", 6)

    await interaction.response.send_message(
        f"No i dobrza dzwonimy na {numer_do_dzwonienia} {ilosc} razy, zwaituj chile...",
        ephemeral=False
    )
    try:
        for _ in range(ilosc):
            pierdzielnij_numer(numer_do_dzwonienia, sekundy=czas_polaczenia)
        await interaction.followup.send(f"✅ Misja wykonana ✅, potwierdzenie przelewu: {numer_do_dzwonienia}")
    except Exception as e:
        await interaction.followup.send(f"12 giga szpontu poszło sie pierdolic: {e}")

choices = [app_commands.Choice(name=name, value=name) for name in shortcuts.keys()]

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.user_install
@tree.command(name="kolnijct", description="kolnij kontakt")
@app_commands.choices(target=choices)
@app_commands.describe(ilosc="Ile razy zadzwonić (1-5)")
async def kolnijct_command(interaction: discord.Interaction, target: str, ilosc: int = 1):
    if interaction.user.id not in ALLOWED_USERS:
        await interaction.response.send_message("oj byczku nie masz whitelisty", ephemeral=True)
        return

    numer_info = shortcuts.get(target.lower(), {"numer": target, "czas": 6})
    numer_do_dzwonienia = numer_info["numer"]
    czas_polaczenia = numer_info.get("czas", 10)
    ilosc = max(1, min(ilosc, 5))

    await interaction.response.send_message(
        f"juz odpalam AJI i dzwonimy do {target} {ilosc} razy przydzwanianie...",
        ephemeral=False
    )
    try:
        for _ in range(ilosc):
            pierdzielnij_numer(numer_do_dzwonienia, sekundy=czas_polaczenia)
        await interaction.followup.send(f"✅ Misja wykonana ✅, potwierdzenie zakupu robuxow: {target}")
    except Exception as e:
        await interaction.followup.send(f"12 giga szpontu poszło sie pierdolic: {e}")

client.run(TOKEN)
