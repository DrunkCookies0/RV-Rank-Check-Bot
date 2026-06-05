# RV Rank Check Bot

A Discord bot that calculates unofficial Rocket League league tiers based on your peak MMR in 2v2 and 3v3.

---

## Quick Start

```bash
# 1. Clone & install
git clone https://github.com/DrunkCookies0/RV-Rank-Check-Bot.git
cd RV-Rank-Check-Bot
pip install -r requirements.txt

# 2. Set your bot token
export DISCORD_TOKEN=your_token_here        # macOS / Linux
$env:DISCORD_TOKEN="your_token_here"        # Windows PowerShell

# 3. Run
python main.py
```

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Discord Bot Setup](#discord-bot-setup)
3. [Local Environment Setup](#local-environment-setup)
4. [Command Usage](#command-usage)
5. [Development & Testing](#development--testing)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)
8. [Security & Maintenance](#security--maintenance)

---

## Prerequisites

Install the following before proceeding:

| Program | Version | Download |
|---------|---------|----------|
| **Python** | 3.12.x | https://www.python.org/downloads/ |
| **pip** | bundled with Python | — |
| **Git** | any recent | https://git-scm.com/downloads |

You also need a **Discord account** with access to the [Discord Developer Portal](https://discord.com/developers/applications).

> **Verify your Python version**
> ```bash
> python --version   # should print Python 3.12.x
> ```
> On some systems the command is `python3`. Use whichever resolves to 3.12.

---

## Discord Bot Setup

### 1. Create a new application

1. Go to https://discord.com/developers/applications and click **New Application**.
2. Give it a name (e.g. `RV Rank Check Bot`) and click **Create**.

### 2. Add a Bot user

1. In the left sidebar, click **Bot**.
2. Click **Add Bot** → **Yes, do it!**
3. Under **Token**, click **Reset Token**, then **Copy** and save it somewhere safe — you will need it later and it is shown only once.

### 3. Configure Privileged Intents

This bot uses only the default intents.  
In the **Bot** page, make sure all **Privileged Gateway Intents** toggles are **OFF** (the code does not require them).

### 4. Generate an invite URL

1. In the left sidebar, click **OAuth2 → URL Generator**.
2. Under **Scopes**, check:
   - `bot`
   - `applications.commands`
3. Under **Bot Permissions**, check:
   - `Send Messages`
   - `Use Slash Commands`
4. Copy the generated URL at the bottom of the page.

### 5. Invite the bot to your server

1. Paste the URL into your browser.
2. Select your server from the dropdown and click **Authorise**.
3. Complete the CAPTCHA.

The bot will now appear in your server's member list (offline until you run it).

---

## Local Environment Setup

### 1. Clone the repository

```bash
git clone https://github.com/DrunkCookies0/RV-Rank-Check-Bot.git
cd RV-Rank-Check-Bot
```

### 2. Create and activate a virtual environment (recommended)

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs `nextcord`, the Discord library used by the bot.

### 4. Set the bot token

The bot reads the token from the `DISCORD_TOKEN` environment variable.

**macOS / Linux (current session)**
```bash
export DISCORD_TOKEN=your_token_here
```

**Windows PowerShell (current session)**
```powershell
$env:DISCORD_TOKEN="your_token_here"
```

Replace `your_token_here` with the token you copied from the Discord Developer Portal.

### 5. Start the bot

```bash
python main.py
```

Expected output on successful startup:
```
logged in as YourBotName (123456789012345678)
_____________________________________
```

The bot is now online. Try the slash command in your Discord server.

---

## Command Usage

The bot registers a global slash command group `/checktier`.

### `/checktier rocket_league`

Calculates your unofficial league tier based on peak Rocket League MMR.

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| `peak3s` | integer | ✅ | 0 – 2500 | Your peak 3v3 MMR |
| `peak2s` | integer | ✅ | 0 – 2500 | Your peak 2v2 MMR |

> Both values must be **≥ 300**; the bot will return an error for lower inputs.

**Example**
```
/checktier rocket_league peak3s:1600 peak2s:1500
```

**Example output**
```
Given the following peaks:
    3v3: 1600
    2v2: 1500
Your unofficial league ranks are:
    3v3: 1575 (Tier 2)
    2v2: 1525 (Tier 3)
```

### Tier Ranges

| Tier | MMR Range (3v3 & 2v2) |
|------|----------------------|
| Tier 1 | 1800+ |
| Tier 2 | 1650 – 1799 |
| Tier 3 | 1500 – 1649 |
| Tier 4 | 1350 – 1499 |
| Tier 5 | 1200 – 1349 |
| Tier 6 | 1050 – 1199 |
| Tier 7 | 300 – 1049 |

---

## Development & Testing

### Why use `test_main.py`?

Global slash commands (used by `main.py`) can take **up to an hour** to propagate across Discord. During development, use `test_main.py` instead — it registers commands to a specific guild immediately.

### Setup for testing

1. **Find your test server's Guild ID**
   - In Discord, enable Developer Mode: *Settings → Advanced → Developer Mode*.
   - Right-click your server icon → **Copy Server ID**.

2. **Create `config.json`** in the project root:
   ```json
   {
     "token": "your_token_here"
   }
   ```
   > ⚠️ `config.json` is listed in `.gitignore` — never commit it.

3. **Update the guild ID in `test_main.py`**
   Open `test_main.py` and replace the existing guild ID on this line:
   ```python
   bot.add_cog(CheckTier(bot, [YOUR_GUILD_ID_HERE]))
   ```

4. **Run the test entry point**
   ```bash
   python test_main.py
   ```
   Slash commands will appear in your test server within seconds.

---

## Deployment

The repository includes a `Procfile` for platforms that support worker-type processes (e.g. Railway, Render, Heroku):

```
worker: python main.py
```

### General steps for any host

1. Push the repository to your hosting provider.
2. Add the environment variable `DISCORD_TOKEN` with your bot token in the platform's settings panel.
3. Start a **worker** dyno/service (not a web server — this bot has no HTTP server).
4. Check the platform's log output for the `logged in as …` message to confirm the bot is running.

> The Python runtime version is pinned to `3.12.6` in `runtime.txt`. Ensure your hosting platform respects this file or configure the version manually.

---

## Troubleshooting

### Bot appears offline / token errors

- Confirm `DISCORD_TOKEN` is set correctly: `echo $DISCORD_TOKEN` (macOS/Linux) or `$env:DISCORD_TOKEN` (PowerShell).
- Make sure there are no leading/trailing spaces in the token value.
- If the token stopped working, regenerate it in the Developer Portal (**Bot → Reset Token**) and update your environment variable.

### Slash command `/checktier` not appearing

- Verify the invite URL included both the `bot` and `applications.commands` scopes.
- If using `main.py` (global commands), wait up to 60 minutes for Discord to propagate the command.
- For instant registration, switch to `test_main.py` with a guild ID (see [Development & Testing](#development--testing)).
- Re-check the bot has **Use Slash Commands** permission in the channel or server.

### Bot sends no response / permission error

- Ensure the bot role has **Send Messages** permission in the target channel.
- Check that the channel is not restricted to specific roles that exclude the bot.

### Python version mismatch

- Confirm `python --version` prints `3.12.x`.
- If you have multiple Python versions, use `python3.12 -m venv .venv` to create the virtual environment explicitly.

### Dependency errors on install

- Ensure you have activated the virtual environment before running `pip install`.
- Try upgrading pip first: `pip install --upgrade pip`.

---

## Security & Maintenance

- **Never commit your bot token.** It grants full control of your bot. `config.json` is already in `.gitignore`.
- **Rotate a leaked token immediately** in the Discord Developer Portal (**Bot → Reset Token**), then update all environments where you use it.
- **Keep permissions minimal.** Only grant the bot the permissions it actually needs (`Send Messages`, `Use Slash Commands`).
- **Pin dependencies** by running `pip freeze > requirements.txt` after testing to lock exact package versions and prevent unexpected breakage from upstream updates.
- **Review dependencies periodically** for security advisories (`pip list --outdated`).
