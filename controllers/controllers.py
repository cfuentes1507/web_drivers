# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request

from datetime import date
from datetime import datetime

class MyController(http.Controller):
    @http.route("/inicio", auth="public", website=True)
    def elearning_courses(self, **kw):
        # Buscar los cursos publicados
        published_courses = (
            http.request.env["slide.channel"].sudo().search([("is_published", "=", True)])
        )

        # Buscar todas las categorías disponibles
        course_categories = http.request.env["slide.channel.tag"].sudo().search([])

        # Pasar ambos conjuntos de datos a la plantilla
        return http.request.render(
            "web_drivers.elearning_template",
            {
                "courses": published_courses,
                "categories": course_categories,
            },
        )


class AuthSignupHomeVat(AuthSignupHome):
    def _prepare_signup_values(self, qcontext):
        values = super(AuthSignupHomeVat, self)._prepare_signup_values(qcontext)
        if "vat" in qcontext:
            values["vat"] = qcontext.get("vat")
        if "custom_sex" in qcontext:
            values["custom_sex"] = qcontext.get("custom_sex")
        if "custom_dob" in qcontext:
            values["custom_dob"] = qcontext.get("custom_dob")
        if "custom_country_id" in qcontext:
            values["custom_country_id"] = qcontext.get("custom_country_id")
        if "custom_state_id" in qcontext:
            values["custom_state_id"] = qcontext.get("custom_state_id")
        if "custom_municipality_id" in qcontext:
            values["custom_municipality_id"] = qcontext.get("custom_municipality_id")
        if "custom_parish_id" in qcontext:
            values["custom_parish_id"] = qcontext.get("custom_parish_id")
        if "edu_sel" in qcontext:
            values["edu_sel"] = qcontext.get("edu_sel")
        if "work_state" in qcontext:
            values["work_state"] = qcontext.get("work_state")
        if "ocupation_sel" in qcontext:
            values["ocupation_sel"] = qcontext.get("ocupation_sel")
        if "entity_sel" in qcontext:
            values["entity_sel"] = qcontext.get("entity_sel")
        if "referal_sel" in qcontext:
            values["referal_sel"] = qcontext.get("referal_sel")
        return values

    @http.route("/web/signup", type="http", auth="public", website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        res = super(AuthSignupHomeVat, self).web_auth_signup()
        if request.httprequest.method == "GET" and hasattr(res, "qcontext"):
            custom_country_id = [
                (country.id, country.name)
                for country in http.request.env["res.country"].sudo().search([])
            ]
            custom_state_id = [
                (country.id, country.name)
                for country in http.request.env["res.country.state"].sudo().search([])
            ]
            custom_municipality_id = [
                (country.id, country.name)
                for country in http.request.env["res.country.municipality"].sudo().search([])
            ]
            custom_parish_id = [
                (country.id, country.name)
                for country in http.request.env["res.country.parish"].sudo().search([])
            ]
            res.qcontext.update(
                {
                    "custom_country_id": custom_country_id,
                    "custom_state_id": custom_state_id,
                    "custom_municipality_id": custom_municipality_id,
                    "custom_parish_id": custom_parish_id,
                    "edu_sel": [
                        ("no_education", "Sin escolaridad"),
                        ("pre_school", "Educación Pre Escolar"),
                        ("primary_education", "Educación Básica (Primaria)"),
                        (
                            "general_secondary",
                            "Educación Media General (1ero a 3er año de Bachillerato)",
                        ),
                        ("diversified_secondary", "Educación Diversificada (4to a 6to año)"),
                        (
                            "undergraduate",
                            "Educación Universitaria Pregrado (TSU, Licenciado o Ingeniero)",
                        ),
                        (
                            "postgraduate",
                            "Educación Universitaria Postgrado (Especialización Técnica, Especialización, Maestría o Doctorado)",
                        ),
                    ],
                    "work_state": [
                        ("public_employee", "Empleado Institución Pública"),
                        ("private_employee", "Empleado Institución Privada"),
                        ("self_employed", "Trabajo Independiente"),
                        ("unemployed", "Desempleado"),
                    ],
                    "ocupation_sel": [
                        ("student", "Estudiante"),
                        ("teacher", "Docente"),
                        ("scientific_researcher", "Investigador Científico"),
                        ("fisherman", "Pescador"),
                        ("aquaculturist", "Acuicultor"),
                        ("public_servant", "Servidor Público"),
                        ("freelance_professional", "Profesional Libre Ejercicio"),
                        ("other", "Otro"),
                    ],
                    "entity_sel": [
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
                    ],
                    "referal_sel": [
                        ("social_network", "Redes Sociales del MPPPA y entes adscritos"),
                        ("telecom", "Medios de comunicación (radio, prensa, web)"),
                        ("chat_apps", "Canales informativos de Whatsapp, Telegram, otros"),
                    ],
                    "custom_sex": [("male", "Masculino"), ("female", "Femenino")],
                }
            )
        user = request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))])
        user.sudo().write(
            {
                "vat": kw.get("vat"),
                "custom_sex": kw.get("custom_sex"),
                "custom_dob": kw.get("custom_dob"),
                "custom_country_id": kw.get("custom_country_id"),
                "custom_state_id": kw.get("custom_state_id"),
                "custom_municipality_id": kw.get("custom_municipality_id"),
                "custom_parish_id": kw.get("custom_parish_id"),
                "phone": kw.get("phone"),
                "edu_sel": kw.get("edu_sel"),
                "work_state": kw.get("work_state"),
                "ocupation_sel": kw.get("ocupation_sel"),
                "entity_sel": kw.get("entity_sel"),
                "referal_sel": kw.get("referal_sel"),
            }
        )
        return res


class CustomMyAccount(CustomerPortal):
    @http.route(["/my/account"], type="http", auth="user", website=True)
    def account(self, redirect=None, **post):
        response = super(CustomMyAccount, self).account(redirect=redirect, **post)
        if request.httprequest.method == "POST" and hasattr(response, "qcontext"):
            user = response.qcontext['sales_user']
            partner = response.qcontext['partner']
            user_dict = {}
            if response.qcontext.get("vat",False):
                user_dict['vat'] = response.qcontext.get("vat",False)
            if response.qcontext.get("user_sex",False):
                user_dict['custom_sex'] = response.qcontext.get("user_sex",False)
            if response.qcontext.get("user_dob",False):
                user_dob_str = response.qcontext.get("user_dob", False)
                user_dob_date = None
                if user_dob_str:
                    try:
                        user_dob_date = datetime.strptime(user_dob_str, "%Y-%m-%d").date()
                    except Exception as e:
                        raise Exception(f"Invalid date format for user_dob: {user_dob_str}")
                user_dict['custom_dob'] = user_dob_date
            if response.qcontext.get("country_id",False):
                user_dict['custom_country_id'] = response.qcontext.get("country_id",False)
            if response.qcontext.get("state_id",False):
                user_dict['custom_state_id'] = response.qcontext.get("state_id",False)
            if response.qcontext.get("municipality_id",False):
                user_dict['custom_municipality_id'] = response.qcontext.get("municipality_id",False)
            if response.qcontext.get("parish_id",False):
                user_dict['custom_parish_id'] = response.qcontext.get("parish_id",False)
            if response.qcontext.get("phone",False):
                user_dict['phone'] = response.qcontext.get("phone",False)
            if response.qcontext.get("edu_sel",False):
                user_dict['edu_sel'] = response.qcontext.get("edu_sel",False)
            if response.qcontext.get("work_state",False):
                user_dict['work_state'] = response.qcontext.get("work_state",False)
            if response.qcontext.get("ocupation_sel",False):
                user_dict['ocupation_sel'] = response.qcontext.get("ocupation_sel",False)
            if response.qcontext.get("entity_sel",False):
                user_dict['entity_sel'] = response.qcontext.get("entity_sel",False)
            if response.qcontext.get("referal_sel",False):
                user_dict['referal_sel'] = response.qcontext.get("referal_sel",False)
            user.sudo().write(user_dict)

        return response
