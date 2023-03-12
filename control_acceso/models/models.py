# -*- coding: utf-8 -*-

from operator import is_not
from odoo import http
from odoo.http import request
from urllib.request import Request
from odoo.http import request
import json
from odoo import fields, api
from datetime import datetime
from email.policy import default
from logging import warning
import requests

from requests import request
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re
from datetime import datetime
from datetime import date, datetime, timedelta
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

    @api.onchange('name')
    def validarMateria(self):
        print("ingreso al validar curso")
        lista = self.env['controlacceso.materia'].search([])
        print("entro al validar materia")
        for i in range(len(lista)):
            print(self.name)
            print(lista[i].name)
            if lista[i].name == self.name:
                raise ValidationError('La materia con el nombre: '+ self.name+ ', ya esta registrada')

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
    estado = fields.Char('Estado de la puerta', required=True, default="cerrado")
    #estado_puerta = fields.Selection(
     #   selection=[("abierto", "abierto"), ("cerrado", "cerrado")],
      #  string="Estado puerta", required=True)
    
    
    def botonconfirm(self):
        p = self.env.context
        nombre = p.get('active_id')
        buscar = self.env['controlacceso.lab'].search([('name','=',nombre)]).update({'estado':"abierto"})
         
            
    @api.onchange('name')
    def validarLab(self):
        lista = self.env['controlacceso.lab'].search([])
        for i in range(len(lista)):
            print(lista[i].name)
            if lista[i].name == self.name:
                raise ValidationError('El nombre el laboratorio: '+self.name+' ya esta registrado')
        

    



class Horario(models.Model):
    _name = 'controlacceso.horario'
    hora_inicio = fields.Selection(
        selection=[("07:30", "07:30"), ("08:30", "08:30"), ("09:30", "09:30"),
                   ("10:30", "10:30"), ("11:30", "11:30"), ("12:30", "12:30"), ("16:30", "16:30")], string="Hora inicio", required=True)
    hora_fin = fields.Selection(
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

   
   

    @api.constrains('fecha')
    def contar(self):
        doc = self.docente_id
        buscarDoc =self.env['controlacceso.docente'].search([('id','=',doc.id)])
        contar =self.env['controlacceso.docente'].search_count([('id','=',doc.id)])
        print("si los cuento",contar)
        self.total_usuarios = contar
        
    @api.constrains('fecha')
    def RegistrardocenteCuenta(self):
        c = self.env.user.name
        correo= self.env['controlacceso.docente2'].search([('name','=',c)])
        print("id uasriooooooo",c)
        self.docente_id = correo.id
    """
    @api.constrains('fecha')
    def validate_date_practica(self):
        
        aux=None
        doc = self.env.user.login
        
        dia = (datetime.today().strftime('%A'))
        hora = ( datetime.today().strftime('%H'))
        horaActual = int(hora)-5
        min= ( datetime.today().strftime('%M')) 
        horaA = str(horaActual)+":"+str(min)
        
        listaHorario = self.env['controlacceso.horario2'].sudo().search([])
        for i in range(len(listaHorario)):
            d = self.docente_id
            c = self.env.user.name
            print("esta es la id",d)
            buscard= self.env['controlacceso.docente2'].sudo().search([('name','=',c)])
            print(buscard)
            buscarH=self.env['controlacceso.horario2'].sudo().search([('docente_id','=',buscard.id)])
        
            for j in range (len(buscarH)):
                if buscarH.lunes !=None and dia == 'lunes':
                    buscarM=self.env['controlacceso.materia'].search([('id','=',buscarH.lunes.id)])
                    print("Aqui da clases lunes", buscarM.name)
                    aux = buscarH[j]
                if buscarH.martes !=None and dia == 'lunes':
                    print("Aqui da clases martes", buscarH.martes)
                    aux = buscarH[j]
                if buscarH.martes !=None and dia == 'martes':
                    print("Aqui da clases martes", buscarH.martes)
                    aux = buscarH[j]
                if buscarH.miercoles !=None and dia == 'miercoles':
                    buscarM=self.env['controlacceso.materia'].search([('id','=',buscarH.lunes.id)])
                    print("Aqui da clases miercoles", buscarM.name)
                    aux = buscarH[j]
                if bool(buscarH.jueves) == True and dia == 'jueves':
                    print("Aqui da clases jueves", buscarH.martes)
                    aux = buscarH[j]
                if buscarH.viernes !=None and dia == 'viernes':
                    print("Aqui da clases viernes", buscarH.martes)
                    aux = buscarH[j]
        if aux == None:
            raise ValidationError('Se debe ingresar la practica dentro de su horario de clases')   



           # if str(dia) == str(listaHorario[i].dia):
            #    print('hay segundo match :v',listaHorario[i].dia)
             #   aux= listaHorario[i]
                
        
        #if aux is None:
         #   raise ValidationError('Se debe ingresar la practica dentro de su horario de clases')
    """




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
    curso_id = fields.Many2one(
        "controlacceso.curso", string="curso",
        default=lambda self: self.env['controlacceso.curso'].search([], limit=1),
        ondelete="cascade")
    name = fields.Many2one("res.users", string="Estudiante",
                               ondelete="cascade")
                               
    
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
                               


class Horario2(models.Model):
    _name = 'controlacceso.horario2'
    hora_inicio = fields.Selection(
        selection=[("07:30", "07:30"), ("08:30", "08:30"), ("09:30", "09:30"),
                   ("10:30", "10:30"), ("11:30", "11:30"), ("12:30", "12:30"), ("14:30", "14:30")], string="Hora inicio", required=True)
    hora_fin = fields.Selection(
        selection=[("08:30", "08:30"), ("09:30", "09:30"),
                   ("10:30", "10:30"), ("11:30", "11:30"), ("12:30", "12:30"),("13:30", "13:30"),("18:30", "18:30")], string="Hora fin", required=True)
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
        "controlacceso.lab", string="Laboratorio")
    carrera_id = fields.Many2one("controlacceso.carrera", string="Carrera",
                                 ondelete="cascade")
  
    curso_id = fields.Many2one("controlacceso.curso", string="Curso",
                               ondelete="cascade")
    docente_id = fields.Many2one("controlacceso.docente2", string="Docente",
                               ondelete="cascade")

    @api.onchange('lunes','martes','miercoles','jueves','viernes')
    def validarHorario(self):
        print(self.hora_inicio)
        print(self.hora_fin)
        print(self.laboratorio_id)
        lunes = None
        listaHorario = self.env['controlacceso.horario2'].sudo().search([])
        for record in self:
            for i in range(len(listaHorario)):
                if len(record.lunes) > 0:
                    for j in range(len(listaHorario[i].lunes)):
                        if record.hora_inicio >= listaHorario[i].hora_inicio and record.hora_inicio < listaHorario[i].hora_fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            print("hora inicio de los lunes",listaHorario[i].hora_inicio)
                            print("hora final de los lunes",listaHorario[i].hora_fin)
                            #print("laboraorio de los lunes",lista[i].laboratorio_id)
                            raise ValidationError('La hora inicio ingresada esta dentro de un horaro existente')
                        elif record.hora_fin > listaHorario[i].hora_inicio and record.hora_fin <= listaHorario[i].hora_fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            raise ValidationError('La hora fin ingresada esta dentro de un horaro existente')
                if len(record.martes) > 0:
                    for j in range(len(listaHorario[i].martes)):
                        if record.hora_inicio >= listaHorario[i].hora_inicio and record.hora_inicio < listaHorario[i].hora_fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            print("hora inicio de los lunes",listaHorario[i].hora_inicio)
                            print("hora final de los lunes",listaHorario[i].hora_fin)
                            #print("laboraorio de los lunes",lista[i].laboratorio_id)
                            raise ValidationError('La hora inicio ingresada esta dentro de un horaro existente')
                        elif record.hora_fin > listaHorario[i].hora_inicio and record.hora_fin <= listaHorario[i].hora_fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            raise ValidationError('La hora fin ingresada esta dentro de un horaro existente')
                if len(record.miercoles) > 0:
                    for j in range(len(listaHorario[i].miercoles)):
                        if record.hora_inicio >= listaHorario[i].hora_inicio and record.hora_inicio < listaHorario[i].hora_fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                           
                            raise ValidationError('La hora inicio ingresada esta dentro de un horaro existente')
                        elif record.hora_fin > listaHorario[i].hora_inicio and record.hora_fin <= listaHorario[i].hora_fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            raise ValidationError('La hora fin ingresada esta dentro de un horaro existente')
                if len(record.jueves) > 0:
                    for j in range(len(listaHorario[i].jueves)):
                        if record.hora_inicio >= listaHorario[i].hora_inicio and record.hora_inicio < listaHorario[i].hora_fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                           
                            raise ValidationError('La hora inicio ingresada esta dentro de un horaro existente')
                        elif record.hora_fin > listaHorario[i].hora_inicio and record.hora_fin <= listaHorario[i].hora_fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            raise ValidationError('La hora fin ingresada esta dentro de un horaro existente')
                if len(record.viernes) > 0:
                    for j in range(len(listaHorario[i].viernes)):
                        if record.hora_inicio >= listaHorario[i].hora_inicio and record.hora_inicio < listaHorario[i].hora_fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            
                            raise ValidationError('La hora inicio ingresada esta dentro de un horaro existente')
                        elif record.hora_fin > listaHorario[i].hora_inicio and record.hora_fin <= listaHorario[i].hora_fin and record.laboratorio_id == listaHorario[i].laboratorio_id:
                            raise ValidationError('La hora fin ingresada esta dentro de un horaro existente')
     

class registroAsistencia(models.Model):
    _name = 'controlacceso.registroasistencia'
    name = fields.Char('nombre usuario', required=True)
    hora_ingreso = fields.Char('Hora ingreso', required=True)
    fecha_ingreso = fields.Char('Fecha ingreso', required=True)
    temperatura = fields.Char('Temperatura', required=True)
    tarjeta = fields.Char('Tarjeta', required=True)
    curso_id= fields.Many2one("controlacceso.curso", string="Curso",
                               ondelete="cascade")
    materia_id= fields.Many2one("controlacceso.materia", string="Materia",
                               ondelete="cascade")
    lab_id= fields.Many2one("controlacceso.lab", string="Laboratorio",
                               ondelete="cascade")
    responsable= fields.Many2one("controlacceso.docente2", string="Laboratorio",
                               ondelete="cascade", required=False)
    ingreso_usuario = fields.Selection(
                    selection=[("Si", "Si"), ("No", "No")], string="Ingreso Usuario", required=True)
    



    
###################################3
#class res_users_ca(models.Model):
 #   _inherit = 'res.users'
  #  tarjeta = fields.Char('Tarjeta', required=True)
   # carrera_id = fields.Many2one(
    #    "controlacceso.carrera", string="Carrera",
     #   default=lambda self: self.env['controlacceso.carrera'].search([], limit=1),
      #  ondelete="cascade")
   # curso_id = fields.Many2one(
    #    "controlacceso.curso", string="curso",
     #   default=lambda self: self.env['controlacceso.curso'].search([], limit=1),
      #  ondelete="cascade", required=False)