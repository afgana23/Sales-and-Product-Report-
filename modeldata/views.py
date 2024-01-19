from django.shortcuts import render,redirect,get_list_or_404
from django .contrib import messages
from django.core.paginator import Paginator
from django.template import RequestContext
from .models import Asset,Category,Sale,Customer,Order
from .forms import AssetForm,SaleForm,AssetSelectForm,SignUpForm,CustomerForm
from django.db.models import Sum,Avg
from modeldata import models
from django  .contrib .auth import authenticate,login,logout



# Create your views here.

    
def home_page(request):


    category=request.GET.get('category')
    if category==None:
        data=Asset.objects.order_by('-amount')
    else:
         data=Asset.objects.filter(category__c_name=category)

    ca=Category.objects.all()
    
    
    contx={
        "data":data,
       
        'ca':ca,
    }
    return render(request,"index.html",contx)
def login_page(request):
      # Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('index')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('index')
	else:
          return render(request,"login.html",{})
def logout_page(request):
     logout(request)
     messages.success(request, "You Have Been Logged Out...")
     return redirect('index')

def signup_user(request):
  # if request.method == 'POST':
	form = SignUpForm(request.POST)
	if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('dashboard')
	else:
		#sform = SignUpForm()
		return render(request, 'signup.html', {'form':form})
	#return render(request, 'register.html', {'form':form})
          


def table_data(request):
     data=Asset.objects.all()
     p=Paginator(data,5)
     page=request.GET.get('page')
     pgnumber=p.get_page(page)
     contx={
       
        'pgnumber':pgnumber,
      

    }
     return render(request,"tabledata.html",contx)

def save_data(request):
     form=AssetForm(request.POST)
     if form.is_valid():
               title=form.cleaned_data['title']
               qty=form.cleaned_data['qty']
               price=form.cleaned_data['price']
               description=form.cleaned_data['description']
               date=form.cleaned_data['date']
               
               
               
               ep=Asset.objects.filter(title=title).first()
               if ep:
                    ep.qty +=qty
                    ep.price=price
                    ep.date=date
                    ep.description=description
                    ep.save()
               else:
                   ep= form.save(commit=False)
               ep.amount=ep.qty*ep.price
              
               ep.save()

               
               messages.success(request, "You Have Successfully Registered! Welcome!")
               return redirect('index')
     else:
         form=AssetForm()

     return render(request,"savedata.html",{'form':form})


def update_data(request,cid):
    asst=Asset.objects.get(id=cid)
    form=AssetForm(request.POST  or  None,instance=asst)
    if form.is_valid():
         form.save()
         messages.success(request, "You Have Successfully Updated Record! Welcome!")
		#return redirect('transaction')


    return render(request,"updatedata.html",{'form':form})


def dashboard_data(request):
    category_data=Category.objects.all()
    result=Asset.objects.all()
    products=Asset.objects.all()
    total_amount=Asset.objects.all().aggregate(Sum('amount'))['amount__sum']
    total_qty=Asset.objects.all().aggregate(Sum('qty'))['qty__sum']
    sale_amount=Sale.objects.all().aggregate(Sum('sale_amount'))['sale_amount__sum']
    sold_qty=Sale.objects.all().aggregate(Sum('qty_sold'))['qty_sold__sum']
    sum_cat=Asset.objects.values('category__c_name').annotate(tm=Sum('amount'))
    #select data fron input code
    form=AssetSelectForm(request.GET )
    if form.is_valid():
          st=form.cleaned_data["st"]
          if st:
               data=Asset.objects.filter(id=st.id)
          else:
               data=Asset.objects.all()
               #xxxxselect data inputxxxx
    for product in products:
        product.price=product.price*product.qty
        total_sum=sum(product.price for product in products)
    with_ptice=[
        {'qty':product.qty,'title':product.title ,'price':product.price,'amt':product.price,'t_price': product.qty* product.price}
        for product in result
       
    ]

    report_date=Sale.objects.extra(
           select={'month':'MONTH(sale_date)','year':'YEAR(sale_date)','day':'DAY(sale_date)'}
      
      ).values('year','month','day').annotate(
           total_sold_qty=Sum('qty_sold'),
             total_amt=Sum('sale_amount')
      )
  
    ctx={
        'total':total_amount,
        'qty':total_qty,
        'sum_cat':sum_cat,
        'result':result,
        'products':with_ptice,
        'total_sum':total_sum,
        'category_data':category_data,
        'sale_amount':sale_amount,
           'sold_qty':sold_qty,
           'report_date':report_date,

           'form':form,
           'data':data
       
 
      }
    
    return render(request,"dashboard.html",ctx)

def calculate_price(request):
    categries=Category.objects.all()
    products=Asset.objects.all()
    category_totals={}
    for category in categries:
        total_amt=Asset.objects.filter(category=category).aggregate(
        totals=Sum(models.F('amount') * models.F('qty'))

    )['totals'] or 0
    category_totals[category.c_name]=total_amt

    
    for product in products:
        product.amount=product.amount*product.qty
        total_sum=sum(product.amount for product in products)
   
   
    return render(request,"price.html",{'products':products,'total_sum':total_sum,'category_totals':category_totals })

    #for product in products:
     #   product.t_price=product.qty * product.amount
           

def single_data(request,cid):
    data=Asset.objects.get(id=cid)

    return render(request,"singledata.html",{'data':data})

def make_sale(request,cid):
      data=Asset.objects.get(id=cid)
      form=SaleForm(request.POST or  None,instance=data)
      if form.is_valid():
        # sale_qty=form.changed_data['sale_qty']
          
         #qty_sold=form.cleaned_data['qty_sold']
         title=form.cleaned_data['title']
         
         sale_qty=form.cleaned_data["sale_qty"]
         sale_date=form.cleaned_data["sale_date"]
      
       
         
         sale=Sale.objects.filter(title=title).first()
         if sale:
               sale.qty_sold +=sale_qty
               sale.sale_qty=sale_qty
               sale.sale_date=sale_date
               
              
               
        
               sale.save()
         else:   
               sale=form.save(commit=False)
             
              
         sale.sale_amount= form.cleaned_data['price']* sale.qty_sold
          
          
         sale.save()
        
         sale.update_asset_qty_amt()
         return redirect('order')
      else:
          return render(request,"sale.html",{'form':form,'data':data})

def sale_report(request):
      sale_amount=Sale.objects.all().aggregate(Sum('sale_amount'))['sale_amount__sum']
      sold_qty=Sale.objects.all().aggregate(Sum('qty_sold'))['qty_sold__sum']
      asset_amount=Asset.objects.all().aggregate(Sum('amount'))['amount__sum']
      asset_qty=Asset.objects.all().aggregate(Sum('qty'))['qty__sum']
      report_date=Sale.objects.extra(
           select={'month':'MONTH(sale_date)','year':'YEAR(sale_date)','day':'DAY(sale_date)'}
      
      ).values('year','month','day').annotate(
           total_sold_qty=Sum('qty_sold'),
             total_amt=Sum('sale_amount')
      )


      contx={
           'sale_amount':sale_amount,
           'sold_qty':sold_qty,
           'asset_qty':asset_qty,
           'asset_amount':asset_amount,
           'report_date':report_date
      }
     
      return render(request,"salesreport.html",contx)

def asset_selected_view(request):
     form=AssetSelectForm(request.GET )
     if form.is_valid():
          st=form.cleaned_data["st"]
          if st:
               data=Asset.objects.filter(id=st.id)
          else:
               data=Asset.objects.all()
    
          return render(request,"selected.html",{'form':form,'data':data})

def order_page(request,cid):
             
 customer=Customer.objects.get(id=cid)
 form=CustomerForm(request.POST ,instance=customer)
 if form.is_valid():
             form.save()
             if form.is_valid():
                   form.save()
                   messages.success(request, "You Have Successfully Updated Record! Welcome!")
		#return redirect('transaction')
           
    
             return render(request,"order.html",{'form':form})  
    
     
                                            
