from django.http import HttpResponse,JsonResponse
from django.shortcuts import  render,redirect,reverse
from .scripts import scrapper
import uuid
import pandas as pd
import stripe
from .models import Business,Orders
# Create your views here.
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest,OrdersCaptureRequest

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

# Creating Access Token for Sandbox
client_id = "AantCxTo8S2RR6e6aRbMV29ZqXwX26bleXFuNq9HmLc2LdAGpxg3SLwKwfypZRutj-6QNoyy1givplZf"
client_secret = "EB8VmPeLMJi0ke7UMryZ8-7TJOv0LRluKUSLaYQ1oPeVn7JDgR-ZgaMPehk1Cp1bT88WRihUxYP7Nchi"
# Creating an environment
environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment)

stripe.api_key='sk_test_TggFaJ2qeD6vxBQAIxetAFnO00d8P2tsGp'



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None




# Opens up page as PDF
class ViewPDF(View):


    def get(self, request, *args, **kwargs):
        data = Orders.objects.get(orderID=request.session['orderID'])
        charge = int((int(request.session['total']) * 20) / 100)
        tax = float(charge) * 0.15
        totalprice = float(charge) + tax
        print(totalprice)
        data = {
            "orderID": data.orderID,
            "email": data.email,
            "company_name": data.company_name,
            "keyword": data.keyword,
            "city": data.city,
            "client_name": data.client_name,
            "amount": data.amount,
            "tax":tax,
            "charge":data.net_price,
            "status": data.status,
            "address": data.address,
            "orderDate": data.orderDate,
            "total":data.total
        }
        print(data)
        pdf = render_to_pdf('pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class DownloadPDF(View):

    def get(self, request, *args, **kwargs):
        data = Orders.objects.get(orderID=request.session['orderID'])
        charge = int((int(request.session['total']) * 20) / 100)
        tax = float(charge) * 0.15
        totalprice = float(charge) + tax
        print(totalprice)
        data = {
            "orderID": data.orderID,
            "email": data.email,
            "company_name": data.company_name,
            "keyword": data.keyword,
            "city": data.city,
            "client_name": data.client_name,
            "amount": totalprice,
            "tax": tax,
            "charge": data.net_price,
            "status": data.status,
            "address": data.address,
            "orderDate": data.orderDate,
            "total": data.total
        }

        pdf = render_to_pdf('pdf_template.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (data['orderID'])
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
import  os
def index(request):
    # for sesskey in request.session.keys():
    #     print(request.session[sesskey])
    #     del request.session[sesskey]
    try:
        os.remove(request.session['filepath'])
        print("deleted")
    except FileNotFoundError:
        print("not found")


    except KeyError:
        print("keyerror")
    request.session.flush();

    return render(request,'index.html')

def getData(request):

    request.session.flush();
    if('filepath'  in request.session):
        import os
        try:
            os.remove(request.session['filepath'])
            print("deleted")
        except FileNotFoundError:
            print("not found")
    if(request.method=='POST' and request.is_ajax()):
        id = str(uuid.uuid1())
        request.session['keyword']=str(request.POST.get('product')).lower().strip()
        request.session['city']=str(request.POST.get('city')).lower().strip()
        data=  Business.objects.filter(keyword=str(request.POST.get('product')).lower().strip(),city= str(request.POST.get('city')).lower().strip(),country='Germany').order_by('name')
        if(data.count()>0):
            print(data)
            filename = './' + id + '.csv';
            df = []
            for d in data:
                name=d.name
                rating=d.rating;
                reviews=d.reviews;
                details=d.industry
                street=d.street
                street_number=d.street_number
                city=d.city
                country=d.country
                phonenumber=d.phone_number;
                weblink=d.website;
                email=d.email
                postalCode=d.postalcode
                area=d.area
                df.append((name,rating,details,street,street_number,postalCode,area,city,country,phonenumber,weblink,email))
            dataFrame = pd.DataFrame(df, columns=(
                'Firmenname / COMPANY NAME', 'rating', 'Branche / INDUSTRY', 'Strasse / Street','Strasse no',"PostalCode","Area",
                'Stadt / City', 'Land / COUNTRY', 'phone_number', 'website','email'))
            dataFrame=dataFrame.reset_index(drop=True)
            dataFrame.to_csv(filename)

            request.session['id'] = id;
            request.session['filepath'] = filename
            request.session['payment'] = 'no';
            request.session['total'] = data.count()

            rating_count=dataFrame[dataFrame['rating']!='-'].count()[0]
            phone_count=dataFrame[dataFrame['phone_number']!='-'].count()[0]
            email_count=dataFrame[dataFrame['email']!='-'].count()[0]
            website_count=dataFrame[dataFrame['website']!='-'].count()[0]
            name_count=dataFrame[dataFrame['Firmenname / COMPANY NAME']!='-'].count()[0]
            postalCode_count=dataFrame[dataFrame['PostalCode']!='-'].count()[0]

            return JsonResponse({'msg': 'success', 'id': id, 'count': data.count(),'rating_count':str(rating_count),
                                 'phone_count':str(phone_count),'email_count':str(email_count),'website_count':str(website_count),
                                 'name_count':str(name_count),'postalCode_count':str(postalCode_count)});

        file=scrapper.getData(str(request.POST.get('product')).lower().strip(), str(request.POST.get('city')).lower().strip(), 'Germany', id,request.POST.get('radius'))
        if(file['total'] == 0):
            return JsonResponse({'msg': 'failed', 'count': file['total']})
        else:
            request.session['id']=id;
            request.session['filepath'] = file['filename'];
            request.session['payment'] = 'no';
            request.session['total']=file['total']

            return JsonResponse({'msg':'success','id':id,'count':file['total'], 'rating_count': file['rating_count'],
                         'phone_count': file['phone_count'], 'email_count':file['email_count'], 'website_count': file['website_count'],
                         'name_count': file['name_count'], 'postalCode_count': file['postalCode_count']});


def finalizeCheckout(request,args):
    charge = int((int(request.session['total']) * 20) / 100)
    tax = float(charge) * 0.15
    totalprice = float(charge) + tax


    print(request.POST)
    if(request.method=='POST' and 'filepath' in request.session.keys() and request.session['payment']!='yes'):

        print(args)
        orderID=args;


        request2 = OrdersGetRequest(args)

        response = client.execute(request2)

        print(float(response.result.purchase_units[0].amount.value))
        if(response.result.status=='APPROVED'):
            print(float(response.result.purchase_units[0].amount.value))
            if(totalprice==float(response.result.purchase_units[0].amount.value)):
                print('Order',response.result.purchase_units[0].amount.value)
                print('Status Code: ', response.status_code)
                print('Status: ', response.result.status)
                print('Order ID: ', response.result.id)
                request3 = OrdersCaptureRequest(response.result.id)
                # 3. Call PayPal to capture an order
                response = client.execute(request3)
                if(response.result.status=='COMPLETED'):
                    print('Status Code: ', response.status_code)
                    print('Status: ', response.result.status)
                    print('Order ID: ', response.result.id)

                    order_data=Orders(total=request.session['total'],city=request.session['city'],keyword=request.session['keyword'],net_price=charge,amount=totalprice,status=response.result.status,orderID=response.result.id,email=request.POST['email'],address=request.POST['address'],company_name=request.POST['company'],client_name=request.POST['name'])

                    order_data.save()

                    request.session['payment'] = 'yes'
                    request.session['orderID']=response.result.id
                    print(request.session['payment'])
                    return JsonResponse({'msg':'success'})
                else:
                    return JsonResponse({'msg':'failed'})
            else:
                return JsonResponse({'msg': 'failed'})
        else:
            return JsonResponse({'msg': 'failed'})
    else:
        return JsonResponse({'msg':'failed'})
def getFile(request):
    if('id' in request.session.keys() and   'filepath' in request.session.keys() and request.session['payment']=='yes'):
        print(request.session['id'],request.session['payment'])
        try:
            file = pd.read_csv(request.session['filepath'])

        except FileNotFoundError:
            return redirect('/charge')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + request.session['id'] + '.csv'
        file.to_csv(path_or_buf=response, sep=';', float_format='%.2f', index=False, decimal=",")
        # import  os
        # try:
        #     os.remove(request.session['filepath'])
        #     print("deleted")
        # except FileNotFoundError:
        #     return redirect('/')

        return response
    else:
        return redirect('/non/3')

def getPay(request):


        if( 'id' in request.session.keys() and   'filepath' in request.session.keys() and request.session['payment']!='yes'):
            charge=int((int(request.session['total']) * 20) / 100)
            tax=float(charge)*0.15
            totalprice=float(charge)+tax
            return render(request,'payment.html',context={'totalprice':totalprice,'tax':tax,'charge':int((int(request.session['total'])*20)/100),'total':int(request.session['total'])})
        else:
            return    redirect('non/2')
def charge(request):
    print(request.POST)
    print(request.session.keys())
    if('filepath' in request.session.keys()):
        amount = int((int(request.session['total']) * 20) / 100)

        if(request.method=='POST' and 'filepath' in request.session.keys() and request.session['payment']!='yes'):
            customer=  stripe.Customer.create(
                email=request.POST['email'],
                name=request.POST['name'],
                source=request.POST['stripeToken']
            )
            charge=stripe.Charge.create(
                customer=customer,
                amount=amount*100,
                currency='usd',
                description=request.session['filepath'],

            )
            if(charge.paid):
                request.session['payment']='yes'
                print(request.session['payment'])
                return render(request,'success.html', context={'url':charge.receipt_url});
            else:
                return render(request, 'payment.html',context={'msg':'Failed! there was a problem with your payment. Retry!','charge':int((int(request.session['total'])*20)/100)})

        else:
            return render(request, 'payment.html',context={'charge':int((int(request.session['total'])*20)/100)})
    else:
        return redirect('/')
def successMsg(request):
    if ('filepath' in request.session.keys() and request.session['payment'] == 'yes'):

        return render(request,'success.html')
    else:

        return redirect('/')
def notfound_404(request,args):
    n=args
    if n=='1':
        error='Search Again!'
    elif n=='2':
        error='Payment not processed'
    else:
        error='Your Session Expired'

    return    render(request,'404.html',context={'err':error})