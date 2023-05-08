from reportlab.pdfbase.pdfutils import _fusc

from odoo import models, api
from datetime import datetime

class SolicitudMatricula(models.AbstractModel):
    _name = "report.control_acceso_registroasistencia.report_registroasistencia"

    @api.model
    def _get_report_values(self, docids, data=None):
        print("ingresa despues de la funcion")
        docs = self.env["controlacceso.registroasistencia"].browse(docids)
        docargs = {
            "docs": docs,
        }
        return docargs


class ReportePracticas(models.AbstractModel):
    print("ingresa despues de la clase")
    _name = "reporte_practica.control_acceso_practicas.report_practica"
    print("ingresa despues del _name")
    @api.model
    def _get_report_values(self, docids, data=None):
        print("ingresa despues de la funcion")
        docs = self.env["controlacceso.practica"].browse(docids)
        docente = self.env['res.users'].sudo().search([('id','=',docs.name.id)])
        asistencia = self.env["controlacceso.registroasistencia"].sudo().search(['fecha_ingreso','=',docs.fecha])
        docargs = {
            "docs": docs,
            "a": asistencia,
            "docente":docente
        }
        print("creand registro practicas", docs.name)
        return docargs

class GenerarHorario(models.AbstractModel):
    _name = "horario.control_acceso_horario2.report_horario"

    @api.model
    def _get_report_values(self, docids, data=None):
        print("ingresa despues de la funcion")
        docs = self.env["controlacceso.horario2"].browse(docids)
        lab = self.env['controlacceso.lab'].sudo().search([])
        docargs = {
            "docs": docs,
            "lab":lab,
        }
        return docargs
    

class ReporteIntentoIngreso(models.AbstractModel):
    _name = "report.control_acceso_registrointentoasistencia.report_registrointentoasistencia"

    @api.model
    def _get_report_values(self, docids, data=None):
        print("ingresa despues de la funcion")
        docs = self.env["controlacceso.registrointentoasistencia"].browse(docids)
        docargs = {
            "docs": docs,
        }
        return docargs