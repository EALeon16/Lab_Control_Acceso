# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from urllib.request import Request
from odoo.http import request
import json
from odoo import fields, api
from datetime import datetime
import pytz
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
            admin = request.env['controlacceso.administrador'].sudo().search([('tarjeta','=',datos['pass'])])
            hora2 = ( datetime.today().strftime('%H'))
            horaActual2 = int(hora2)-5
            dia2 = (datetime.today().strftime('%A'))
            
            min2= ( datetime.today().strftime('%M')) 
            #########pztz$####################
            utc_now = datetime.utcnow()

            local_tz = pytz.timezone('America/Bogota')

            local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(local_tz)

            day_of_week = local_now.strftime('%A') 

            date_str = local_now.strftime('%Y-%m-%d')  

            time_str = local_now.strftime('%H:%M')  
            print("esto se presenta",day_of_week,date_str,time_str)
            ##########pytz#######################
            current_time = datetime.now().time()
            horaA= utc_to_gmt_minus_5(current_time)

            #print("Hora UTC:", current_time.strftime("%H:%M:%S"))
            
            temp = datos["Temperatura"]
            print("ẗemperatura", temp)
            lab = datos["lab"]
            nroT = datos["pass"]
            
            laboratorio = request.env['controlacceso.lab'].sudo().search([('name','=',lab)])
            estudiante = request.env['controlacceso.usuarioestudiante'].sudo().search([('tarjeta','=',datos['pass'])])
            print(lab, nroT, "encontrol estudinates:",len(estudiante) > 0)
            #curso = request.env['controlacceso.curso'].sudo().search([('id','=',estudiante.curso_id.id)])
            m = request.env['controlacceso.materia'].sudo().search([('id','=',16)])
            #################################################
            curso = None
            buscarH = None
            if len(estudiante) > 0:
                print("****************")
                
                curso = None
                buscarH = None
                if len(estudiante) > 0:
                    print("la tarjeta perenece a un etudiante")
                    cursos = []
                    for c in estudiante.curso_id:
                        cursos.append(c.id)
                        print(c, "curso fooor")
                        print(c.id, "curso.id fooor")
                        c2 = request.env['controlacceso.curso'].sudo().search([('id','=',c.id)])
                        if c2:
                            curso = c2.id
                            print("see encontro el curso", curso)
                        horario = request.env['controlacceso.horario2'].sudo().search([('curso_id','=',c.id),('periodo_id.estado','=',True)])
                        if horario:
                            print("entro if horario try")
                            buscarH = horario
                            carrera = request.env['controlacceso.carrera'].sudo().search([('id','=',curso)])
                            materia = request.env['controlacceso.materia'].sudo().search([('carrera_id','=',carrera.id)])
                            print(buscarH)
                            aux = buscarH
                            nombre = request.env['res.users'].sudo().search([('id','=',estudiante.name.id)])
                            #buscarH = request.env['controlacceso.horario2'].sudo().search([('curso_id','=',estudiante.curso_id.id)])
                        #print("estos veces esta el curso en el horario", buscarH.curso_id)
                            print("antex aux try")
                            aux = buscarH
                            print("despues aux try")
                                #print("aqui esta el curso del estudiante", aux.curso_id)
                            for i in range (len(aux)):
                                if aux[i].lunes and day_of_week == 'lunes':
                                    lunes = aux[i]
                                if aux[i].martes and day_of_week == 'martes':
                                    martes = aux[i]
                                if aux[i].miercoles and day_of_week == 'miércoles':
                                    miercoles = aux[i]
                                if aux[i].jueves and day_of_week == 'jueves':
                                    jueves = aux[i]
                                if aux[i].viernes and day_of_week == 'viernes':
                                    viernes = aux[i]
                            print("entro a estudiante")
                            if lunes != None and time_str >= lunes.inicio and time_str <= lunes.fin:
                                m = request.env['controlacceso.materia'].sudo().search([('id','=',lunes.lunes.id)])
                                buscar = request.env['controlacceso.horario2'].sudo().search([('lunes','=',m.id)])
                                print("buscar en el horario", buscar.docente_id)
                                buscarDocente = request.env['controlacceso.docente2'].sudo().search([('id','=',buscar.docente_id.id)])
                                print("buscar donde", buscarDocente.id)
                                print("buscar donde", buscarDocente.name)
                                if temp < str(38):
                                    request.env['controlacceso.registroasistencia'].sudo().create({
                                                    'name':nombre.name,
                                                    'hora_ingreso':time_str,
                                                    'fecha_ingreso':date_str,
                                                    'temperatura':temp,
                                                    'tarjeta':datos["pass"],
                                                    'responsable':buscarDocente.id,
                                                    'curso_id':curso,
                                                    'materia_id':m.id,
                                                    'ingreso_usuario':"Si",
                                                    'lab_id':laboratorio.id,})
                                else:
                                    request.env['controlacceso.registroasistencia'].sudo().create({
                                                    'name':nombre.name,
                                                    'hora_ingreso':time_str,
                                                    'fecha_ingreso':date_str,
                                                    'temperatura':temp,
                                                    'tarjeta':datos["pass"],
                                                    'curso_id':curso,
                                                    'responsable':buscarDocente.id,
                                                    'materia_id':m.id,
                                                    'ingreso_usuario':"No",
                                                    'lab_id':laboratorio.id,})

                                print('creado')
                                return nombre.name
                            if martes != None and time_str >= martes.inicio and time_str <= martes.fin:
                                print("entro al martes")
                                m = request.env['controlacceso.materia'].sudo().search([('id','=',martes.martes.id)])
                                buscar = request.env['controlacceso.horario2'].sudo().search([('martes','=',m.id)])
                                buscarDocente = request.env['controlacceso.docente2'].sudo().search([('id','=',buscar.docente_id.id)])
                                if temp < str(38):
                                    request.env['controlacceso.registroasistencia'].sudo().create({
                                                    'name':nombre.name,
                                                    'hora_ingreso':time_str,
                                                    'fecha_ingreso':date_str,
                                                    'temperatura':temp,
                                                    'tarjeta':datos["pass"],
                                                    'curso_id':curso,
                                                    'ingreso_usuario':"Si",
                                                    'materia_id':m.id,
                                                    'responsable':buscarDocente.id,
                                                    'lab_id':laboratorio.id,})
                                    print('creado')
                                    return nombre.name
                                else:
                                    print("entro al registrar temperatura normal")
                                    request.env['controlacceso.registroasistencia'].sudo().create({
                                                    'name':nombre.name,
                                                    'hora_ingreso':time_str,
                                                    'fecha_ingreso':date_str,
                                                    'temperatura':temp,
                                                    'tarjeta':datos["pass"],
                                                    'curso_id':curso,
                                                    'responsable':buscarDocente.id,
                                                    'ingreso_usuario':"No",
                                                    'materia_id':m.id,
                                                    'lab_id':laboratorio.id,})
                                    print('creado')
                                    return nombre.name
                            if miercoles != None and time_str >= miercoles.inicio and time_str <= miercoles.fin:
                                m = request.env['controlacceso.materia'].sudo().search([('id','=',miercoles.miercoles.id)])
                                buscar = request.env['controlacceso.horario2'].sudo().search([('miercoles','=',m.id)])
                                buscarDocente = request.env['controlacceso.docente2'].sudo().search([('id','=',buscar.docente_id.id)])
                                if temp < str(38):
                                    request.env['controlacceso.registroasistencia'].sudo().create({
                                                    'name':nombre.name,
                                                    'hora_ingreso':time_str,
                                                    'fecha_ingreso':date_str,
                                                    'temperatura':temp,
                                                    'tarjeta':datos["pass"],
                                                    'curso_id':curso,
                                                    'responsable':buscarDocente.id,
                                                    'ingreso_usuario':"Si",
                                                    'materia_id':m.id,
                                                    'lab_id':laboratorio.id,})
                                    print('creado')
                                    return nombre.name
                                else:
                                    request.env['controlacceso.registroasistencia'].sudo().create({
                                                    'name':nombre.name,
                                                    'hora_ingreso':time_str,
                                                    'fecha_ingreso':date_str,
                                                    'temperatura':temp,
                                                    'tarjeta':datos["pass"],
                                                    'curso_id':curso,
                                                    'ingreso_usuario':"No",
                                                    'responsable':buscarDocente.id,
                                                    'materia_id':m.id,
                                                    'lab_id':laboratorio.id,})
                                    print('creado')
                                    return nombre.name
                            if jueves != None and time_str >= jueves.inicio and time_str <= jueves.fin:
                                m = request.env['controlacceso.materia'].sudo().search([('id','=',jueves.jueves.id)])
                                buscar = request.env['controlacceso.horario2'].sudo().search([('jueves','=',m.id)])
                                buscarDocente = request.env['controlacceso.docente2'].sudo().search([('id','=',buscar.docente_id.id)])
                                if temp < str(38):
                                    request.env['controlacceso.registroasistencia'].sudo().create({
                                                    'name':nombre.name,
                                                    'hora_ingreso':time_str,
                                                    'fecha_ingreso':date_str,
                                                    'temperatura':temp,
                                                    'tarjeta':datos["pass"],
                                                    'curso_id':curso,
                                                    'responsable':buscarDocente.id,
                                                    'materia_id':m.id,
                                                    'ingreso_usuario':"Si",
                                                    'lab_id':laboratorio.id,})
                                    print('creado')
                                    return nombre.name
                                else:
                                    request.env['controlacceso.registroasistencia'].sudo().create({
                                                    'name':nombre.name,
                                                    'hora_ingreso':time_str,
                                                    'fecha_ingreso':date_str,
                                                    'temperatura':temp,
                                                    'tarjeta':datos["pass"],
                                                    'curso_id':curso,
                                                    'responsable':buscarDocente.id,
                                                    'materia_id':m.id,
                                                    'ingreso_usuario':"No",
                                                    'lab_id':laboratorio.id,})
                                    print('creado')
                                    return nombre.name
                            if viernes != None and time_str >= viernes.inicio and time_str <= viernes.fin:
                                print("entro al viernes")
                                m = request.env['controlacceso.materia'].sudo().search([('id','=',viernes.viernes.id)])
                                buscar = request.env['controlacceso.horario2'].sudo().search([('viernes','=',m.id)])
                                buscarDocente = request.env['controlacceso.docente2'].sudo().search([('id','=',buscar.docente_id.id)])
                                if temp < str(38):
                                    request.env['controlacceso.registroasistencia'].sudo().create({
                                                    'name':nombre.name,
                                                    'hora_ingreso':time_str,
                                                    'fecha_ingreso':date_str,
                                                    'temperatura':temp,
                                                    'tarjeta':datos["pass"],
                                                    'curso_id':curso,
                                                    'materia_id':m.id,
                                                    'responsable':buscarDocente.id,
                                                    'ingreso_usuario':"Si",
                                                    'lab_id':laboratorio.id,})
                                    print('creado')
                                    return nombre.name
                                else:
                                    request.env['controlacceso.registroasistencia'].sudo().create({
                                                    'name':nombre.name,
                                                    'hora_ingreso':time_str,
                                                    'fecha_ingreso':date_str,
                                                    'temperatura':temp,
                                                    'tarjeta':datos["pass"],
                                                    'curso_id':curso,
                                                    'materia_id':m.id,
                                                    'responsable':buscarDocente.id,
                                                    'ingreso_usuario':"No",
                                                    'lab_id':laboratorio.id,})
                                    print('creado')
                                    return nombre.name
################################################################
            elif len(docente) > 0 and len(admin) > 0:
                nombreDocente = request.env['res.users'].sudo().search([('id','=',docente.name.id)])
                print("este es el nombre", nombreDocente.name)
                buscarH = request.env['controlacceso.horario2'].sudo().search([('docente_id','=',docente.id)])
                    #print("estos veces esta el curso en el horario", buscarH.curso_id)
                aux = buscarH
                    #print("aqui esta el curso del estudiante", aux.curso_id)
                for i in range (len(aux)):
                    if aux[i].lunes and day_of_week == 'lunes':
                        lunes = aux[i]
                    if aux[i].martes and day_of_week == 'martes':
                        martes = aux[i]
                    if aux[i].miercoles and day_of_week == 'miércoles':
                        miercoles = aux[i]
                    if aux[i].jueves and day_of_week == 'jueves':
                        jueves = aux[i]
                    if aux[i].viernes and day_of_week == 'viernes':
                        viernes = aux[i]
                if lunes != None:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',lunes.lunes.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('lunes','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"Si",
                                        'lab_id':laboratorio.id,})
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})

                    print('creado')
                    return nombreDocente.name
                if martes != None and time_str >= martes.inicio and time_str <= martes.fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',martes.martes.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('martes','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
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
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name
                if miercoles != None and time_str >= miercoles.inicio and time_str <= miercoles.fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',miercoles.miercoles.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('miercoles','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
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
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name

                if jueves != None and time_str >= jueves.inicio and time_str <= jueves.fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',jueves.jueves.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('jueves','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
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
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        'temperatura':temp,
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
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
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
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name
                else:
                    request.env['controlacceso.registroasistencia'].sudo().create({
                                            'name':nombreDocente.name,
                                            'hora_ingreso':time_str,
                                            'fecha_ingreso':date_str,
                                            'temperatura':temp,
                                            'tarjeta':datos["pass"],
                                            'curso_id':"",
                                            'materia_id':"",
                                            'ingreso_usuario':"Si",
                                            'lab_id':laboratorio.id,})
                    print('creado con temperatura norma')
                    return nombreDocente.name
################################################################
            elif len(admin) > 0:
                nombre = request.env['res.users'].sudo().search([('id','=',admin.name.id)])

                if temp < str(38):
                    request.env['controlacceso.registroasistencia'].sudo().create({
                                            'name':nombre.name,
                                            'hora_ingreso':time_str,
                                            'fecha_ingreso':date_str,
                                            'temperatura':temp,
                                            'tarjeta':datos["pass"],
                                            'curso_id':"",
                                            'materia_id':"",
                                            'ingreso_usuario':"Si",
                                            'lab_id':laboratorio.id,})
                    print('creado con temperatura norma')
                    return nombre.name
                else:

                    request.env['controlacceso.registroasistencia'].sudo().create({
                                            'name':nombre.name,
                                            'hora_ingreso':time_str,
                                            'fecha_ingreso':date_str,
                                            'temperatura':temp,
                                            'tarjeta':datos["pass"],
                                            'curso_id':"",
                                            'materia_id':"",
                                            'ingreso_usuario':"No",
                                            'lab_id':laboratorio.id,})
                    print('creado con temperatura alta')
                    return nombre.name
###################################################################################################################
            elif len(docente) > 0:
                nombreDocente = request.env['res.users'].sudo().search([('id','=',docente.name.id)])
                print("este es el nombre", nombreDocente.name)
                buscarH = request.env['controlacceso.horario2'].sudo().search([('docente_id','=',docente.id),('periodo_id.estado','=',True)])
                    #print("estos veces esta el curso en el horario", buscarH.curso_id)
                aux = buscarH
                    #print("aqui esta el curso del estudiante", aux.curso_id)
                for i in range (len(aux)):
                    if aux[i].lunes and day_of_week == 'lunes' and time_str >= aux[i].inicio and time_str <= aux[i].fin:
                        lunes = aux[i]
                    if aux[i].martes and day_of_week == 'martes' and time_str >= aux[i].inicio and time_str <= aux[i].fin:
                        martes = aux[i]
                    if aux[i].miercoles and day_of_week == 'miércoles' and time_str >= aux[i].inicio and time_str <= aux[i].fin:
                        miercoles = aux[i]
                    if aux[i].jueves and day_of_week == 'jueves' and time_str >= aux[i].inicio and time_str <= aux[i].fin:
                        jueves = aux[i]
                    if aux[i].viernes and day_of_week == 'viernes' and time_str >= aux[i].inicio and time_str <= aux[i].fin:
                        viernes = aux[i]
                if lunes != None:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',lunes.lunes.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('lunes','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"Si",
                                        'lab_id':laboratorio.id,})
                    else:
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})

                    print('creado')
                    return nombreDocente.name
                if martes != None and time_str >= martes.inicio and time_str <= martes.fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',martes.martes.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('martes','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
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
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name
                if miercoles != None and time_str >= miercoles.inicio and time_str <= miercoles.fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',miercoles.miercoles.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('miercoles','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
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
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        'temperatura':temp,
                                        'tarjeta':datos["pass"],
                                        'curso_id':buscarCurso.id,
                                        'materia_id':m.id,
                                        'ingreso_usuario':"No",
                                        'lab_id':laboratorio.id,})
                        print('creado')
                        return nombreDocente.name

                if jueves != None and time_str >= jueves.inicio and time_str <= jueves.fin:
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',jueves.jueves.id)])
                    buscar = request.env['controlacceso.horario2'].sudo().search([('jueves','=',m.id)])
                    buscarCurso = request.env['controlacceso.curso'].sudo().search([('id','=',buscar.curso_id.id)])
                    if temp < str(38):
                        request.env['controlacceso.registroasistencia'].sudo().create({
                                        'name':nombreDocente.name,
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
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
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        'temperatura':temp,
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
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
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
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
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
            hora2 = ( datetime.today().strftime('%H'))
            dia2 = (datetime.today().strftime('%A'))
            
            min2= ( datetime.today().strftime('%M')) 
            current_time2 = datetime.now().time()
            horaA2= utc_to_gmt_minus_5(current_time)
            utc_now = datetime.utcnow()

            local_tz = pytz.timezone('America/Bogota')

            local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(local_tz)

            day_of_week = local_now.strftime('%A') 

            date_str = local_now.strftime('%Y-%m-%d')  

            time_str = local_now.strftime('%H:%M')  
            print("esto se presenta",day_of_week,date_str,time_str)
            ##########pytz#######################
            admin = request.env['controlacceso.administrador'].sudo().search([('tarjeta','=',datos['pass'])])

            estudiante = request.env['controlacceso.usuarioestudiante'].sudo().search([('tarjeta','=',datos['pass'])])
            docente = request.env['controlacceso.docente2'].sudo().search([('tarjeta','=',datos['pass'])])
            laboratorio = request.env['controlacceso.lab'].sudo().search([('name','=',datos['pass'])])
            print("lab", datos['lab'])
            buscarLab = request.env['controlacceso.lab'].sudo().search([('name','=',datos['lab'])])
            print("ecnontro lab",buscarLab.id,"---",buscarLab)
            
            if len(estudiante) > 0:
                print("la tarjeta perenece a un etudiante")
                print("****************")
                
                curso = None
                buscarH = None
                if len(estudiante) > 0:
                    print("la tarjeta perenece a un etudiante")
                    cursos = []
                    for c in estudiante.curso_id:
                        c2 = request.env['controlacceso.curso'].sudo().search([('id','=',c.id)])
                        print("primer for",c2.name)
                        buscarH = request.env['controlacceso.horario2'].sudo().search([('curso_id','=',c.id),('periodo_id.estado','=',True)])
                        print(buscarH)
                        if buscarH:
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
                                if lunes != None and time_str >= lunes.inicio and time_str <= lunes.fin and lunes.laboratorio_id == buscarLab:
                                    print("entro al if despues del for")
                                    return "registrar temperatura"
                                if martes != None and time_str >= martes.inicio and time_str <= martes.fin and martes.laboratorio_id == buscarLab:
                                    
                                    return "registrar temperatura"
                                if miercoles != None and time_str >= miercoles.inicio and time_str <= miercoles.fin and miercoles.laboratorio_id == buscarLab:
                                    
                                    return "registrar temperatura"
                                if jueves != None and time_str >= jueves.inicio and time_str <= jueves.fin and jueves.laboratorio_id == buscarLab:
                                    
                                    return "registrar temperatura"
                                if viernes != None and time_str >= viernes.inicio and time_str <= viernes.fin and viernes.laboratorio_id == buscarLab:
                                    
                                    return "registrar temperatura"
                                
                                    
                            else:
                                    nombre = request.env['res.users'].sudo().search([('id','=',estudiante.name.id)])
                                    nombre_laboratorio = request.env['controlacceso.lab'].sudo().search([('name','=',datos['lab'])])
                                    request.env['controlacceso.registrointentoasistencia'].sudo().create({
                                                        'name':nombre.name,
                                                        'hora_ingreso':time_str,
                                                        'fecha_ingreso':date_str,
                                                        
                                                        'tarjeta':datos["pass"],
                                                        'lab_id':nombre_laboratorio.id,})
                                    print("no registrar temperatura 2")
                                    return "no registrar temperatura"
                        else:
                                    nombre = request.env['res.users'].sudo().search([('id','=',estudiante.name.id)])
                                    nombre_laboratorio = request.env['controlacceso.lab'].sudo().search([('name','=',datos['lab'])])
                                    request.env['controlacceso.registrointentoasistencia'].sudo().create({
                                                        'name':nombre.name,
                                                        'hora_ingreso':time_str,
                                                        'fecha_ingreso':date_str,
                                                        
                                                        'tarjeta':datos["pass"],
                                                        'lab_id':nombre_laboratorio.id,})
                                    print("no registrar temperatura 3")
                                    return "no registrar temperatura"
                        
                        print("****************")
                    nombre = request.env['res.users'].sudo().search([('id','=',estudiante.name.id)])
                    nombre_laboratorio = request.env['controlacceso.lab'].sudo().search([('name','=',datos['lab'])])
                    request.env['controlacceso.registrointentoasistencia'].sudo().create({
                                                        'name':nombre.name,
                                                        'hora_ingreso':time_str,
                                                        'fecha_ingreso':date_str,
                                                        
                                                        'tarjeta':datos["pass"],
                                                        'lab_id':nombre_laboratorio.id,})
                    print("no registrar temperatura 1")
                    return "no registrar temperatura"
                    """    
                    for c in estudiante.curso_id:
                        cursos.append(c.id)
                        print(c, "curso fooor")
                        print(c.id, "curso.id fooor")
                        c2 = request.env['controlacceso.curso'].sudo().search([('id','=',c.id)])
                        if c2:
                            curso = c2.id
                            print("see encontro el curso", curso)
                        horario = request.env['controlacceso.horario2'].sudo().search([('curso_id','=',c.id)])
                        if horario:
                            buscarH = horario
                            carrera = request.env['controlacceso.carrera'].sudo().search([('id','=',curso)])
                            materia = request.env['controlacceso.materia'].sudo().search([('carrera_id','=',carrera.id)])
                            print(buscarH)
                            """
                            
                
                
#####################################################################
            if len(admin) > 0:
                print("la tarjeta perenece a un administrador")
                
                return "registrar temperatura"  
#########################################################
                
            if len(docente) > 0:
                print("encontro al docente", docente)
                buscarH = request.env['controlacceso.horario2'].sudo().search([('docente_id','=',docente.id),('periodo_id.estado','=',True)])
                print("estos veces el docente da clase en la semana", buscarH.curso_id)
                aux = buscarH
                    #print("aqui esta el curso del estudiante", aux.curso_id)
                for i in range (len(aux)):
                    if aux[i].lunes and day_of_week == 'lunes' and time_str >= aux[i].inicio and time_str <= aux[i].fin:
                        print("!1")
                        lunes = aux[i]
                        print(aux[i])
                    if aux[i].martes and day_of_week == 'martes' and time_str >= aux[i].inicio and time_str <= aux[i].fin:
                        print("2")
                        martes = aux[i]
                    if aux[i].miercoles and day_of_week == 'miércoles' and time_str >= aux[i].inicio and time_str <= aux[i].fin:
                        print("3")
                        miercoles = aux[i]
                    if aux[i].jueves and day_of_week == 'jueves' and time_str >= aux[i].inicio and time_str <= aux[i].fin:
                        print("4")
                        jueves = aux[i]
                    if aux[i].viernes and day_of_week == 'viernes' and time_str >= aux[i].inicio and time_str <= aux[i].fin:
                        print("5")
                        viernes = aux[i]
                        
                        
                if lunes != None and time_str >= lunes.inicio and time_str <= lunes.fin and lunes.laboratorio_id == buscarLab:
                    print("entro al dia lunes")
                    m = request.env['controlacceso.materia'].sudo().search([('id','=',lunes.lunes.id)])
                    return "registrar temperatura"
                if martes != None and time_str >= martes.inicio and time_str <= martes.fin and martes.laboratorio_id == buscarLab:
                    return "registrar temperatura"
                if miercoles != None and time_str >= miercoles.inicio and time_str <= miercoles.fin and miercoles.laboratorio_id == buscarLab:
                    return "registrar temperatura"
                if jueves != None and time_str >= jueves.inicio and time_str <= jueves.fin and jueves.laboratorio_id == buscarLab:
                    return "registrar temperatura"
                if viernes != None and time_str >= viernes.inicio and time_str <= viernes.fin and viernes.laboratorio_id == buscarLab:
                    print("si")
                    return "registrar temperatura"
                
                else:
                    nombre = request.env['res.users'].sudo().search([('id','=',docente.name.id)])

                    nombre_laboratorio = request.env['controlacceso.lab'].sudo().search([('name','=',datos['lab'])])
                    request.env['controlacceso.registrointentoasistencia'].sudo().create({
                                        'name':nombre.name,
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        
                                        'tarjeta':datos["pass"],
                                        'lab_id':nombre_laboratorio.id,})
                    return "no registrar temperatura" 
                
             
                    
            else:
                print("la tarjeta no perenece a ningun usuario")
                nombre_laboratorio = request.env['controlacceso.lab'].sudo().search([('name','=',datos['lab'])])
                request.env['controlacceso.registrointentoasistencia'].sudo().create({
                                        'name':"Usuario no registrado en el sistema",
                                        'hora_ingreso':time_str,
                                        'fecha_ingreso':date_str,
                                        
                                        'tarjeta':datos["pass"],
                                        'lab_id':nombre_laboratorio.id,})
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