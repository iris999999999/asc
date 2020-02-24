from django.shortcuts import render, redirect
from device_message.models import Device_Message
from persons_card.models import Persons_Card
from persons.models import Persons

def messages(request):
    sql = """
select dmdm.id, pp."sur_name",pp."name" ,pp."patronymic",jj."name", dd."name",oo."name", date_f,time_f, "readerID"
from device_message_device_message dmdm 
left join persons_card_persons_card pc on dmdm.persons_card_id = pc.id
left join persons_persons pp on pc.persons_id = pp.id
left join jobs_jobs jj on pp.jobs_id = jj.id
left join departaments_departaments dd on jj.departaments_id = dd.id
left join organizations_organizations oo on dd.organizations_id = oo.id order by oo."name"
    """
    result = Device_Message.objects.raw(sql)
    for line in result:
        person = Persons.objects.get(id=Persons_Card.objects.get(id=line.persons_card_id).persons_id)
        print(person.name, person.sur_name)
    messages = Device_Message.objects.all()
    #messages = Device_Message.objects.filter(readerID="Вход")
    cards    = Persons_Card.objects.filter()
    persons  = Persons.objects.all()
    return render(request,'device_message.html',{"messages":messages,
                                                 "cards":cards,
                                                 "persons":persons,})
    


