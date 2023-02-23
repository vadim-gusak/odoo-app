from odoo import fields, models


class BotMessagesModel(models.Model):
    _name = "bot.messages"
    _description = "Bot messages"

    message = fields.Text("Message for Bot", required=True, active=True)
