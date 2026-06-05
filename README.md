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

For Railway deployment, put the token in **Railway → Service → Variables** as `DISCORD_TOKEN`.

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

### 4. Generate an invite URL (current Discord UI)

1. In the left sidebar, click **OAuth2**.
2. On the OAuth2 page, scroll to the **OAuth2 URL Generator** section.
3. Under **Scopes**, check:
   - `bot`
   - `applications.commands`
4. Under **Bot Permissions**, check:
   - `Send Messages`
   - `Use Slash Commands`
5. Copy the value from **Generated URL** at the bottom.

> You only need your bot token from the **Bot** page to run this project.
> Do **not** use or share the OAuth2 **Client Secret**.

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

Use the token from the Discord Developer Portal **Bot** page.

| Use case | Where the token goes |
|----------|----------------------|
| Run `python main.py` locally | `DISCORD_TOKEN` environment variable |
| Run `python test_main.py` locally | `config.json` in the project root |
| Deploy on Railway | Railway service variable named `DISCORD_TOKEN` |

The normal bot entry point (`main.py`) reads the token from the `DISCORD_TOKEN` environment variable.

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

The bot is now online. Use `/checktier setup_panel` (admin only) once in each channel where you want the button panel to appear.

---

## Command Usage

The bot registers a global slash command group `/checktier`.

### `/checktier setup_panel` (Admin only)

Posts a rank-check panel in the current channel with a persistent button:
- **Button text:** `Click here to check your rank tier`
- Clicking the button opens a popup modal
- Users enter `peak3s` and `peak2s`
- Bot posts their unofficial rank tier result in chat

Only server admins can run this setup command.

### Modal inputs (`Check Your Rank Tier`)

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| `peak3s` | integer | ✅ | 300 – 2500 | Your peak 3v3 MMR |
| `peak2s` | integer | ✅ | 300 – 2500 | Your peak 2v2 MMR |

> Both values must be within **300–2500**; the bot will return an error for invalid inputs.

**Setup example**
```
/checktier setup_panel
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

Global slash commands (used by `main.py`) can take **up to an hour** to propagate across Discord.

> Note: as currently implemented, `checkTierRL.py` registers commands globally because `guild_ids` is `None` at import time. If you want instant guild-scoped registration during development, update the `@nextcord.slash_command(guild_ids=...)` decorator to include your Guild ID(s) and then run `test_main.py`.
### Setup for testing

1. **Invite the bot to a test server**
   - Use the OAuth2 URL from [Discord Bot Setup](#discord-bot-setup).
   - Pick a server you control so you can safely test slash commands.

2. **Find your test server's Guild ID**
   - In Discord, enable Developer Mode: *Settings → Advanced → Developer Mode*.
   - Right-click your server icon → **Copy Server ID**.

3. **Create `config.json`** in the project root:
   ```json
   {
     "token": "your_token_here"
   }
   ```
   > ⚠️ `config.json` is listed in `.gitignore` — never commit it.

4. **Update the guild ID in `test_main.py`**
   Open `test_main.py` and replace the existing guild ID on this line:
   ```python
   bot.add_cog(CheckTier(bot, [YOUR_GUILD_ID_HERE]))
   ```

5. **Run the test entry point**
   ```bash
   python test_main.py
   ```
   Slash commands will appear in your test server within seconds.

6. **Test the bot in Discord**
   - Open the server where you invited the bot.
   - In any channel where you want rank checks, run `/checktier setup_panel` as an admin.
   - Click the **Click here to check your rank tier** button.
   - Enter values for `peak3s` and `peak2s` such as `1600` and `1500`.
   - Submit the modal and confirm the bot posts the calculated tiers in chat.

---

## Deployment

The repository includes a `Procfile` for platforms that support worker-type processes (e.g. Railway, Render, Heroku):

```
worker: python main.py
```

### Railway setup

1. Push this repository to GitHub.
2. In Railway, create a **New Project** and choose **Deploy from GitHub repo**.
3. Select this repository.
4. After Railway creates the service, open the service and go to **Variables**.
5. Add a variable named `DISCORD_TOKEN` and paste in your bot token from the Discord Developer Portal.
6. Deploy the service.
7. Open the Railway logs and confirm you see the `logged in as ...` message.

> This project is a background worker, not a web app. If Railway asks for a start command, use `python main.py`.

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

### Slash command `/checktier setup_panel` not appearing

- Verify the invite URL included both the `bot` and `applications.commands` scopes.
- If using `main.py` (global commands), wait up to 60 minutes for Discord to propagate the command.
- For instant registration, switch to `test_main.py` with a guild ID (see [Development & Testing](#development--testing)).
- Re-check the bot has **Use Slash Commands** permission in the channel or server.
- The user running setup must be a server admin.

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
