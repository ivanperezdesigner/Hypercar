from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/menu.html', context={'options': ['Change_oil', 'Inflate_tires', 'diagnostic']})


service_line = {
    'change_oil': [],
    'inflate_tires': [],
    'diagnostic': []
}
ticket_number = 0
next_ticket = 0

class Service(View):
    def get(self, request, service, *args, **kwargs):
        if service == 'change_oil':
            global wait_time
            wait_time = len(service_line["change_oil"]) * 2
        elif service == "inflate_tires":
            wait_time = len(service_line["change_oil"]) * \
                2 + len(service_line["inflate_tires"]) * 5
        elif service == "diagnostic":
            wait_time = len(service_line["change_oil"]) * 2 + len(
                service_line["inflate_tires"]) * 5 + len(service_line   ["diagnostic"] * 30)

        global ticket_number
        ticket_number += 1
        service_line[service].append(ticket_number)
        print(service_line)

        context = {"ticket": ticket_number, "wait": wait_time}
        return render(request, 'tickets/detail.html', context)


class Processing(View):
    def get(self, request, *args, **kwargs):
        change_oil = len(service_line['change_oil'])
        inflate_tires = len(service_line['inflate_tires'])
        diagnostic = len(service_line['diagnostic'])
        context = {"change_oil": change_oil, "inflate_tires": inflate_tires, "diagnostic": diagnostic}
        return render(request, 'tickets/processing.html', context)
    
    def post(self, request, *args, **kwargs):
        global next_ticket
        if len(service_line['change_oil']) > 0:
            next_ticket = service_line['change_oil'].pop(0)
        elif len(service_line['inflate_tires']) > 0:
            next_ticket = service_line['inflate_tires'].pop(0)
        elif len(service_line['diagnostic']) > 0:
            next_ticket = service_line['diagnostic'].pop(0)
        else:
            next_ticket = 0
        return redirect('/next')

class Next(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next.html', context={"ticket_number": next_ticket})