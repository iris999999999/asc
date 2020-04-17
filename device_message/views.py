from django.shortcuts import render, redirect
from device_message.models import Device_Message
from persons_card.models import Persons_Card
from persons.models import Persons

from .forms import DateForm
from .forms import Organization_Form

from django.http import FileResponse
from django.http import HttpResponse
import requests as req

import pandas as pd
import psycopg2

import datetime

import bs4
from fpdf import FPDF
from datetime import datetime, date, time


def get_sql(form_organization,date_time):   

    sql = """
    select dmdm.id, pp."sur_name" as pp_sur_name,pp."name" as pp_name ,pp."patronymic" as pp_patronymic,
    jj."name" as jj_name, dd."name" as dd_name,oo."name" as oo_name, oo."id" as oo_id, date_f,time_f, 
    "readerID"
    from device_message_device_message dmdm 
    left join persons_card_persons_card pc on dmdm.persons_card_id = pc.id
    left join persons_persons pp on pc.persons_id = pp.id
    left join jobs_jobs jj on pp.jobs_id = jj.id
    left join departaments_departaments dd on jj.departaments_id = dd.id
    left join organizations_organizations oo on dd.organizations_id = oo.id order by oo."name"
        """
    

    conn_string = "host='localhost' dbname='ascdb' user='ascadmin' password='i'" 
    conn = psycopg2.connect(conn_string) 
    #frame_query принимает результат sql запроса, а вовзращает DataFrame 
    df  = pd.read_sql(sql, conn)
    #df.to_csv('123.csv')   

    date_1 = date_time["datetime1"].date()  
    date_2 = date_time["datetime2"].date()

    time_1 = date_time["datetime1"].time()  
    time_2 = date_time["datetime2"].time()

   
    df_ = df.groupby(['oo_name','oo_id','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name','date_f','time_f','readerID']).size().reset_index(name='count').query('(date_f >= @date_1)&(date_f <= @date_2)&(time_f >= @time_1)&(time_f <= @time_2)').copy()
   
    df1 = df_[['oo_name','dd_name','oo_id']].copy()
    id_organization = 1
    if int(form_organization) == 2:
        id_organization = 3
    elif int(form_organization) == 3:
        id_organization = 9

    if  id_organization == 1:
        organizations_departaments = df1.groupby(['oo_name','dd_name','oo_id']).size().reset_index(name='count')
    else:
        organizations_departaments = df1.groupby(['oo_name','dd_name','oo_id']).size().reset_index(name='count').query('oo_id == @id_organization')
       
    
    df1 = df_[['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name']].copy()
    persons_jobs = df1.groupby(['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name']).size().reset_index(name='count') 
    
    df1 = df_[['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name','date_f','time_f','readerID']].copy()
    devices_messages = df1.groupby(['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name','date_f','time_f','readerID']).size().reset_index(name='count') 
   
    now = datetime.now()
        
    return { "organizations_departaments":organizations_departaments,
             "persons_jobs":persons_jobs,
             "devices_messages":devices_messages,
             "form_date":DateForm,
             "form_organization":Organization_Form,
             "now":now.strftime('%d-%m-%Y %H:%M')                                                
            }   


def dateTimeF():
    return {'datetime1':datetime.combine(date.today(),time(0,0)),
            'datetime2':datetime.combine(date.today(),time(23,0))}


def messages(request):    
    
    return render(request,'device_message.html',get_sql(1,dateTimeF()))



def refreshPage(request):   
    form = DateForm(request.GET)
    return render(request, "device_message.html",
    context = get_sql(1,DateTime_1(),DateTime_2()))
        

def PageBootstrap(request): 
    
    if request.method == "GET":
        return render(request, "device_message_b.html", context = get_sql(1,dateTimeF()))

    elif request.method == "POST":
        form  = Organization_Form(request.POST)
        formD = DateForm(request.POST)
        form_organization_=""
        date1_=datetime.combine(date.today(),time(0,0))
        date2_=datetime.combine(date.today(),time(23,0))

        #import pdb; pdb.set_trace()
        if form.is_valid():
          form_organization_= form.cleaned_data.get("organization_list") 
         
        if formD.is_valid():
          
          date1_= formD.cleaned_data.get("date1") 
          date2_= formD.cleaned_data.get("date2") 
          

        return render(request, "device_message_b.html", 
            context = get_sql(form_organization_,{'datetime1':date1_,'datetime2':date2_}))
    else:
        return HttpResponseNotAllowed()

def table_pdf(data,pdf,spacing=1):   
 
    #col_width = pdf.w / 4.5
    #row_height = pdf.font_size

    col_width = 40
    row_height = 7

    for row in data:
        pdf.cell(40)
        pdf.set_fill_color(180,0,157)
        for item in row:
            
            pdf.cell(col_width, row_height*spacing,
                     txt=item, align="C", border=1)
            
        pdf.ln(row_height)

    return pdf

def save_from_html(request): 
    
    resp = req.get("http://127.0.0.1:8000/") 
    soup = bs4.BeautifulSoup(resp.text, 'lxml')
 
    response = HttpResponse(content_type='pdf')
    response['Content-Disposition'] = 'attachment'
    #filename=/home/irina/Documents/python_projects/asc/device_message.pdf

    pdf = FPDF()
    pdf.add_page()
    font = '/home/irina/Documents/python_projects/asc/font/DejaVuSansCondensed-Bold.ttf'
    fontB = '/home/irina/Documents/python_projects/asc/font/DejaVuSansCondensed.ttf'
    pdf.add_font('DejaVu', '', font, uni=True)
    pdf.set_font('DejaVu', '', 7)
    pdf.cell(190, 7, txt="Система контроля и управления доступом ASC32", ln=1, align="R")
    
    #pdf.add_font('DejaVu', '', font, uni=True)
    pdf.set_font('DejaVu', '', 7)
    pdf.cell(190, 7, txt="{}".format(soup.find('div',id='date_time_now').text.strip()), ln=1, align="R")
    
    #pdf.add_font('DejaVu', '', fontB, uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 10, txt="Отчет по контролю времени входа/выхода персонала на предприятии.", ln=1, align="C")
    
    for sub_heading in soup.find_all('div',id='organizations_departaments'):
        #pdf.add_font('DejaVu', 'B', fontB, uni=True)
        pdf.set_font('DejaVu', '', 13)  
        pdf.set_text_color(222,154,255)         
        pdf.cell(0, 10, txt="{}".format(sub_heading.text.strip()), ln=1, align="C")
        
        for sub_heading1 in soup.find_all('div',id='persons_jobs'):
            if sub_heading1.find_previous('div',id='organizations_departaments').text == sub_heading.text:
            
                #pdf.add_font('DejaVu', '', font, uni=True)
                pdf.set_font('DejaVu', '', 11)
                pdf.set_text_color(0,0,0)  
                pdf.cell(0, 10, txt="{}".format(sub_heading1.text.strip()), ln=1, align="C")
                
                data = []
                data1 = []
                data.append(['Дата','Время','Считыватель'])
                k = 1
                
                for sub_heading2 in soup.find_all('tr'):
                    
                    if sub_heading2.find_previous('div',id='persons_jobs') != None:
                        if sub_heading2.find_previous('div',id='persons_jobs').text == sub_heading1.text:
                            if  (sub_heading2.text.strip() !=""):
                                if (sub_heading2.text.find("Дата") == -1) and (sub_heading2.text.find("Проход") == -1) and (sub_heading2.text.find("Считыватель") == -1):
                                    data.append(sub_heading2.text.strip().split('\n'))
                                            

                
                pdf.set_font('DejaVu', '', 9)
                pdf.set_text_color(0,0,0)

                pdf = table_pdf(data,pdf) 

    pdf.output("device_message.pdf")

    return response
 

def return_(request):
    return render(request, "device_message.html", context = get_sql())