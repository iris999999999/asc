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
    
    df1 = df[['oo_name','dd_name']].copy()
    organizations_departaments = df1.groupby(['oo_name','dd_name']).size().reset_index(name='count') 
    
    df1 = df[['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name']].copy()
    persons_jobs = df1.groupby(['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name']).size().reset_index(name='count') 
    
    df1 = df[['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name','date_f','time_f','readerID']].copy()
    devices_messages = df1.groupby(['oo_name','dd_name','pp_sur_name','pp_name','pp_patronymic','jj_name','date_f','time_f','readerID']).size().reset_index(name='count') 
    
   
    
    return { "organizations_departaments":organizations_departaments,
             "persons_jobs":persons_jobs,
             "devices_messages":devices_messages                                                 
            }
    


def messages(request):    
    
    return render(request,'device_message.html',get_sql())

def some_view(request):

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "report saved!")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='save.pdf')    


def index(request):   
    return some_view(request)
    # return render(request, "index.html")

def return_(request):
    return render(request, "device_message.html", context = get_sql())