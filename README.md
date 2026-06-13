# PyMail — HTML Email Client Agent

**Version 2.0.0**

A Python toolkit for sending HTML and plain-text emails via SMTP. Supports Gmail, custom providers, bulk sends, and an interactive Streamlit web UI. Includes Docker Compose and a Dev Container setup with [Mailpit](https://github.com/axllent/mailpit) for local SMTP testing.

## Features

- **HTML email support** — Send richly formatted newsletters from HTML templates
- **Bulk sending** — Deliver the same message to multiple recipients (configurable limit)
- **Web UI** — Streamlit-based interface: configure SMTP, upload templates, send in one click
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
├── pymail.py               # Simple plain-text email sender
├── no_income_no_asset.html # Sample HTML template
├── requirements.txt        # Python dependencies
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

Inside the Compose network, `env.py` reads `SMTP_HOST=mailpit` and `SMTP_PORT=1025` from environment variables — no `app_secrets.py` needed for local testing.

### Option B: Dev Container (VS Code / Cursor)

1. Open the project folder in VS Code or Cursor
2. Run **Dev Containers: Reopen in Container**
3. The container starts the app service with `sleep infinity` for interactive dev
4. Run `streamlit run streamlit_email.py` inside the container, or use the forwarded ports (8501, 8025)

### Option C: Local Python install

```bash
git clone <repository-url>
cd pymail
pip install -r requirements.txt
```

**Dependencies:**

- Python 3.12+
- `streamlit>=1.37.0` — web UI
- Standard library: `smtplib`, `ssl`, `email`

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

For Docker/Mailpit, `SMTP_HOST` and `SMTP_PORT` are set automatically via `docker-compose.yml`. For other deployments, override them with environment variables:

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=465
```

### Run the Web UI

```bash
streamlit run streamlit_email.py
```

Configure SMTP, enter credentials, upload an HTML template, and click **Send Email**.

When using Mailpit locally, set host to `mailpit` (inside Docker) or `localhost` (from the host) and port `1025`; leave the password blank.

## Usage

### Streamlit Web UI

Interactive interface for bulk HTML emails:

```bash
streamlit run streamlit_email.py
```

- **SMTP Settings** — Host and port (Gmail: `smtp.gmail.com`, port `465` or `587`; Mailpit: port `1025`)
- **Email connection** — Sender address and password (or App Password)
- **Compose** — Subject, comma-separated recipients (1–20), HTML file upload
- **Send** — Delivers to all recipients

### Bulk HTML email (CLI)

Send to all addresses in `env.RECIEVERS_LIST`:

```bash
python pymail_html.py
```

Ensure `env.py` has:

- `SENDER_EMAIL`, `RECIEVERS_LIST`, `EMAIL_SUBJECT`
- `HTML_FILENAME` — path to your HTML template

### Plain-text email (`pymail.py`)

Send a single plain-text message (uses `env` and `secrets`):

```bash
python pymail.py
```

Requires in `env.py`:

- `EMAIL_ADDRESS` — sender
- `EMAIL_RECEIVERS` — recipient

And in `secrets.py`:

- `EMAIL_PASSWORD`

### Use as a module

```python
import pymail_html as ph

# Load HTML and send to one recipient
html = ph.get_html_doc('newsletter.html')
ph.send_html_email(receiver_email='user@example.com', html_doc=html)

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

## Building a Standalone Executable

Use PyInstaller to bundle `pymail_html.py`:

```bash
pyinstaller pymail_html.spec
```

The executable will be in `dist/pymail_html`. Ensure `env.py` and `app_secrets.py` are available in the working directory when you run it.

## Security Notes

- **Never commit** `app_secrets.py` or `secrets.py` — they are in `.gitignore`
- Use App Passwords for Gmail instead of your main password
- Keep credentials out of version control and deploy scripts
- Mailpit is for local development only; do not expose it in production

## License

See repository for license information.
