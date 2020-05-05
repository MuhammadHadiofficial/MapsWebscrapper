from django.http import HttpResponse,JsonResponse
from django.shortcuts import  render,redirect,reverse
from .scripts import scrapper
import uuid
import pandas as pd
import stripe

stripe.api_key='sk_test_TggFaJ2qeD6vxBQAIxetAFnO00d8P2tsGp'
def index(request):
    # for sesskey in request.session.keys():
    #     print(request.session[sesskey])
    #     del request.session[sesskey]

    return render(request,'index.html')

def getData(request):
    # results = pd.DataFrame()
    #

    # return JsonResponse({'msg': 'success', 'id': 67786, 'count': 24});
    # request.session['payment'] = 'no';
    #
    # print(request.session.keys())
    # if('id' in request.session.keys()):
    #     request.session.modified = True
    #
    #     del request.session['id']
    #     # m=request.session.pop('id')
    #     print(request.session.keys())
    #     request.session['id']=None
    # if('filepath' in request.session.keys()):
    #
    #     request.session.modified = True
    #
    #     del request.session['filepath'];
    #     request.session['filepath']=None
    #
    #     print(request.session.keys())
    #
    #
    # # print(request.POST.get('product'),uuid.uuid1())
    request.session.flush();
    if(request.method=='POST' and request.is_ajax()):
        id = str(uuid.uuid1())
        file=scrapper.getData(request.POST.get('product'), request.POST.get('city'), 'Germany', id)
        print(id)
        # print(request.session)
        if(file['total'] == 0):
            return JsonResponse({'msg': 'failed', 'count': file['total']})
        else:
            request.session['id']=id;
            request.session['filepath'] = file['filename'];
            request.session['payment'] = 'no';
            request.session['total']=file['total']
            return JsonResponse({'msg':'success','id':id,'count':file['total']});
    # print(filename)
    # return HttpResponse(filename)
def getFile(request):
    print('file')
    if(    'id' in request.session.keys() and   'filepath' in request.session.keys() and request.session['payment']=='yes'):
        print(request.session['id'],request.session['payment'])
        file = pd.read_csv(request.session['filepath'])
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + request.session['id'] + '.csv'
        file.to_csv(path_or_buf=response, sep=';', float_format='%.2f', index=False, decimal=",")

        return response
    else:
        redirect('non/2')
def getPay(request):
        if( 'id' in request.session.keys() and   'filepath' in request.session.keys() and request.session['payment']!='yes'):
            print(request.session.keys())
            return render(request,'payment.html',context={'charge':int((int(request.session['total'])*20)/100)})
        else:
            return    redirect('non/2')
def charge(request):
    amount=int((int(request.session['total'])*20)/100)
    print(amount)
    if(request.method=='POST' and 'filepath' in request.session.keys() and request.session['payment']!='yes'):
        customer=  stripe.Customer.create(
            email=request.POST['email'],
            name=request.POST['nickname'],
            source=request.POST['stripeToken']
        )
        charge=stripe.Charge.create(
            customer=customer,
            amount=amount*100,
            currency='usd',
            description=request.session['filepath'],

        )
        print(charge.paid)
        print('data',request.POST)
        # receipt_url
        # seller_message
        # paid
        print(charge)
        if(charge.paid):

            request.session['payment']='yes'
            print(request.session['payment'])
            return render(request,'success.html', context={'url':charge.receipt_url});
        else:
            return render(request, 'payment.html',context={'msg':'Failed! there was a problem with your payment. Retry!','charge':int((int(request.session['total'])*20)/100)})

    else:
        print("hell")
        return render(request, 'payment.html',context={'charge':int((int(request.session['total'])*20)/100)})
def successMsg(request,args):
    if ('filepath' in request.session.keys() and request.session['payment'] == 'yes'):

        amount=args
        return render(request,'success.html')
    else:

        redirect('non/1')
def notfound_404(request,args):
    n=args
    error=''
    print(n)
    if n=='1':
        error='Search Again!'
    elif n=='2':
        error='Payment not processed'
    else:
        error='khghjghj'

    return    render(request,'404.html',context={'err':error})