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
        context = {'service_line': service_line}
        return render(request, 'tickets/processing.html', context)

    def post(self, request, *args, **kwargs):
        if len(service_line['change_oil']) > 0:
            service_line['change_oil'].pop(0)
        elif len(service_line['inflate_tires']) > 0:
            service_line['inflate_tires'].pop(0)
        elif len(service_line['diagnostic']) > 0:
            service_line['diagnostic'].pop(0)
        return redirect('/next')

class Next(View):
    def get(self, request, *args, **kwargs):
        next = 0
        if len(service_line['change_oil']) > 1:
            next = service_line.get('change_oil')[0]
        elif len(service_line['inflate_tires']) > 1:
            next = service_line.get('inflate_tires')[0]
        elif len(service_line['diagnostic']) > 1:
            next = service_line.get('diagnostic')[0]
        context = {'next': next}
        return render(request, 'tickets/next.html', context)