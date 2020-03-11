from django.shortcuts import render, redirect
from device_message.models import Device_Message
from persons_card.models import Persons_Card
from persons.models import Persons
import pandas as pd
import psycopg2
import numpy as np
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
import datetime
import csv

from django.http import HttpResponse
import bs4
import requests as req
from fpdf import FPDF



def get_sql():
    sql = """
select dmdm.id, pp."sur_name" as pp_sur_name,pp."name" as pp_name ,pp."patronymic" as pp_patronymic,
jj."name" as jj_name, dd."name" as dd_name,oo."name" as oo_name, date_f,time_f, 
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
    df.to_csv('123.csv')
    
    df1 = df[['oo_name','dd_name']].copy()
    organizations_departaments = df1.groupby(['oo_name','dd_name']).size().reset_index(name='count') 
    
    df1 = df[['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name']].copy()
    persons_jobs = df1.groupby(['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name']).size().reset_index(name='count') 
    
    df1 = df[['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name','date_f','time_f','readerID']].copy()
    devices_messages = df1.groupby(['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name','date_f','time_f','readerID']).size().reset_index(name='count') 
    
    now = datetime.datetime.now()
    #print(now.strftime('%d-%m-%Y %H:%M'))
    
    return { "organizations_departaments":organizations_departaments,
             "persons_jobs":persons_jobs,
             "devices_messages":devices_messages,
             "now":now.strftime('%d-%m-%Y %H:%M')                                                
            }   


def messages(request):    
    
    return render(request,'device_message.html',get_sql())

def table_pdf(data,pdf,spacing=1):
   
 
    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height*spacing,
                     txt=item, border=1)
        pdf.ln(row_height)

    return pdf

def save_from_html(request): 
    
    resp = req.get("http://127.0.0.1:8000/") 
    soup = bs4.BeautifulSoup(resp.text, 'lxml')
 
    response = HttpResponse(content_type='pdf')
    response['Content-Disposition'] = 'attachment; filename=save.pdf'

    pdf = FPDF()
    pdf.add_page()
    font = '/home/irina/Documents/python_projects/asc/font/DejaVuSansCondensed.ttf'
    pdf.add_font('DejaVu', '', font, uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.cell(200, 10, txt="Отчет по проходам", ln=1, align="C")
    
    for sub_heading in soup.find_all('h3'):
        pdf.add_font('DejaVu', '', font, uni=True)
        pdf.set_font('DejaVu', '', 13)          
        pdf.cell(0, 10, txt="{}".format(sub_heading.text.strip()), ln=1)
        
        for sub_heading1 in soup.find_all('h4'):
            if sub_heading1.find_previous('h3').text == sub_heading.text:
            
                pdf.add_font('DejaVu', '', font, uni=True)
                pdf.set_font('DejaVu', '', 11)
                pdf.cell(0, 10, txt="{}".format(sub_heading1.text.strip()), ln=1)
                
                data = []
                data1 = []
                data.append(['Дата','Проход','Считыватель'])
                k = 1
                #print(sub_heading1.text)
                for sub_heading2 in soup.find_all('tr'):
                    if sub_heading2.find_previous('h4').text == sub_heading1.text:
                        if  (sub_heading2.text.strip() !=""):
                            if (sub_heading2.text.find("Дата") == -1) and (sub_heading2.text.find("Проход") == -1) and (sub_heading2.text.find("Считыватель") == -1):
                                #print(sub_heading2.text.strip()) 
                                #if k ==3:
                                #    data1.append(sub_heading2.text.strip())                                     
                                #    data.append(data1)

                                 #   data1 = []
                                 #   k=1
                                #else:
                                    
                                    #data1.append(sub_heading2.text.strip())
                                    #print(sub_heading2.text.strip().split('\n'))
                                    data.append(sub_heading2.text.strip().split('\n'))
                                   # k+=1 


                #data.append(data1)
                

                for row in data:
                    for item in row:
                        pass
                        #print(item)

                pdf = table_pdf(data,pdf) 


    pdf.output("device_message.pdf")

    return response
 

def return_(request):
    return render(request, "device_message.html", context = get_sql())