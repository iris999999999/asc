from django.shortcuts import render, redirect
from device_message.models import Device_Message
from persons_card.models import Persons_Card
from persons.models import Persons
import pandas as pd
#import oursql 

import psycopg2
import numpy as np


def messages(request):
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
    #result = Device_Message.objects.raw(sql)
    #organizations_departaments = set()
    #persons_jobs = set()
    

    #for line in result:
     #   person = Persons.objects.get(id=Persons_Card.objects.get(id=line.persons_card_id).persons_id)
      #  organizations_departaments.add(line.oo_name+"_"+line.dd_name)
       # persons_jobs.add(line.oo_name+"_"+line.dd_name+"**********"+line.pp_sur_name+" "+line.pp_name+" "+line.pp_patronymic+"_"+line.dd_name)
   
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

    #for index, row in persons_jobs.iterrows():
      #s  print(row['oo_name'],row['dd_name'],row['pp_sur_name'],row['pp_name'],row['pp_patronymic'],row['jj_name'])
    
    
    return render(request,'device_message.html',{                                     
                                                 "organizations_departaments":organizations_departaments,
                                                 "persons_jobs":persons_jobs,
                                                 "devices_messages":devices_messages                                                 
                                                 })
    


