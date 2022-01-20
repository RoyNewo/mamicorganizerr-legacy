import requests
from discord import Webhook, RequestsWebhookAdapter

webhook = Webhook.from_url(
    "https://discord.com/api/webhooks/921367652843262002/qXvzLrTzM6KD7XEKhBlSTeRFbIj_BnqfavYeV-bqSozaY-qpm7xIQzdvprAyNKmaUNC6",
    adapter=RequestsWebhookAdapter(),
)
webhook.send("Hello World")
