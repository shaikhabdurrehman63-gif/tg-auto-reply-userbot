# Telegram Business Auto-Reply Bot (Per-Customer)

Yeh ek **legit Telegram Bot** hai (userbot nahi). Customers aapke bot ko message karte
hain. Aap kisi bhi customer ke message par **REPLY (swipe) karke** trigger word bhejte
hain, aur uske baad us specific customer ke saare messages ka auto-reply chalu ho
jaata hai — jab tak aap wapas OFF na karein.

## Yeh kaam kaise karega (workflow)

1. Customer aapko message karta hai: "what's your last price"
2. Aap us message par **reply/swipe** karte hain aur likhte hain: `auto mood on`
3. Bot confirm karega: "✅ Auto-reply ON kar diya gaya hai for [naam]"
4. Ab us customer ka **koi bhi** message aaye, bot khud-ba-khud aapka custom
   reply bhej dega — bina aapko kuch karna pade
5. Jab chahe, us customer ke kisi message par reply karke `auto mood off` likh dein
   — us customer ke liye auto-reply band ho jayega

Yeh **sirf us ek customer** ke liye chalu hota hai jispar aapne trigger bheja —
baaki sab customers normal rehte hain jab tak aap unke liye bhi ON na karein.

## Step 1: Bot banayein (BotFather se)

1. Telegram mein `@BotFather` ko message karein
2. `/newbot` bhejein, naam aur username set karein (`_bot` se end hona chahiye)
3. Aapko ek **TOKEN** milega jaise `123456789:ABCdefGhIJKlmNoPQRstuVwxyZ` — safe rakhein

## Step 2: Apni Telegram User ID pata karein

1. `@userinfobot` ko Telegram par message karein
2. Woh aapki numeric ID bhej dega, jaise `123456789`

## Step 3: Code mein apni details bharein (`bot.py` file mein)

```python
ADMIN_IDS = [123456789]  # <-- apni user ID yahan daalein
```

```python
AUTO_REPLY_MESSAGE = """
Namaste! 🙏 Dhanyawad hamein message karne ke liye.
Hum abhi busy hain, jaldi hi aapko reply karenge.
Business hours: 10 AM - 7 PM
"""
```

Agar trigger words badalne hain (default `auto mood on` / `auto mood off`) to:

```python
TRIGGER_ON = "auto mood on"
TRIGGER_OFF = "auto mood off"
```

## Step 4: GitHub par upload karein

1. GitHub par naya repository banayein
2. `bot.py`, `requirements.txt`, `render.yaml` — teeno files upload karein
3. BOT_TOKEN seedha code mein mat likhein, Render mein environment variable se denge

## Step 5: Render par deploy karein

1. [render.com](https://render.com) par account banayein
2. **New +** → **Background Worker**
3. GitHub repo connect karein
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
5. Environment Variable add karein:
   - Key: `BOT_TOKEN`
   - Value: (BotFather wala token paste karein)
6. **Create Background Worker**

2-3 minute mein bot live ho jayega.

## Important Notes

- Yeh Bot API use karta hai — aapka personal account safe rehta hai, ban ka risk nahi
- Trigger sirf tab kaam karega jab aap kisi message par **reply (swipe)** karke word
  bhejenge — normal (non-reply) message se trigger nahi hoga
- `active_customers` list memory mein store hoti hai — agar Render free plan par bot
  restart ho (sleep se wake hote waqt), to yeh list reset ho jayegi aur aapko dobara
  `auto mood on` bhejna hoga us customer ke liye. Agar yeh permanent chahiye (restart
  ke baad bhi yaad rahe), to bata dijiye — database (jaise free Postgres ya simple
  JSON file) add kar denge
- Free plan background workers Render par kabhi-kabhi sleep/restart ho sakte hain.
  24x7 bina rukawat chalane ke liye paid **Starter plan** ($7/month se) behtar rahega
