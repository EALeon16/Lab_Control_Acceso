# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from urllib.request import Request
from odoo.http import request
import json
from odoo import fields, api
from datetime import datetime
import requests









class ApiController(http.Controller):
    
    @http.route('/api/dost/', methods=['post'], auth='public', csrf=False)
    def create_order(self, **kwargs):
        aux = None
        lunes = None 
        martes = None 
        miercoles = None 
        jueves = None 
        viernes = None 
        datos = kwargs
        try:
            print("entro al try")
            docente = request.env['controlacceso.docente2'].sudo().search([('tarjeta','=',datos['pass'])])
            print("docente encontrado",docente.name)
            
            hora = ( datetime.today().strftime('%H'))
            horaActual = int(hora)-5
            #dia = (datetime.today().strftime('%A'))
            dia = 'lunes'
            min= ( datetime.today().strftime('%M')) 
            if horaActual >= 10:
                horaA = str(horaActual)+":"+str(min)
            else:
                horaA = "0"+str(horaActual)+":"+str(min)
            
            temp = datos["Temperatura"]
            print("ẗemperatura", temp)
            lab = datos["lab"]
            nroT = datos["pass"]
            
            laboratorio = request.env['controlacceso.lab'].sudo().search([('name','=',lab)])
            estudiante = request.env['controlacceso.usuarioestudiante'].sudo().search([('tarjeta','=',datos['pass'])])
            print(len(estudiante) > 0)
            curso = request.env['controlacceso.curso'].sudo().search([('id','=',estudiante.curso_id.id)])
            m = request.env['controlacceso.materia'].sudo().search([('id','=',16)])
            if len(estudiante) > 0:
                nombre = request.env['res.users'].sudo().search([('id','=',estudiante.name.id)])
                buscarH = request.env['controlacceso.horario2'].sudo().search([('curso_id','=',estudiante.curso_id.id)])
            #print("estos veces esta el curso en el horario", buscarH.curso_id)
                aux = buscarH
                    #print("aqui esta el curso del estudiante", aux.curso_id)
                for i in range (len(aux)):
                    if aux[i].lunes and dia == 'lunes':
                        lunes = aux[i]
                    if aux[i].martes and dia == 'martes':
                        martes = aux[i]
                    if aux[i].miercoles and dia == 'miércoles':
                        miercoles = aux[i]
                    if aux[i].jueves and dia == 'jueves':
                        jueves = aux[i]
                    if aux[i].viernes and dia == 'viernes':
                        viernes = aux[i]
                if lunes != None and horaA >= lunes.hora_inicio and horaA <= lunes.hora_fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',lunes.lunes.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('lunes','=',m.id)])
                    print("buscar en el horario", buscar.docente_id)
                    buscarDocente = request.env['controlacceso.docente2'].sudo().search([('id','=',buscar.docente_id.id)])
                    print("buscar donde", buscarDocente.id)
                    print("buscar donde", buscarDocente.name)
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombre.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'responsable':buscarDocente.id,
                                        'curso_id':curso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"Si",
                                        'lab_id':laboratorio.id,})
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombre.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':curso.id,
                                        'responsable':buscarDocente.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})

                    print('creado')
                    return nombre.name
                if martes != None and horaA >= martes.hora_inicio and horaA <= martes.hora_fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',martes.martes.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('martes','=',m.id)])
                    buscarDocente = request.env['controlacceso.docente2'].sudo().search([('id','=',buscar.docente_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombre.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':curso.id,
                                        'ingreso_usuario':"Si",
                                        'materia_id':m.id,
                                        'responsable':buscarDocente.id,
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombre.name
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombre.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':curso.id,
                                        'responsable':buscarDocente.id,
                                        'ingreso_usuario':"No",
                                        'materia_id':m.id,
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombre.name
                if miercoles != None and horaA >= miercoles.hora_inicio and horaA <= miercoles.hora_fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',miercoles.miercoles.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('miercoles','=',m.id)])
                    buscarDocente = request.env['controlacceso.docente2'].sudo().search([('id','=',buscar.docente_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombre.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':curso.id,
                                        'responsable':buscarDocente.id,
                                        'ingreso_usuario':"Si",
                                        'materia_id':m.id,
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombre.name
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombre.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':curso.id,
                                        'ingreso_usuario':"No",
                                        'responsable':buscarDocente.id,
                                        'materia_id':m.id,
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombre.name
                if jueves != None and horaA >= jueves.hora_inicio and horaA <= jueves.hora_fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',jueves.jueves.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('jueves','=',m.id)])
                    buscarDocente = request.env['controlacceso.docente2'].sudo().search([('id','=',buscar.docente_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombre.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':curso.id,
                                        'responsable':buscarDocente.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"Si",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombre.name
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombre.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':curso.id,
                                        'responsable':buscarDocente.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombre.name
                if viernes != None and horaA >= viernes.hora_inicio and horaA <= viernes.hora_fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',viernes.viernes.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('viernes','=',m.id)])
                    buscarDocente = request.env['controlacceso.docente2'].sudo().search([('id','=',buscar.docente_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombre.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':curso.id,
                                        'materia_id':m.id,
                                        'responsable':buscarDocente.id,
                                        'ingreso_usuario':"Si",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombre.name
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombre.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':curso.id,
                                        'materia_id':m.id,
                                        'responsable':buscarDocente.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombre.name
###################################################################################################################
            elif len(docente) > 0:
                nombreDocente = request.env['res.users'].sudo().search([('id','=',docente.name.id)])
                print("este es el nombre", nombreDocente.name)
                buscarH = request.env['controlacceso.horario2'].sudo().search([('docente_id','=',docente.id)])
                    #print("estos veces esta el curso en el horario", buscarH.curso_id)
                aux = buscarH
                    #print("aqui esta el curso del estudiante", aux.curso_id)
                for i in range (len(aux)):
                    if aux[i].lunes and dia == 'lunes':
                        lunes = aux[i]
                    if aux[i].martes and dia == 'martes':
                        martes = aux[i]
                    if aux[i].miercoles and dia == 'miércoles':
                        miercoles = aux[i]
                    if aux[i].jueves and dia == 'jueves':
                        jueves = aux[i]
                    if aux[i].viernes and dia == 'viernes':
                        viernes = aux[i]
                if lunes != None:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',lunes.lunes.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('lunes','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"Si",
                                        'lab_id':laboratorio.id,})
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})

                    print('creado')
                    return nombreDocente.name
                if martes != None and horaA >= martes.hora_inicio and horaA <= martes.hora_fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',martes.martes.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('martes','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"Si",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name
                if miercoles != None and horaA >= miercoles.hora_inicio and horaA <= miercoles.hora_fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',miercoles.miercoles.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('miercoles','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':'36',
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"Si",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':'36',
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name

                if jueves != None and horaA >= jueves.hora_inicio and horaA <= jueves.hora_fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',jueves.jueves.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('jueves','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':'36',
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"Si",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':'36',
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name

                if viernes != None:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',viernes.viernes.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('viernes','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"Si",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name 
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':horaA,
                                        'fecha_ingreso':datetime.today().strftime('%Y-%m-%d'),
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name

        except:
            print("entro al catch")
            print(datos['pass'])
            aux = None
            lunes = None 
            martes = None 
            miercoles = None 
            jueves = None 
            viernes = None 
            hora = ( datetime.today().strftime('%H'))
            horaActual = int(hora)-5
            #dia = (datetime.today().strftime('%A'))
            dia='lunes'
            min= ( datetime.today().strftime('%M')) 
            if horaActual >= 10:
                horaA = str(horaActual)+":"+str(min)
            else:
                horaA = "0"+str(horaActual)+":"+str(min)
            
            estudiante = request.env['controlacceso.usuarioestudiante'].sudo().search([('tarjeta','=',datos['pass'])])
            docente = request.env['controlacceso.docente2'].sudo().search([('tarjeta','=',datos['pass'])])
            
            laboratorio = request.env['controlacceso.lab'].sudo().search([('name','=',datos['pass'])])
            
            
            if len(estudiante) > 0:
                print("esete es el curso del estudiante",estudiante.curso_id)
                curso = request.env['controlacceso.curso'].sudo().search([('id','=',estudiante.curso_id.id)])
                carrera = request.env['controlacceso.carrera'].sudo().search([('id','=',curso.id)])
                materia = request.env['controlacceso.materia'].sudo().search([('carrera_id','=',carrera.id)])
                buscarH = request.env['controlacceso.horario2'].sudo().search([('curso_id','=',estudiante.curso_id.id)])
                print(buscarH)
                aux = buscarH
                
                
                for i in range (len(aux)):
                    if aux[i].lunes and dia == 'lunes':
                        lunes = aux[i]
                    if aux[i].martes and dia == 'martes':
                        martes = aux[i]
                    if aux[i].miercoles and dia == 'miércoles':
                        miercoles = aux[i]
                    if aux[i].jueves and dia == 'jueves':
                        jueves = aux[i]
                    if aux[i].viernes and dia == 'viernes':
                        viernes = aux[i]
                if lunes != None and horaA >= lunes.hora_inicio and horaA <= lunes.hora_fin:
                    
                    return "registrar temperatura"
                if martes != None and horaA >= martes.hora_inicio and horaA <= martes.hora_fin:
                    
                    return "registrar temperatura"
                if miercoles != None and horaA >= miercoles.hora_inicio and horaA <= miercoles.hora_fin:
                    
                    return "registrar temperatura"
                if jueves != None and horaA >= jueves.hora_inicio and horaA <= jueves.hora_fin:
                    
                    return "registrar temperatura"
                if viernes != None and horaA >= viernes.hora_inicio and horaA <= viernes.hora_fin:
                    
                    return "registrar temperatura"
                else:
                    return "no registrar temperatura"
                
            if len(docente) > 0:
                print("encontro al docente", docente)
                buscarH = request.env['controlacceso.horario2'].sudo().search([('docente_id','=',docente.id)])
                print("estos veces el docente da clase en la semana", buscarH.curso_id)
                aux = buscarH
                    #print("aqui esta el curso del estudiante", aux.curso_id)
                for i in range (len(aux)):
                    if aux[i].lunes and dia == 'lunes':
                        lunes = aux[i]
                    if aux[i].martes and dia == 'martes':
                        martes = aux[i]
                    if aux[i].miercoles and dia == 'miércoles':
                        miercoles = aux[i]
                    if aux[i].jueves and dia == 'jueves':
                        jueves = aux[i]
                    if aux[i].viernes and dia == 'viernes':
                        viernes = aux[i]
                if lunes != None and horaA >= lunes.hora_inicio and horaA <= lunes.hora_fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',lunes.lunes.id)])
                    return "registrar temperatura"
                if martes != None and horaA >= martes.hora_inicio and horaA <= martes.hora_fin:
                    return "registrar temperatura"
                if miercoles != None and horaA >= miercoles.hora_inicio and horaA <= miercoles.hora_fin:
                    return "registrar temperatura"
                if jueves != None and horaA >= jueves.hora_inicio and horaA <= jueves.hora_fin:
                    return "registrar temperatura"
                if viernes != None and horaA >= viernes.hora_inicio and horaA <= viernes.hora_fin:
                    return "registrar temperatura"
                
                else:
                    return "no registrar temperatura" 
                
            if datos['pass'] == "24 93 77 28":
                    return "administrador"   
                    
            else:
                return "no registrar temperatura"

            

    
    @http.route('/api/dost/abrirPuerta', methods=['get','post'], auth='public', csrf=False)
    def abrirPuerts(self, **kwargs):  
        
        datos = kwargs
        lab = datos["lab"]
        estado = datos["estado"]
        buscarLab = request.env['controlacceso.lab'].sudo().search([('name','=',lab)])
        print(buscarLab.estado)
        print(lab,estado)
        if buscarLab.estado == "abierto":
            request.env['controlacceso.lab'].sudo().search([('name','=',lab)]).sudo().update({'estado':"cerrado"})
            return "abrir puerta"
        else:
            return "no abrir"
        
    
        

        
    
    
        

    



