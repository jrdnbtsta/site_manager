import json
import http

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.views import View

from rsvp.models import Guest, Party

# Create your views here.

def wake_up(self):
    content = {
        "status": "success",
        "message": "server is now awake"
    }
    status = http.client.OK

    return HttpResponse(content=json.dumps(content), status=status, content_type='application/json')


class PartyAPI(View):

    def get(self, request):
        """
        Based on query params, get party
        return body:
        {
            guest_id: <int>,
            first_name: <str>,
            email: <str>,
            address: <str>
            attending_wedding: <bool>,
            attending_welcome_dinner: <bool>,
            party: [
                {
                    guest_id: <int>,
                    first_name: <int>,
                    last_name: <int>,
                    email: <str>,
                    address: <str>
                    attending_wedding: <bool>,
                    attending_welcome_dinner: <bool>,
                },
                {
                    guest_id: <int>,
                    first_name: <int>,
                    last_name: <int>,
                    email: <str>,
                    address: <str>
                    attending_wedding: <bool>,
                    attending_welcome_dinner: <bool>,
                },
            ]
            party_count: 2,
        }
        """

        first_name = request.GET.get('first_name', '')
        last_name = request.GET.get('last_name', '')
        email = request.GET.get('email', '')
        init_guest = None

        try:
            if email:
                init_guest = Guest.objects.filter(email__iexact=email).first()
            elif first_name and last_name:
                init_guest = Guest.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name).first()
            if not init_guest:
            
                # send error / tell user to reach out
                content = {
                    "message": "no-guest-found",
                    "status": "error",
                    "party": [],
                    "guest_id": None
                }
                status = http.client.BAD_REQUEST
                return HttpResponse(content=json.dumps(content), status=status, content_type='application/json')

            try:
                party = []
                p = Party.objects.filter(guest=init_guest).first()
                for guest in p.guest.all():
                    party.append({
                        "guest_id": guest.id,
                        "first_name": guest.first_name,
                        "last_name": guest.last_name,
                        "email": guest.email,
                        "address": guest.address,
                        "attending_wedding": guest.attending_wedding,
                        "attending_welcome_dinner": guest.attending_welcome_dinner
                    })

                content = {
                    "guest_id": init_guest.id,
                    "party": party,
                    "party_count": len(party),
                    "status": "success",
                    "message": "received party"
                }
                status= http.client.OK

            except AttributeError:
                content = {
                    "guest_id": init_guest.id,
                    "party": party,
                    "party_count": 1,
                    "status": "success",
                    "message": "No Party Associated with guest"
                }
                status = http.client.ok

        except Exception as e:
            content = {
                "status": "error",
                "message": e
            }
            status = http.client.BAD_REQUEST


        return HttpResponse(content=json.dumps(content), status=status, content_type='application/json')


@method_decorator(csrf_exempt, name='dispatch')
class GuestAPI(View):

    def put(self, request):
        guest_fields = ['email', 'address', 'attending_wedding', 'attending_welcome_dinner', 'notes']
        data = json.loads(request.body)        
        id = data.get('id')
        updated_guest = False

        try:
            if id:
                guest = Guest.objects.filter(pk=id).first()

                for key, value in data.items():
                    if key in guest_fields:
                        updated_guest = True
                        setattr(guest, key, value)

                if updated_guest:
                    guest.save()
                    content = {
                        "status": "succesfully updated guest",
                        "guest": {
                            "id": guest.id,
                            "first_name": guest.first_name,
                            "last_name": guest.last_name,
                            "email": guest.email,
                            "address": guest.address,
                            "attending_wedding": guest.attending_wedding,
                            "attending_welcome_dinner": guest.attending_welcome_dinner,
                            "notes": guest.notes
                        }
                    }
                    status = http.client.OK

                else:
                    content = {
                        "message": "No editable guest fields provided",
                        "status": "error"
                    }
                    status = http.client.BAD_REQUEST

            else:
                content = {
                    'status': 'error',
                    'message': 'missing ID'
                }
                status = http.client.BAD_REQUEST

        except Exception as e:
            content = {
                "status": "Exception",
                "message": e,
            }
            status = http.client.BAD_REQUEST

        return HttpResponse(content=json.dumps(content), status=status, content_type='application/json') 
