from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.cache import cache
import xero
import uuid

from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes
from .models import Form
import os
from xero.exceptions import XeroException

callback_uri = 'https://pods-app-git-4779450e3d53.herokuapp.com/callback'
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

# Create your views here.

def login(request):
       return render(request,'login.html')


def form(request):
        if(request.method == 'POST'):
              productType = request.POST['productType']
              contactID = request.POST['contactID']
              date = request.POST['date']
              dueDate = request.POST['dueDate']
              lineAmountTypes = request.POST['lineAmountTypes']
              description = request.POST['description']
              quantity = request.POST['quantity']
              unitAmount = request.POST['unitAmount']
              accountCode = request.POST['accountCode']
              discountRate = request.POST['discountRate']
              if(productType and contactID and date and dueDate and lineAmountTypes and description and quantity and unitAmount and accountCode and discountRate ):

                    form = Form(productType=productType, contactID = contactID, date=date,dueDate=dueDate,lineAmountTypes=lineAmountTypes,
                          description=description,quantity=quantity,unitAmount=unitAmount,accountCode=accountCode,
                          discountRate=discountRate)
                    form.save()
                    jsonData = {
                            "Type": productType,
                            "Contact": {
                            "ContactID": contactID
                            },
                            "Date": date,
                            "DueDate": dueDate,
                            "DateString": "2009-05-27T00:00:00",
                            "DueDateString": "2009-06-06T00:00:00",
                            "LineAmountTypes": lineAmountTypes,
                            "LineItems": [
                            {
                            "Description": description,
                            "Quantity": quantity,
                            "UnitAmount": unitAmount,
                            "AccountCode": accountCode,
                            "DiscountRate": discountRate
                            }
                            ]}
                    jsonFetch = JsonResponse(jsonData)
                    print(jsonFetch)
                    #xero.contacts.put(jsonFetch)

                    return redirect(success)
              else:
                  return render(request,'form.html')
        else:
              return render(request,'form.html')


def start_xero_auth_view(request):
    # Updated scopes as per the Xero API requirements
    scopes = [
        XeroScopes.OPENID,
        XeroScopes.PROFILE,
        XeroScopes.EMAIL,
        XeroScopes.OFFLINE_ACCESS,
        XeroScopes.ACCOUNTING_CONTACTS,
        XeroScopes.ACCOUNTING_TRANSACTIONS,
        XeroScopes.ACCOUNTING_ATTACHMENTS,
        XeroScopes.ACCOUNTING_SETTINGS,
        XeroScopes.ACCOUNTING_JOURNALS_READ,
        XeroScopes.ACCOUNTING_REPORTS_READ,
        XeroScopes.PROJECTS,
        XeroScopes.ASSETS
    ]

    credentials = OAuth2Credentials(
        client_id, client_secret, callback_uri=callback_uri, scope=scopes
    )
    authorization_url = credentials.generate_url()
    # Generate a unique state string
#     state = str(uuid.uuid4())
    # Append the state to the authorization URL manually
#     authorization_url += '&state=' + state
    # Store the entire state
    cache.set('xero_creds', credentials.state)
    
    # Store and log the 'state' parameter
    cache.set('xero_oauth_state', credentials.state.get('auth_state'))
    
    print("Stored OAuth state:", credentials.state.get('auth_state'))  # Add logging

    return HttpResponseRedirect(authorization_url)

def process_callback_view(request):
       saved_state = cache.get('xero_oauth_state')
       returned_state = request.GET.get('state')

       print("Saved state:", saved_state)  # Log saved state
       print("Returned state:", returned_state)  # Log returned state

       if not saved_state or not returned_state or saved_state != returned_state:
              # Handle the error - state mismatch
              return render(request, 'error.html', {'error': 'State parameter mismatch'})

       cred_state = cache.get('xero_creds')
       credentials = OAuth2Credentials(**cred_state)
       auth_secret = request.get_raw_uri()
       credentials.verify(auth_secret)
       credentials.set_default_tenant()
       cache.set('xero_creds', credentials.state)
       return redirect('latest_invoice')  # Redirect after successful auth

def some_view_which_calls_xero(request):
       cred_state = cache.get('xero_creds')
       credentials = OAuth2Credentials(**cred_state)
       if credentials.expired():
           credentials.refresh()
           cache.set('xero_creds', credentials.state)
       xero = Xero(credentials)

       contacts = xero.contacts.all()

def success(request):
    return render(request,'message.html')

def latest_invoice(request):
    try:
        # Retrieve the Xero credentials from cache
        cred_state = cache.get('xero_creds')
        if not cred_state or not cred_state.get('token'):
            # Redirect to the auth view if credentials are not in cache
            return redirect('auth')

        credentials = OAuth2Credentials(**cred_state)

        # Check if token is valid and contains 'expires_at'
        if 'expires_at' not in credentials.token:
            # Redirect to re-authenticate if token is invalid or incomplete
            return redirect('auth')

        # Refresh credentials if expired
        if credentials.expired():
            credentials.refresh()
            cache.set('xero_creds', credentials.state)

        # Initialize Xero API client
        xero_client = Xero(credentials)

        # Fetch the latest invoice
        invoices = xero_client.invoices.all()
        latest_invoice = invoices[0] if invoices else None

        # Pass the latest invoice to the template
        return render(request, 'latest_invoice.html', {'invoice': latest_invoice})

    except XeroException as e:
        # Handle Xero API errors
        return render(request, 'error.html', {'error': str(e)})
    except Exception as e:
        # Handle any other errors
        return render(request, 'error.html', {'error': 'An unexpected error occurred'})