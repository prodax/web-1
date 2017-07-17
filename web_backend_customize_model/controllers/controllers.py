# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class BackendCustomizeModel(http.Controller):

    def get_view_ids(self, xml_ids):
        ids = []
        for xml_id in xml_ids:
            if "." in xml_id:
                record_id = request.env.ref(xml_id).id
            else:
                record_id = int(xml_id)
            ids.append(record_id)
        return ids

    @http.route(['/backend/theme_customize_get'], type='json', auth="public",
                website=True)
    def theme_customize_get(self, xml_ids):
        enable = []
        disable = []
        ids = self.get_view_ids(xml_ids)
        for view in request.env['ir.ui.view'].with_context(
                active_test=True).browse(ids):
            if view.active:
                enable.append(view.xml_id)
            else:
                disable.append(view.xml_id)
        return [enable, disable]

    @http.route(['/backend/theme_customize'], type='json', auth="public",
                website=True)
    def theme_customize(self, enable, disable, get_bundle=False):
        """ enable or Disable lists of ``xml_id`` of the inherit templates """

        def set_active(ids, active):
            if ids:
                real_ids = self.get_view_ids(ids)
                request.env['ir.ui.view'].with_context(active_test=True).browse(
                    real_ids).write({'active': active})

        set_active(disable, False)
        set_active(enable, True)

        if get_bundle:
            context = dict(request.context, active_test=True)
            return request.env["ir.qweb"]._get_asset('web.assets_backend',
                                                     options=context)

        return True

    @http.route(['/backend/theme_customize_reload'], type='http', auth="public",
                website=True)
    def theme_customize_reload(self, href, enable, disable):
        self.theme_customize(enable and enable.split(",") or [],
                             disable and disable.split(",") or [])
        return request.redirect(
            href + ("&theme=true" if "#" in href else "#theme=true"))

    @http.route(['/backend/multi_render'], type='json', auth="public",
                website=True)
    def multi_render(self, ids_or_xml_ids, values=None):
        View = request.env['ir.ui.view']
        res = {}
        for id_or_xml_id in ids_or_xml_ids:
            res[id_or_xml_id] = View.render_template(id_or_xml_id, values)
        return res
