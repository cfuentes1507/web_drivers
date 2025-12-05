from odoo import models, fields, api


class ResState(models.Model):
    _inherit = "res.country.state"
    _description = "Registro State"

    name = fields.Char()

    cne_state_code = fields.Char(string="ID del Estado")

    country_id = fields.Many2one("res.country", string="country")



class ResMunicipality(models.Model):
    _name = "res.country.municipality"
    _description = "Registro Municipality"

    name = fields.Char()

    cne_municipality_code = fields.Char(string="ID del Municipio")

    state_id = fields.Many2one("res.country.state", string="Estado")


class ResParish(models.Model):
    _name = "res.country.parish"
    _description = "Registro Parish"

    name = fields.Char()

    cne_parish_code = fields.Char(string="ID de la Parroquia")

    municipality_id = fields.Many2one("res.country.municipality", string="municipality")
