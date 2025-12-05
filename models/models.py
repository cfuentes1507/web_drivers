# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class web_drivers(models.Model):
#     _name = 'web_drivers.web_drivers'
#     _description = 'web_drivers.web_drivers'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


class ResUsers(models.Model):
    _inherit = "res.users"

    custom_sex = fields.Selection([("male", "Masculino"), ("female", "Femenino")])
    custom_dob = fields.Date(string="Fecha de nacimiento")
    age = fields.Integer(string="Edad", compute="_compute_age")

    @api.depends("custom_dob")
    def _compute_age(self):
        for record in self:
            if record.custom_dob:
                record.age = fields.Date.today().year - record.custom_dob.year
            else:
                record.age = 0

    custom_country_id = fields.Many2one(
        "res.country",
        string="Country",
        ondelete="restrict",
        default=lambda self: self.env.ref("base.ve"),
    )
    custom_state_id = fields.Many2one(
        "res.country.state",
        string="Estado",
        domain="[('country_id', '=?', custom_country_id)]",
    )
    custom_municipality_id = fields.Many2one(
        "res.country.municipality",
        string="Municipio",
        domain="[('state_id', '=?', state_id)]",
    )
    custom_parish_id = fields.Many2one(
        "res.country.parish",
        string="Parroquia",
        domain="[('municipality_id', '=?', municipality_id)]",
    )

    edu_sel = fields.Selection(
        [
            ("no_education", "Sin escolaridad"),
            ("pre_school", "Educación Pre Escolar"),
            ("primary_education", "Educación Básica (Primaria)"),
            ("general_secondary", "Educación Media General (1ero a 3er año de Bachillerato)"),
            ("diversified_secondary", "Educación Diversificada (4to a 6to año)"),
            ("undergraduate", "Educación Universitaria Pregrado (TSU, Licenciado o Ingeniero)"),
            (
                "postgraduate",
                "Educación Universitaria Postgrado (Especialización Técnica, Especialización, Maestría o Doctorado)",
            ),
        ]
    )

    work_state = fields.Selection(
        [
            ("public_employee", "Empleado Institución Pública"),
            ("private_employee", "Empleado Institución Privada"),
            ("self_employed", "Trabajo Independiente"),
            ("unemployed", "Desempleado"),
        ]
    )

    ocupation_sel = fields.Selection(
        [
            ("student", "Estudiante"),
            ("teacher", "Docente"),
            ("scientific_researcher", "Investigador Científico"),
            ("fisherman", "Pescador"),
            ("aquaculturist", "Acuicultor"),
            ("public_servant", "Servidor Público"),
            ("freelance_professional", "Profesional Libre Ejercicio"),
            ("other", "Otro"),
        ]
    )

    entity_sel = fields.Selection(
        [
            ("mpppa", "MPPPA"),
            ("insopesca", "INSOPESCA"),
            ("corpesca", "CORPESCA"),
            ("fonpesca", "FONPESCA"),
            ("cenipa", "CENIPA"),
            ("pescalba", "PESCALBA"),
            ("juventud_pesquera", "Juventud Pesquera"),
            ("conppa", "CONPPA"),
            ("cooperativa", "Cooperativa"),
            ("movimiento_estudiantil", "Movimiento Estudiantil"),
            ("consejo_comunal", "Consejo Comunal"),
        ]
    )

    referal_sel = fields.Selection(
        [
            ("social_network", "Redes Sociales del MPPPA y entes adscritos"),
            ("telecom", "Medios de comunicación (radio, prensa, web)"),
            ("chat_apps", "Canales informativos de Whatsapp, Telegram, otros"),
        ]
    )


class ResPartner(models.Model):
    _inherit = "res.partner"
    # Campo auxiliar para encontrar el usuario asociado (si existe)
    user_id = fields.Many2one("res.users", compute="_compute_user_id", store=False)

    # Campo calculado para enlazar al primer usuario, ya que res.users tiene Many2one a res.partner
    def _compute_user_id(self):
        for partner in self:
            partner.user_id = partner.user_ids[0] if partner.user_ids else False

    # --- Definición de Campos Relacionados ---
    # Estos campos "copian" el valor del campo original en res.users

    # Ejemplo para 'custom_country_id'
    # La ruta es: 'user_id.custom_country_id_en_res_users'
    # **¡Advertencia!** Debes saber el nombre real del campo en res.users
    user_country_id = fields.Many2one(
        "res.country",
        string="País del Usuario",
        related="user_id.custom_country_id",  # <-- Apunta al campo original
        readonly=True,  # Los campos relacionados son de solo lectura por defecto
    )
    user_state_id = fields.Many2one(
        "res.country.state",
        string="Estado del Usuario",
        related="user_id.custom_state_id",
        readonly=True,
    )
    user_municipality_id = fields.Many2one(
        "res.country.municipality",
        string="Municipio del Usuario",
        related="user_id.custom_municipality_id",
        readonly=True,
    )
    user_parish_id = fields.Many2one(
        "res.country.parish",
        string="Parroquia del Usuario",
        related="user_id.custom_parish_id",
        readonly=True,
    )
    # Campos de Selección (uso del campo related)
    user_sex = fields.Selection(
        related="user_id.custom_sex",
        string="Sexo",
        readonly=True,
    )
    user_edu_sel = fields.Selection(
        related="user_id.edu_sel",
        string="Educación",
        readonly=True,
    )
    user_work_state = fields.Selection(
        related="user_id.work_state",
        string="Estatus Laboral",
        readonly=True,
    )
    user_ocupation_sel = fields.Selection(
        related="user_id.ocupation_sel",
        string="Ocupación",
        readonly=True,
    )
    user_entity_sel = fields.Selection(
        related="user_id.entity_sel",
        string="Ente de Adscripción",
        readonly=True,
    )
    # Date
    user_dob = fields.Date(string="Fecha Nacimiento del Usuario", related="user_id.custom_dob")
    user_age = fields.Integer(
        string="Edad del Usuario",
        related="user_id.age",  # <-- Apunta al campo 'age' de res.users
        readonly=True,
        store=False,  # Como el campo original es calculado y no almacenado
    )

    # Y así sucesivamente para todos los campos:
    # user_age = fields.Integer(related='user_id.age')
    # user_sex = fields.Selection(related='user_id.custom_sex')


class WebDriverSideChannel(models.Model):
    _inherit = "slide.channel.partner"
    _description = "web_drivers.side_channel"

    partner_id_vat = fields.Char(string="VAT", related="partner_id.vat")
