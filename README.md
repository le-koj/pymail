# PyMail — HTML Email Client Agent

**Version 2.0.0**

A Python toolkit for sending HTML and plain-text emails via SMTP. Supports Gmail, custom providers, bulk sends, and an interactive Streamlit web UI. Includes Docker Compose and a Dev Container setup with [Mailpit](https://github.com/axllent/mailpit) for local SMTP testing.

## Features

- **HTML email support** — Send richly formatted newsletters from HTML templates
- **Bulk sending** — Deliver the same message to multiple recipients (configurable limit)
- **Web UI** — Streamlit-based interface: configure SMTP, upload templates, send in one click
- **Mailpit integration** — One-click local testing mode captures outbound mail without real delivery
- **CLI & scriptable** — Use as a module or run from the command line
- **Provider-agnostic** — Gmail by default; works with any SMTP server
- **Local dev stack** — Docker Compose with Mailpit (SMTP capture + web UI) and SpamAssassin

## Project Structure

```
pymail/
├── env.py                  # Global configuration (SMTP, addresses, subject)
├── app_secrets.py          # Sender password (create locally; not committed)
├── pymail_html.py          # Core: HTML email logic, SMTP, bulk send
├── streamlit_email.py      # Web UI for bulk HTML email sending
├── pymail.py               # Legacy plain-text email sender
├── no_income_no_asset.html # Sample HTML template
├── requirements.txt        # Python dependencies (Streamlit stack)
├── Dockerfile              # Python 3.12 app image (Streamlit)
├── docker-compose.yml      # App + Mailpit + SpamAssassin stack
├── .devcontainer/
│   └── devcontainer.json   # VS Code / Cursor Dev Container config
└── README.md
```

## Quick Start

### Option A: Docker Compose (recommended for local dev)

Run the Streamlit app and a local Mailpit SMTP server:

```bash
docker compose up --build
```

| Service       | URL / Port              | Purpose                          |
|---------------|-------------------------|----------------------------------|
| Streamlit app | http://localhost:8501   | Send emails via the web UI       |
| Mailpit UI    | http://localhost:8025   | View captured outbound mail      |
| Mailpit SMTP  | localhost:1025          | SMTP endpoint (no auth required) |

Inside the Compose network, `docker-compose.yml` sets `MAILPIT_HOST=mailpit` and `MAILPIT_PORT=1025`. In the Streamlit UI, check **Send to Mailpit** to route mail to the capture server — no `app_secrets.py` or SMTP password needed for local testing.

### Option B: Dev Container (VS Code / Cursor)

1. Open the project folder in VS Code or Cursor
2. Run **Dev Containers: Reopen in Container**
3. The container starts the app service with `sleep infinity` for interactive dev
4. Run `streamlit run streamlit_email.py` inside the container, or use the forwarded ports (8501, 8025)

The devcontainer runs `pip install -r requirements.txt` on create so edits to dependencies are picked up after rebuild.

### Option C: Local Python install

```bash
git clone https://github.com/le-koj/pymail.git
cd pymail
pip install -r requirements.txt
```

**Dependencies:**

- Python 3.12+
- `streamlit==1.58.0` (and transitive deps pinned in `requirements.txt`)
- Standard library: `smtplib`, `ssl`, `email`

The v2 dependency set is intentionally slim: Jupyter, PyInstaller, and other dev-only packages from v1 were removed.

### Configuration

Create `app_secrets.py` in the project root (gitignored) for production SMTP:

```python
EMAIL_PASSWORD = 'your-app-password-or-password'
```

Or set the `EMAIL_PASSWORD` environment variable (used as a fallback when `app_secrets.py` is absent, e.g. in Docker).

Create or edit `env.py` with your settings:

```python
SENDER_EMAIL = 'your-email@gmail.com'
RECIEVERS_LIST = ['recipient1@example.com', 'recipient2@example.com']
EMAIL_SUBJECT = 'Your subject line'
HTML_FILENAME = 'no_income_no_asset.html'
```

For Docker/Mailpit, `MAILPIT_HOST` and `MAILPIT_PORT` are set automatically via `docker-compose.yml`. For production SMTP, override host and port with environment variables:

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=465
```

### Run the Web UI

```bash
streamlit run streamlit_email.py
```

Configure SMTP, enter credentials, upload an HTML template, and click **Send Email**.

For local Mailpit testing, enable **Send to Mailpit** in the UI. From the host machine, captured mail is visible at http://localhost:8025. Inside Docker, Mailpit is reached at `mailpit:1025` (configured automatically).

## Usage

### Streamlit Web UI

Interactive interface for bulk HTML emails:

```bash
streamlit run streamlit_email.py
```

- **Send to Mailpit** — Toggle to capture mail locally (no password required); optional preview recipient address
- **SMTP Settings** — Host and port when not using Mailpit (Gmail: `smtp.gmail.com`, port `465` or `587`; Mailpit direct: port `1025`)
- **Email connection** — Sender address and password (or App Password); skipped in Mailpit mode
- **Compose** — Subject, comma-separated recipients (1–20), HTML file upload
- **Send** — Delivers to all recipients (or captures in Mailpit)

### Bulk HTML email (CLI)

Send to all addresses in `env.RECIEVERS_LIST`:

```bash
python pymail_html.py
```

Ensure `env.py` has:

- `SENDER_EMAIL`, `RECIEVERS_LIST`, `EMAIL_SUBJECT`
- `HTML_FILENAME` — path to your HTML template
- `app_secrets.py` with `EMAIL_PASSWORD` (or `EMAIL_PASSWORD` env var)

### Plain-text email (`pymail.py`)

Legacy script for a single plain-text message. Requires a local `secrets.py` (gitignored) with `EMAIL_PASSWORD`, and `EMAIL_ADDRESS` / `EMAIL_RECEIVERS` defined in `env.py` (not part of the default v2 template):

```bash
python pymail.py
```

### Use as a module

```python
import pymail_html as ph

# Load HTML and send to one recipient
html = ph.get_html_doc('newsletter.html')
ph.send_html_email(receiver_email='user@example.com', html_doc=html)

# Capture locally via Mailpit
ph.send_html_email(
    receiver_email='test@example.com',
    html_doc=html,
    via_mailpit=True,
)

# Or send to all in RECIEVERS_LIST
ph.send_bulk_email(html_doc=html)
```

## Configuration Reference

### `env.py`

| Variable        | Type   | Description                              |
|----------------|--------|------------------------------------------|
| `RECEIVERS_LIMIT` | int  | Max recipients per bulk send (default: 20) |
| `SMTP_HOST`    | str    | SMTP host; overridable via `SMTP_HOST` env var |
| `SMTP_PORT`    | int    | SMTP port; overridable via `SMTP_PORT` env var |
| `SMTP_PORTS`   | tuple  | Port options for UI selector             |
| `MAILPIT_HOST` | str    | Mailpit SMTP host; defaults to `localhost`, set to `mailpit` in Docker |
| `MAILPIT_PORT` | int    | Mailpit SMTP port; defaults to `1025`    |
| `SENDER_EMAIL` | str    | Sender address                           |
| `RECEIVER_EMAIL` | str  | Default single recipient                 |
| `RECIEVERS_LIST` | list  | Recipients for bulk send                 |
| `EMAIL_SUBJECT` | str   | Subject line                             |
| `HTML_FILENAME` | str   | Default HTML template path               |

### `app_secrets.py`

| Variable        | Type | Description                          |
|----------------|------|--------------------------------------|
| `EMAIL_PASSWORD` | str | Sender password or Gmail App Password |

If this file is missing, `pymail_html.py` falls back to the `EMAIL_PASSWORD` environment variable (empty string by default, which is fine for Mailpit).

## Gmail Setup

Gmail requires an **App Password** when 2-Step Verification is enabled:

1. Enable [2-Step Verification](https://myaccount.google.com/security)
2. Create an [App Password](https://myaccount.google.com/apppasswords)
3. Use that 16-character password in `app_secrets.EMAIL_PASSWORD` or the Streamlit UI

Using the normal account password will result in `535 Username and Password not accepted`.

## Security Notes

- **Never commit** `app_secrets.py` or `secrets.py` — they are in `.gitignore`
- Use App Passwords for Gmail instead of your main password
- Keep credentials out of version control and deploy scripts
- Mailpit is for local development only; do not expose it in production
- v2 pins a minimal, audited dependency set (`pip-audit` reports no known vulnerabilities)

## License

See repository for license information.
