# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http

class MyController(http.Controller):
    @http.route('/inicio', auth='public', website=True)
    def elearning_courses(self, **kw):
        # Buscar los cursos publicados
        published_courses = http.request.env['slide.channel'].sudo().search([('is_published', '=', True)])
        
        # Buscar todas las categorías disponibles
        course_categories = http.request.env['slide.channel.tag'].sudo().search([])

        # Pasar ambos conjuntos de datos a la plantilla
        return http.request.render('web_drivers.elearning_template', {
            'courses': published_courses,
            'categories': course_categories,
        })
