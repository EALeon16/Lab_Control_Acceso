# -*- coding: utf-8 -*-

from operator import is_not
from odoo import http
from odoo.http import request
from urllib.request import Request
from odoo.http import request
import json
import pytz
from datetime import datetime, time
from pytz import timezone
import os

from odoo import fields, api
from datetime import datetime
from email.policy import default
from logging import warning
import requests
import datetime
from requests import request
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re
from odoo.addons.calendar.models.calendar_recurrence import weekday_to_field, RRULE_TYPE_SELECTION, END_TYPE_SELECTION, MONTH_BY_SELECTION, WEEKDAY_SELECTION, BYDAY_SELECTION
import ast
import json
from collections import defaultdict
from datetime import timedelta, datetime
from random import randint
import time


from odoo import api, Command, fields, models, tools, SUPERUSER_ID, _, _lt
from odoo.exceptions import UserError, ValidationError, AccessError
from odoo.tools import format_amount
from odoo.osv.expression import OR

#from .project_task_recurrence import DAYS, WEEKS
#from .project_update import STATUS_COLOR

count = None



class Carrera(models.Model):
    _name = 'controlacceso.carrera'
    _description = 'registro de carreras'
    name = fields.Char('Carrera', required=True)
    @api.onchange('name')
    def validarCarrera(self):
        lista = self.env['controlacceso.carrera'].search([])
        for i in range(len(lista)):
            if lista[i].name == self.name:
                raise ValidationError('La carrera con el nombre: '+ self.name+ ', ya esta registrada')

class Curso(models.Model):
    _name = 'controlacceso.curso'
    name = fields.Char('Nombre curso', required=True)
    carrera_id = fields.Many2one(
        "controlacceso.carrera", string="Carrera",
        default=lambda self: self.env['controlacceso.carrera'].search([], limit=1),
        ondelete="cascade")
    carrera =  fields.Char(related='carrera_id.name', string="Nombre Carrera",)
    
    @api.onchange('name')
    def validarCurso(self):
        print("ingreso al validar curso")
        listaCursos = self.env['controlacceso.curso'].search([])
        print("entro al validar curso")
        for i in range(len(listaCursos)):
            print(self.name)
            print(listaCursos[i].name)
            if listaCursos[i].name == self.name:
                raise ValidationError('El curso con el nombre: '+ self.name+ ', ya esta registrado')

class Materia(models.Model):
    _name = 'controlacceso.materia'
    name = fields.Char('Nombre materia', required=True)
    carrera_id = fields.Many2one(
        "controlacceso.carrera", string="Carrera",
        default=lambda self: self.env['controlacceso.carrera'].search([], limit=1),
        ondelete="cascade")

    #@api.onchange('name')
    #def validarMateria(self):
     #   print("ingreso al validar curso")
      #  lista = self.env['controlacceso.materia'].search([])
       # print("entro al validar materia")
        #for i in range(len(lista)):
         #   print(self.name)
          #  print(lista[i].name)
           # if lista[i].name == self.name:
            #    raise ValidationError('La materia con el nombre: '+ self.name+ ', ya esta registrada')

class Docente(models.Model):
    _name = 'controlacceso.docente'
    cedula = fields.Char('Cedula', required=True)
    name = fields.Char('Nombres y Apellidos', required=True)
    correo_docente = fields.Char('Correo', required=True)
    id_tarjeta = fields.Char('Tarjeta', required=True)
    carrera_id = fields.Many2one(
        "controlacceso.carrera", string="Carrera",
        default=lambda self: self.env['controlacceso.carrera'].search([], limit=1),
        ondelete="cascade")
   
    @api.onchange('correo_docente')
    def validate_mail(self):
        if self.correo_docente:
            match = re.match('.+@unl.edu\.ec', self.correo_docente)
            if match == None:
                raise ValidationError('Solo se aceptan direcciones de correo pertenecientes a @unl.edu.ec')


    #@api.onchange('name')
    #def crearUser(self):
     #   crear_user = self.env['res.users'].sudo().create({
      #                      'name':self.name,
        #                    'login':self.correo_docente,})
       # if crear_user:
         #   print("se creo el usuario")
                 

    #@api.onchange('id_tarjeta')
    #def validate_nrotarjeta(self):
    #    if self.id_tarjeta:
     #       match = re.match('/^([a-f0-9]{6}|[a-f0-9]{3})$/', self.correo_docente)
      #      if match == None:
       #         raise ValidationError('Ingrese formato correcto')

class Estudiante(models.Model):
    _name = 'controlacceso.estudiante'
    cedula = fields.Char('Cedula', required=True)
    name = fields.Char('Nombres y Apellidos', required=True)
    id_tarjeta = fields.Char('Tarjeta', required=True)
    carrera_id = fields.Many2one(
        "controlacceso.carrera", string="Carrera",
        default=lambda self: self.env['controlacceso.carrera'].search([], limit=1),
        ondelete="cascade")
    curso_id = fields.Many2one(
        "controlacceso.curso", string="curso",
        default=lambda self: self.env['controlacceso.curso'].search([], limit=1),
        ondelete="cascade")

class Laboratorio(models.Model):
    _name = 'controlacceso.lab'
    name = fields.Char('Numero de Laboratorio', required=True)
    nombre_lab = fields.Char('Nombre del Laboratorio', required=True)
    estado = fields.Char('Estado de la puerta', required=True, default="cerrado")
    
    
    
    def botonconfirm(self):
        p = self.env.context
        nombre = p.get('active_id')
        buscar = self.env['controlacceso.lab'].search([('name','=',nombre)]).update({'estado':"abierto"})
        #print("horaaaa", datetime.now().time())
        #current_time = datetime.now().time()
        #gmt_minus_5_time = utc_to_gmt_minus_5(current_time)

        #print("Hora UTC:", current_time.strftime("%H:%M:%S"))
        #print(gmt_minus_5_time)
        #print(gmt_minus_5_time > "09:30" and gmt_minus_5_time < "11:30")
        #aegunda prueba#
        utc_now = datetime.utcnow()

        local_tz = pytz.timezone('America/Bogota')

        local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(local_tz)

        day_of_week = local_now.strftime('%A') 

        date_str = local_now.strftime('%Y-%m-%d')  

        time_str = local_now.strftime('%H:%M')  
        print("esto se presenta",day_of_week,date_str,time_str)
    
        
 
        
         
            
    @api.onchange('name')
    def validarLab(self):
        lista = self.env['controlacceso.lab'].search([])
        for i in range(len(lista)):
            print(lista[i].name)
            if lista[i].name == self.name:
                raise ValidationError('El nombre el laboratorio: '+self.name+' ya esta registrado')
        
    @api.depends('nombre_lab')
    def name_get(self):
        result = []
        for record in self:
            name = record.nombre_lab
            result.append((record.id, name))
        return result
    



class Horario(models.Model):
    _name = 'controlacceso.horario'
    inicio = fields.Selection(
        selection=[("07:30", "07:30"), ("08:30", "08:30"), ("09:30", "09:30"),
                   ("10:30", "10:30"), ("11:30", "11:30"), ("12:30", "12:30"), ("16:30", "16:30")], string="Hora inicio", required=True)
    fin = fields.Selection(
        selection=[("08:30", "08:30"), ("09:30", "09:30"),
                   ("10:30", "10:30"), ("11:30", "11:30"), ("12:30", "12:30"),("13:30", "13:30"),("18:30", "18:30")], string="Hora fin", required=True)
    dia = fields.Selection(
        selection=[("lunes", "lunes"), ("martes", "martes"), ("miercoles", "miercoles"),
                   ("jueves", "jueves"), ("viernes", "viernes")], string="Dia", required=True)
    
    laboratorio_id = fields.Many2one(
        "controlacceso.lab", string="Laboratorio")
    carrera_id = fields.Many2one("controlacceso.carrera", string="Carrera",
                                 ondelete="cascade")
    materia_id = fields.Many2one("controlacceso.materia", string="Materia",
                                 ondelete="cascade")
    curso_id = fields.Many2one("controlacceso.curso", string="Curso",
                               ondelete="cascade")
    docente_id = fields.Many2one("controlacceso.docente", string="Docente",
                               ondelete="cascade")
    

 

    

   
class Practicas(models.Model):
    


    _name = 'controlacceso.practica'
    name = fields.Char('Tema de la practica', required=True, default="Uso diario")
    total_usuarios = fields.Integer('Numero usuarios')
    fecha = fields.Char('Fecha', required=True, default=datetime.today().strftime('%Y-%m-%d'))
    docente_id = fields.Many2one(
        "controlacceso.docente2", string="Docente Responsable",
        default=lambda self: self.env['controlacceso.docente2'].search([], limit=1),
        ondelete="cascade")
    lab_id = fields.Many2one(
        "controlacceso.lab", string="Laboratorio",
        default=lambda self: self.env['controlacceso.lab'].search([], limit=1),
        ondelete="cascade")
    curso_id = fields.Many2one("controlacceso.curso", string="Curso",
                               ondelete="cascade")
    materia_id = fields.Many2one("controlacceso.materia", string="Materia",
                               ondelete="cascade")
    descripcion = fields.Html('Descripcion', required=True)
    resultados_practicas_ids = fields.One2many('controlacceso.resultados_practicas', 'practica_id', string='Resultados de prácticas')
    periodo_id = fields.Many2one("controlacceso.periodoacademico", string="Periodo Academico",required=True,
                               ondelete="cascade")
    @api.depends('name')
    def _compute_current_user(self):
        for record in self:
            current_user = self.env.user
            usuario_estudiante = self.env['controlacceso.usuarioestudiante'].search([('name', '=', current_user.id)], limit=1)
            record.estudiantes_ids = self.env['controlacceso.usuarioestudiante'].search([('curso_id', '=', usuario_estudiante.curso_id.id)])
    
    estudiantes_ids = fields.Many2many('controlacceso.usuarioestudiante', compute='_compute_current_user')
    


   
   

    @api.model
    def create(self, vals):
        docente = self.env['controlacceso.docente2'].search([('name', '=', self.env.user.name)], limit=1)
        vals['docente_id'] = docente.id
        return super(Practicas, self).create(vals)

    @api.constrains('fecha')
    def _check_fecha(self):
        for record in self:
            # Definir una expresión regular para validar el formato de la fecha
            fecha_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
            # Validar que la fecha ingresada cumpla con el formato deseado
            if not fecha_regex.match(record.fecha):
                raise ValidationError("La fecha debe tener el formato 'YYYY-MM-DD'.")
   



class UsuarioDocente(models.Model):
    _name = 'controlacceso.docente2'
    tarjeta = fields.Char('Nro. de tarjeta', required=True)
    carrera_id = fields.Many2one("controlacceso.carrera", string="Carrera",
                               ondelete="cascade")
    name = fields.Many2one("res.users", string="Docente",
                               ondelete="cascade")
    
    @api.onchange('tarjeta')
    def validarTarjetaDocente(self):
        print("ingreso al valiar tarjeta docente")
        listaestudiantes = self.env['controlacceso.usuarioestudiante'].sudo().search([])
        listadocente = self.env['controlacceso.docente2'].sudo().search([])
        for i in range(len(listaestudiantes)):
            if listaestudiantes[i].tarjeta == self.tarjeta:
                nombre = self.env['res.users'].sudo().search([('id','=',listaestudiantes[i].name.id)])
                print(nombre.name)
                raise ValidationError('Este numero de tarjeta ya esta registrado con el estudiante: '+nombre.name)
        for i in range(len(listadocente)):
            if listadocente[i].tarjeta == self.tarjeta:
                nombre = self.env['res.users'].sudo().search([('id','=',listadocente[i].name.id)])
                print(nombre.name)
                raise ValidationError('Este numero de tarjeta ya esta registrado con el docente: '+nombre.name)
    

class UsuarioEstudiante(models.Model):
    _name = 'controlacceso.usuarioestudiante'
    tarjeta = fields.Char('Tarjeta', required=True)
    carrera_id = fields.Many2one(
        "controlacceso.carrera", string="Carrera",
        default=lambda self: self.env['controlacceso.carrera'].search([], limit=1),
        ondelete="cascade")
    curso_id = fields.Many2many(
    "controlacceso.curso", string="Cursos",
    ondelete="cascade")
    name = fields.Many2one("res.users", string="Estudiante",
                               ondelete="cascade")
    cursos_asignados = fields.Char(compute="_compute_cursos_asignados", string="Cursos asignados")

    
    @api.onchange('tarjeta')
    def validarTarjeta(self):
        listaestudiantes = self.env['controlacceso.usuarioestudiante'].sudo().search([])
        listadocente = self.env['controlacceso.docente2'].sudo().search([])
        for i in range(len(listaestudiantes)):
            if listaestudiantes[i].tarjeta == self.tarjeta:
                nombre = self.env['res.users'].sudo().search([('id','=',listaestudiantes[i].name.id)])
                print(nombre.name)
                raise ValidationError('Este numero de tarjeta ya esta registrado con el estudiante: '+nombre.name)
        for i in range(len(listadocente)):
            if listadocente[i].tarjeta == self.tarjeta:
                nombre = self.env['res.users'].sudo().search([('id','=',listadocente[i].name.id)])
                print(nombre.name)
                raise ValidationError('Este numero de tarjeta ya esta registrado con el docente: '+nombre.name)
                               

    @api.depends('curso_id')
    def _compute_cursos_asignados(self):
        for record in self:
            cursos = record.curso_id.mapped('name')
            record.cursos_asignados = ", ".join(cursos)

class Horario2(models.Model):
    _name = 'controlacceso.horario2'
    inicio = fields.Char('Hora inicio', required=True)
    fin = fields.Char('Hora fin', required=True)
    lunes = fields.Many2one("controlacceso.materia", required=False, string="Lunes",
                                 ondelete="cascade")
    martes = fields.Many2one("controlacceso.materia", required=False, string="Martes",
                                 ondelete="cascade")
    miercoles = fields.Many2one("controlacceso.materia", required=False, string="Miercoles",
                                 ondelete="cascade")
    jueves = fields.Many2one("controlacceso.materia", required=False, string="Jueves",
                                 ondelete="cascade")
    viernes = fields.Many2one("controlacceso.materia", required=False, string="Viernes",
                                 ondelete="cascade")
    laboratorio_id = fields.Many2one(
        "controlacceso.lab", string="Laboratorio", required=True)
    carrera_id = fields.Many2one("controlacceso.carrera", string="Carrera",
                                 ondelete="cascade",required=True)
  
    curso_id = fields.Many2one("controlacceso.curso", string="Curso",
                               ondelete="cascade", required=True)
    docente_id = fields.Many2one("controlacceso.docente2", string="Docente",
                               ondelete="cascade", required=True)
    periodo_id = fields.Many2one("controlacceso.periodoacademico", string="Periodo Academico",required=True,
                               ondelete="cascade")
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args += [('periodo_id', '!=', False)]
        return super(Horario2, self).search(args, offset=offset, limit=limit, order=order, count=count)

    
    
    """
    @api.onchange('lunes','martes','miercoles','jueves','viernes')
    def validarHorario(self):
        print(self.inicio)
        print(self.fin)
        print(self.laboratorio_id)
        lunes = None
        listaHorario = self.env['controlacceso.horario2'].sudo().search([])
        for record in self:
            for i in range(len(listaHorario)):
                if len(record.lunes) > 0:
                    for j in range(len(listaHorario[i].lunes)):
                        if record.inicio >= listaHorario[i].inicio and record.inicio < listaHorario[i].fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            print("hora inicio de los lunes",listaHorario[i].inicio)
                            print("hora final de los lunes",listaHorario[i].fin)
                            #print("laboraorio de los lunes",lista[i].laboratorio_id)
                            raise ValidationError('La hora inicio ingresada esta dentro de un horaro existente')
                        elif record.fin > listaHorario[i].inicio and record.fin <= listaHorario[i].fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            raise ValidationError('La hora fin ingresada esta dentro de un horaro existente')
                if len(record.martes) > 0:
                    for j in range(len(listaHorario[i].martes)):
                        if record.inicio >= listaHorario[i].inicio and record.inicio < listaHorario[i].fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            print("hora inicio de los lunes",listaHorario[i].inicio)
                            print("hora final de los lunes",listaHorario[i].fin)
                            #print("laboraorio de los lunes",lista[i].laboratorio_id)
                            raise ValidationError('La hora inicio ingresada esta dentro de un horaro existente')
                        elif record.fin > listaHorario[i].inicio and record.fin <= listaHorario[i].fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            raise ValidationError('La hora fin ingresada esta dentro de un horaro existente')
                if len(record.miercoles) > 0:
                    for j in range(len(listaHorario[i].miercoles)):
                        if record.inicio >= listaHorario[i].inicio and record.inicio < listaHorario[i].fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                           
                            raise ValidationError('La hora inicio ingresada esta dentro de un horaro existente')
                        elif record.fin > listaHorario[i].inicio and record.fin <= listaHorario[i].fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            raise ValidationError('La hora fin ingresada esta dentro de un horaro existente')
                if len(record.jueves) > 0:
                    for j in range(len(listaHorario[i].jueves)):
                        if record.inicio >= listaHorario[i].inicio and record.inicio < listaHorario[i].fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                           
                            raise ValidationError('La hora inicio ingresada esta dentro de un horaro existente')
                        elif record.fin > listaHorario[i].inicio and record.fin <= listaHorario[i].fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            raise ValidationError('La hora fin ingresada esta dentro de un horaro existente')
                if len(record.viernes) > 0:
                    for j in range(len(listaHorario[i].viernes)):
                        if record.inicio >= listaHorario[i].inicio and record.inicio < listaHorario[i].fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            
                            raise ValidationError('La hora inicio ingresada esta dentro de un horaro existente')
                        elif record.fin > listaHorario[i].inicio and record.fin <= listaHorario[i].fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            raise ValidationError('La hora fin ingresada esta dentro de un horaro existente')
    """

    @api.constrains('inicio', 'fin')
    def validar_horas(self):
        hora_inicio = self.inicio
        hora_fin = self.fin
        
        # Verificar si las cadenas tienen el formato correcto (HH:MM)
        if not re.match(r'^\d{2}:\d{2}$', hora_inicio):
            raise ValidationError("El formato de hora en el campo 'inicio' debe ser HH:MM con dos dígitos en la hora")
        if not re.match(r'^\d{2}:\d{2}$', hora_fin):
            raise ValidationError("El formato de hora en el campo 'fin' debe ser HH:MM con dos dígitos en la hora")

        # Extraer las horas y minutos del campo 'inicio'
        hora, minutos = hora_inicio.split(':')
        hora = int(hora)
        minutos = int(minutos)
        
        # Verificar si la hora y los minutos son válidos para el campo 'inicio'
        if hora < 0 or hora > 23:
            raise ValidationError("La hora en el campo 'inicio' debe estar entre 0 y 23")
        if minutos < 0 or minutos > 59:
            raise ValidationError("Los minutos en el campo 'inicio' deben estar entre 0 y 59")
        
        # Extraer las horas y minutos del campo 'fin'
        hora, minutos = hora_fin.split(':')
        hora = int(hora)
        minutos = int(minutos)
        
        # Verificar si la hora y los minutos son válidos para el campo 'fin'
        if hora < 0 or hora > 23:
            raise ValidationError("La hora en el campo 'fin' debe estar entre 0 y 23")
        if minutos < 0 or minutos > 59:
            raise ValidationError("Los minutos en el campo 'fin' deben estar entre 0 y 59")
        
        # Verificar si la hora de inicio es anterior a la hora de fin
        if hora_inicio >= hora_fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin")
        
        # Si todo está bien, devolver True
        return True

class registroAsistencia(models.Model):
    _name = 'controlacceso.registroasistencia'
    name = fields.Char('Nombre de usuario', required=True)
    hora_ingreso = fields.Char('Hora ingreso', required=True)
    fecha_ingreso = fields.Char('Fecha ingreso', required=True)
    temperatura = fields.Char('Temperatura', required=True)
    tarjeta = fields.Char('Tarjeta', required=True)
    curso_id= fields.Many2one("controlacceso.curso", string="Curso",
                               ondelete="cascade",required=False)
    materia_id= fields.Many2one("controlacceso.materia", string="Materia",
                               ondelete="cascade",required=False)
    lab_id= fields.Many2one("controlacceso.lab", string="Laboratorio",
                               ondelete="cascade",required=False)
    responsable= fields.Many2one("controlacceso.docente2", string="Responsable",
                               ondelete="cascade", required=False)
    ingreso_usuario = fields.Selection(
                    selection=[("Si", "Si"), ("No", "No")], string="Ingreso Usuario", required=True)
    



class UsuarioAdministrador(models.Model):
    _name = 'controlacceso.administrador'
    tarjeta = fields.Char('Nro. de tarjeta', required=True)
    name = fields.Many2one("res.users", string="Administrador",
                               ondelete="cascade")
    
class registroIntentoAsistencia(models.Model):
    _name = 'controlacceso.registrointentoasistencia'
    name = fields.Char('Nombre usuario', required=True)
    hora_ingreso = fields.Char('Hora intento de ingreso', required=True)
    fecha_ingreso = fields.Char('Fecha intento de ingreso', required=True)
    tarjeta = fields.Char('Tarjeta', required=True)
    lab_id= fields.Many2one("controlacceso.lab", string="Laboratorio",
                               ondelete="cascade",required=False)

class PeriodoAcademico(models.Model):
    _name = 'controlacceso.periodoacademico'
    name = fields.Char(string='Nombre', required=True)
    fecha_inicio = fields.Date(string='Fecha Inicio', required=True)
    fecha_fin = fields.Date(string='Fecha Fin', required=True)
    estado = fields.Boolean(string='Activo')
    horario_ids = fields.One2many('controlacceso.horario2', 'periodo_id', string='Horario')
    @api.constrains('name')
    def contarP(self):
        periodos = self.env['controlacceso.periodoacademico'].search([('estado', '=', True)])

        for periodo in periodos:
            print("nombres periodos",periodo.estado)
    #####actualizar automaticamente
    @api.model
    def actualizar_estado(self):
        fecha_actual = fields.Date.today()
        print(fecha_actual)
        periodos = self.search([])
        for periodo in periodos:
            if periodo.fecha_inicio <= fecha_actual <= periodo.fecha_fin:
                periodo.estado = True
            else:
                periodo.estado = False
class ResUsers(models.Model):
    _inherit = 'res.users'

    estudiante_curso_ids = fields.One2many(
        'controlacceso.usuarioestudiante', 'name', string="Cursos del estudiante",
        domain="[('name', '=', name)]")
    
    
    @api.model
    def create(self, vals):
        if vals.get('name') == 'Administrador':
            vals['groups_id'] = [(6, 0, [])]
        return super(ResUsers, self).create(vals)
        
    
class ResultadosPracticas(models.Model):
    _name = 'controlacceso.resultados_practicas'
    name = fields.Html('Resultados practicas', required=True)
    estado = fields.Selection([
        ('inicial', 'Inicial'),
        ('desarrollando', 'Desarrollando'),
        ('finalizado','Finalizado'),
    ], string='Estado',default='inicial')
    archivo = fields.Binary('Archivo', groups="control_acceso.res_groups_docentes,control_acceso.res_groups_alumnos,control_acceso.res_groups_administrador")
    estudiante_id = fields.Many2one('controlacceso.usuarioestudiante', string='Estudiante')
    practica_id = fields.Many2one('controlacceso.practica', string='Práctica')
    periodo_id = fields.Many2one("controlacceso.periodoacademico", string="Periodo Academico",required=True,
                               ondelete="cascade")
    materia_id = fields.Many2one("controlacceso.materia", string="Materia",
                               ondelete="cascade")
    @api.constrains('name')
    def RegistrarCuenta(self):
        c = self.env.user.name
        correo= self.env['controlacceso.usuarioestudiante'].search([('name','=',c)])
        print("id uasriooooooo",c)
        self.estudiante_id = correo.id
    @api.constrains('name')
    def validarRegistroPractica(self):
        aux = None
        lunes = None 
        martes = None 
        miercoles = None 
        jueves = None 
        viernes = None 
        utc_now = datetime.utcnow()

        local_tz = pytz.timezone('America/Bogota')

        local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(local_tz)

        day_of_week = local_now.strftime('%A') 

        date_str = local_now.strftime('%Y-%m-%d')  

        time_str = local_now.strftime('%H:%M')  
        user = self.env.user.name
        estudiante= self.env['controlacceso.usuarioestudiante'].search([('name','=',user)])
        for c in estudiante.curso_id:
            print("entro al primer for", c)
            c2 = self.env['controlacceso.curso'].sudo().search([('id','=',c.id)])
            print("primer for",c2.name)
            buscarH = self.env['controlacceso.horario2'].sudo().search([('curso_id','=',c.id)])
                        
            if buscarH:
                print("horario primer for",buscarH)
                aux = buscarH
                                
                                
                for i in range (len(aux)):
                    print("entro al for")
                    if aux[i].lunes and day_of_week == 'lunes':
                        print("entro al lunes for")
                        lunes = aux[i]
                    if aux[i].martes and day_of_week == 'martes':
                        martes = aux[i]
                    if aux[i].miercoles and day_of_week == 'miércoles':
                        miercoles = aux[i]
                    if aux[i].jueves and day_of_week == 'jueves':
                        jueves = aux[i]
                    if aux[i].viernes and day_of_week == 'viernes':
                        viernes = aux[i]
                print("antes if despues for")
                if lunes != None and time_str >= lunes.inicio and time_str <= lunes.fin :
                    print("entro al if despues del for")
                    return 
                if martes != None and time_str >= martes.inicio and time_str <= martes.fin :
                                    
                    return 
                if miercoles != None and time_str >= miercoles.inicio and time_str <= miercoles.fin:
                                    
                    return 
                if jueves != None and time_str >= jueves.inicio and time_str <= jueves.fin :
                                    
                    return 
                if viernes != None and time_str >= viernes.inicio and time_str <= viernes.fin :
                        
                    return 
                else:
                    print("esta ingresando la practic en horario fuera del asignado")
                    raise ValidationError("No puede asignar resultados de las practicas en horas fuera del horario")

        print("ingreso al validar registro practica", estudiante)
    @api.model
    def create(self, vals):
        periodo = self.env['controlacceso.periodoacademico'].search([('estado', '=', True)], limit=1)
        vals['periodo_id'] = periodo.id
        return super(ResultadosPracticas, self).create(vals)
    @api.onchange('practica_id')
    def validarMateria(self):
        print("esto presenta",self.practica_id)
        if self.practica_id:
            self.materia_id = self.practica_id.materia_id
def utc_to_gmt_minus_5(time):
    # GMT-5 es 5 horas hacia atrás de UTC
    gmt_minus_5_offset = -5
    
    # Convertir el objeto time a segundos
    time_in_seconds = time.hour * 3600 + time.minute * 60 + time.second
    
    # Calcular la hora en GMT-5
    gmt_minus_5_time_in_seconds = (time_in_seconds + gmt_minus_5_offset * 3600) % 86400
    
    # Convertir la hora GMT-5 en segundos a objeto time
    gmt_minus_5_hour = gmt_minus_5_time_in_seconds // 3600
    gmt_minus_5_minute = (gmt_minus_5_time_in_seconds % 3600) // 60
    gmt_minus_5_second = gmt_minus_5_time_in_seconds % 60
    
    return time.replace(hour=gmt_minus_5_hour, minute=gmt_minus_5_minute, second=gmt_minus_5_second).strftime("%H:%M")