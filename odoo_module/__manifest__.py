{
    "name": "Bot",
    "version": "0.1",
    "depends": ["base"],
    "summary": "My first Odoo App",
    "application": True,
    "data": [
        "data/bot.messages.csv",
        "security/ir.model.access.csv",
        "views/messages_property_views.xml",
        "views/messages_menus.xml",
    ],
}
