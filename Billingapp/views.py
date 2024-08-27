from django.shortcuts import render
from django.db.models import Sum
import uuid
from django.utils import timezone
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from .models import *
from .form import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpRequest,HttpResponse, FileResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import make_aware
from django.db.models import Sum, F
from datetime import datetime
import pywhatkit as kit
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.db.models import Sum, F, ExpressionWrapper
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from datetime import timedelta
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
# from weasyprint import HTML
from django.template.loader import get_template
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
if os.environ.get('DISPLAY'):
    import pywhatkit as kit


def generate_unique_transaction_id(name,mobile):
    prefix = name 
    no=mobile
    timestamp = timezone.now().strftime('%y %m %d %H  %M ') 
    return f'{prefix}-{no}-{timestamp}'

# @login_required
# def billing_form(request, id):
#     BillingFormSet = formset_factory(BillingForm, extra=1)
#     customer = get_object_or_404(Customer, id=id)
#     mobile = customer.phone_number
#     TotalPrice = 0
#     if request.method == 'POST':
#         formset = BillingFormSet(request.POST)
#         if formset.is_valid():
#             transcode = generate_unique_transaction_id(customer, mobile)
#             for i, form in enumerate(formset):
#                 try:
#                     form.instance.customer = customer
#                     form.instance.transcode = transcode
#                     form.instance.transaction_id = f"{transcode}-{i}" 
#                     form.save()  # Save each form individually
#                 except KeyError as e:
#                     print(f"Missing field in form data: {e}")
#                 except Exception as e:
#                     print(f"An error occurred while saving the form: {e}")
            
#             sales = Transaction_Sale.objects.filter(transcode=transcode, customer=customer)
#             for sale in sales:
#                 TotalPrice += sale.total_price  # Calculate total price using the property
            
#             return render(request, 'Billingapp/Billing.html', {'sales': sales, 'customer': customer, 'TotalPrice': TotalPrice})
#         else:
#             print("Formset is not valid")
#             for form in formset:
#                 print(form.errors)
#             print(request.POST)
#     else:
#         formset = BillingFormSet()
#         transcode = generate_unique_transaction_id(customer, mobile)
#         for form in formset:
#             form.fields['transcode'] = transcode
    
#     return render(request, 'Billingapp/Billing.html', {'formset': formset, 'customer': customer, 'transcode': transcode})
def homepage(request):
    return render(request, 'Billingapp/home.html')
def home(request):
    transactions = Transaction_Sale.objects.all()
    top_customers = (transactions
                        .values('customer_id', 'customer__name')  # Include customer name in the query
                        .annotate(total_amount=Sum(F('product__price') * F('quantity'), output_field=models.DecimalField()))
                        .order_by('-total_amount')[:10])
    print(top_customers)
    
    customer_profit = Customer.objects.annotate(total_profit=Sum(F('transaction_sale__quantity') * (F('transaction_sale__product__price') - F('transaction_sale__product__buying_price')))).order_by('-total_profit')[:10]
    max_profit = customer_profit[0].total_profit if customer_profit else 0
    today = timezone.now()
    start_date = today - timezone.timedelta(days=7)

    # Query to get sales data for the past 7 days
    sales_data = (
    Transaction_Sale.objects.filter(timestamp__range=[start_date, today])
    .annotate(day=TruncDay('timestamp'))
    .values('day')
    .annotate(total_sales=Sum(F('quantity') * F('product__price')))
    .order_by('day')
    )

    
    days = [entry['day'].strftime('%A') for entry in sales_data]
    sales_totals = [float(entry['total_sales']) for entry in sales_data]

    days_json = json.dumps(days)
    sales_totals_json = json.dumps(sales_totals)



    profit_data = (
    Transaction_Sale.objects.filter(timestamp__range=[start_date, today])
    .annotate(day=TruncDay('timestamp'))
    .values('day')
    .annotate( total_profit=Sum((F('product__price') - F('product__buying_price')) * F('quantity')))
    .order_by('day')
    )

    
    profitdays = [entry['day'].strftime('%A') for entry in profit_data]
    profit_totals = [float(entry['total_profit']) for entry in profit_data]

    profitdays_json = json.dumps(profitdays)
    profittotals_json = json.dumps(profit_totals)


        
    return render(request, 'Billingapp/admin.html',{'top_customers': top_customers,'customer_profits':customer_profit,'max_profit':max_profit,'days_json': days_json,'sales_totals_json': sales_totals_json,'profitdays_json':profitdays_json,'profittotals_json':profittotals_json })

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('homepage')
    return redirect('/')

def user_login(request):
    if request.method == 'POST':
        if request.method == 'POST':
            username = request.POST.get('username', '')  # Provide a default value if key is missing
            password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        transactions = Transaction_Sale.objects.all()
        top_customers = (transactions
                            .values('customer_id', 'customer__name')  # Include customer name in the query
                            .annotate(total_amount=Sum(F('product__price') * F('quantity'), output_field=models.DecimalField()))
                            .order_by('-total_amount')[:10])
        

        customer_profit = Customer.objects.annotate(total_profit=Sum(F('transaction_sale__quantity') * (F('transaction_sale__product__price') - F('transaction_sale__product__buying_price')))).order_by('-total_profit')[:10]
        max_profit = customer_profit[0].total_profit if customer_profit else 0




        today = timezone.now()
        start_date = today - timezone.timedelta(days=7)

    # Query to get sales data for the past 7 days
        sales_data = (
        Transaction_Sale.objects.filter(timestamp__range=[start_date, today])
        .annotate(day=TruncDay('timestamp'))
        .values('day')
        .annotate(total_sales=Sum(F('quantity') * F('product__price')))
        .order_by('day')
        )

      
        days = [entry['day'].strftime('%A') for entry in sales_data]
        sales_totals = [float(entry['total_sales']) for entry in sales_data]

        days_json = json.dumps(days)
        sales_totals_json = json.dumps(sales_totals)



        profit_data = (
        Transaction_Sale.objects.filter(timestamp__range=[start_date, today])
        .annotate(day=TruncDay('timestamp'))
        .values('day')
        .annotate( total_profit=Sum((F('product__price') - F('product__buying_price')) * F('quantity')))
        .order_by('day')
        )

      
        profitdays = [entry['day'].strftime('%A') for entry in profit_data]
        profit_totals = [float(entry['total_profit']) for entry in profit_data]

        profitdays_json = json.dumps(profitdays)
        profittotals_json = json.dumps(profit_totals)


        
    

        if user is not None:
            login(request, user)
            if user.role == 'admin':
                Role=user.role
                print(top_customers)
                return render(request, 'Billingapp/admin.html',{'top_customers': top_customers,'customer_profits':customer_profit,'max_profit': max_profit,'SalesDatas':sales_data,'days_json': days_json,'sales_totals_json': sales_totals_json,'profitdays_json':profitdays_json,'profittotals_json':profittotals_json})
            elif user.role == 'own':
                Role=user.role
                print(top_customers)
                return render(request, 'Billingapp/admin.html',{'top_customers': top_customers,'customer_profits':customer_profit,'max_profit': max_profit,'SalesDatas':sales_data,'days_json': days_json,'sales_totals_json': sales_totals_json,'profitdays_json':profitdays_json,'profittotals_json':profittotals_json})
            elif user.role == 'employee':
                Role = user.role
                customer =Customer.objects.all()
                print(customer)
                return render(request, 'Billingapp/admin.html',{'top_customers': top_customers,'customer_profits':customer_profit,'max_profit': max_profit,'SalesDatas':sales_data,'days_json': days_json,'sales_totals_json': sales_totals_json,'profitdays_json':profitdays_json,'profittotals_json':profittotals_json})
        return render(request, 'Billingapp/login.html')
    return render(request, 'Billingapp/login.html')

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponse('User Added')  
    else:
        form = RegistrationForm()
    return render(request, 'Billingapp/register.html', {'form': form})

def Customerregister(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Customerlist')
    else:
        form = CustomerForm()
    customers = Customer.objects.all()
    return render(request, 'Billingapp/Customerlist.html', {'form': form, 'Customers': customers})

def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('register')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'Billingapp/customer_edit.html', {'form': form, 'customer': customer})

def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('register')
    return render(request, 'Billingapp/customer_delete_confirm.html', {'customer': customer})
def search_customer(request):
    search_text = request.POST.get('search')
    cell = request.POST.get('cell')
    results=Customer.objects.all()
    if search_text :
        results = results.filter(name__icontains=search_text)
    if cell:
        results = results.filter(phone_number__icontains=cell)
    print(results)
    return render(request, 'Billingapp/searchresult.html', {'customers':results})

def Vendor_register(request):
    if request.method == 'POST':
        form = VendorForm(request.POST)
        if form.is_valid():
            form.save()
            results=Supplier.objects.all()
            return render(request, 'Billingapp/Vendor.html', {'vendors':results})
    else:
        form = VendorForm()
    return render(request, 'Billingapp/Vendor_register.html', {'form': form})

def edit_vendor(request, vendor_id):
    vendor = get_object_or_404(Supplier, id=vendor_id)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('Vendor_register')  # Redirect to the vendor register page
    else:
        form = VendorForm(instance=vendor)
    return render(request, 'Billingapp/Vendor_edit.html', {'form': form})

def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Supplier, id=vendor_id)
    if request.method == 'POST':
        vendor.delete()
        return redirect('Vendor_register')  # Redirect to the vendor register page
    return render(request, 'Billingapp/Vendor_delete.html', {'vendor': vendor})


def search_Vendor(request):
    search_text = request.POST.get('search')
    cell = request.POST.get('phone_number')
    results=Supplier.objects.all()
    if search_text :
        results = results.filter(name__icontains=search_text)
    if cell:
        results = results.filter(phone_number__icontains=cell)

    return render(request, 'Billingapp/Vendor_searchresult.html', {'vendors':results})

def Purchase_billing_form(request, id):
    PurchaseFormSet = formset_factory(PurchaseForm, extra=1)
    vendor = get_object_or_404(Supplier, id=id)
    mobile = vendor.phone_number
    TotalPrice = 0
    
    if request.method == 'POST':
        formset = PurchaseFormSet(request.POST)
        if formset.is_valid():
            transcode = generate_unique_transaction_id(vendor, mobile)
            print(transcode)
            
            for i, form in enumerate(formset):
                try:
                    form.instance.vendor = vendor
                    form.instance.transcode = transcode
                    form.instance.transaction_id = f"{transcode}-{i}" 
                    form.save()  
                    print(f"{transcode}-{i}" )
                except KeyError as e:
                    print(f"Missing field in form data: {e}")
                except Exception as e:
                    print(f"An error occurred while saving the form: {e}")
         
            sales = Transaction_Buy.objects.filter(transcode=transcode, vendor=vendor)
           
            for sale in sales:
                TotalPrice += sale.total_price 
                return render(request, 'Billingapp/Purchase.html', {'sales': sales, 'vendor': vendor, 'TotalPrice': TotalPrice})
        else:
            print("Formset is not valid")
            for form in formset:
                print(form.errors)
            print(request.POST)
    else:
        formset = PurchaseFormSet()
        # Here, you can set the transcode for each form in the formset before rendering the form.
        transcode = generate_unique_transaction_id(vendor, mobile)
        print(transcode)
        for form in formset:
            form.fields['transcode'] = transcode
    
    return render(request, 'Billingapp/PurchaseBilling.html', {'formset': formset, 'vendor': vendor ,'transcode':transcode})

def Stock_Detail(request):
    product_names = Product.objects.values_list('name', flat=True)
    print(product_names)
    if 'product_name' in request.GET:
        product_name = request.GET['product_name']
        Stock=Product.objects.filter(name=product_name)
        return render(request, 'Billingapp/Stock.html', {'Stocks': Stock })
    else:
        Stock=Product.objects.all()
        return render(request, 'Billingapp/Stock.html', {'Stocks': Stock ,'product_names': product_names})


def Order_Detail(request):
    return render(request, 'Billingapp/emp_dashboard.html')


def Transactions_summary(request):
    transaction_summary = Transaction_Sale.objects.values('transcode').annotate(total_quantity=Sum('quantity'))
    
   
    return render(request, 'Billingapp/Transactions.html', {'TranSummeries': transaction_summary })



def delailing_view(request, transcode):
    Details=Transaction_Sale.objects.filter(transcode=transcode)
    return render(request, 'Billingapp/Transactions.html', {'Details': Details })

def Buy_summary(request):
    transaction_summary = Transaction_Buy.objects.values('transcode').annotate(total_quantity=Sum('quantity'))
    return render(request, 'Billingapp/Transactions.html', {'TranSummeries': transaction_summary })

def Buying_view(request, transcode):
    Details=Transaction_Buy.objects.filter(transcode=transcode)
    return render(request, 'Billingapp/Transactions.html', {'Details': Details })
    
def Product_Sale_view(request):
    if 'product_name' not in request.GET:
        product_names = Transaction_Sale.objects.values('product__name').annotate(total_quantity=Sum('quantity'))
        product_names1 = json.dumps([sale['product__name'] for sale in product_names])
        quantities = json.dumps([sale['total_quantity'] for sale in product_names])
        return render(request, 'Billingapp/Transactions.html', {'product_names': product_names,'product_names1': product_names1, 'quantities': quantities})
    elif 'product_name' in request.GET:
        product_name = request.GET['product_name']
        total_quantity = Transaction_Sale.objects.filter(product__name=product_name).aggregate(total_quantity=Sum('quantity'))['total_quantity']
        return render(request, 'Billingapp/Transactions.html', {'product_name': product_name, 'total_quantity': total_quantity})
   
        
    
    


   
def Transactions(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Convert dates to datetime objects and make them timezone-aware
    if start_date:
        start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
       

    if start_date and end_date:
        transactions = Transaction_Sale.objects.filter(timestamp__range=[start_date, end_date])
        total_transactions=transactions.count()
        return render(request, 'Billingapp/Transactions.html', {'Transacttions': transactions ,'total_transactions':total_transactions })
    else:
        transactions = Transaction_Sale.objects.all()
        total_transactions=transactions.count()

        return render(request, 'Billingapp/Transactions.html', {'Transacttions': transactions ,'total_transactions':total_transactions })
    

def top_customers(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Convert dates to datetime objects and make them timezone-aware
    if start_date:
        start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))

    transactions = Transaction_Sale.objects.all()
    if start_date and end_date:
        transactions = transactions.filter(timestamp__range=[start_date, end_date])

    top_customers = (transactions
                     .values('customer_id', 'customer__name')  # Include customer name in the query
                     .annotate(total_amount=Sum(F('product__price') * F('quantity'), output_field=models.DecimalField()))
                     .order_by('-total_amount')[:5])

    return render(request, 'Billingapp/top_customers.html', {'top_customers': top_customers, 'start_date': start_date, 'end_date': end_date})

def send_whatsapp_message(request):
    if request.method == 'POST':
        form = WhatsAppMessageForm(request.POST)
        if form.is_valid():
            customer = form.cleaned_data['customer']
            message = form.cleaned_data['message']
            phone_number = customer.phone_number

            # Ensure the phone number includes the country code
            if not phone_number.startswith('+'):
                # Assuming default country code as +1 (USA) if not provided
                phone_number = '+91' + phone_number

            try:
                kit.sendwhatmsg_instantly(phone_number, message, wait_time=15)
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")

            return HttpResponse("Message sent successfully!")
    else:
        form = WhatsAppMessageForm()
    
    return render(request, 'Billingapp/send_message.html', {'form': form})
def profit_report(request):
    # Calculate profit for each product
    product_profits = Transaction_Sale.objects.values('product__name', 'product__category').annotate(
        total_profit=Sum((F('product__price') - F('product__buying_price')) * F('quantity'))
    )
    total_profit_cat = sum(product['total_profit'] for product in product_profits)

    # Calculate daily profit
    daily_profits = Transaction_Sale.objects.annotate(day=TruncDay('timestamp')).values('day').annotate(
        total_profit=Sum((F('product__price') - F('product__buying_price')) * F('quantity'))
    )
    max_profit = max(daily['total_profit'] for daily in daily_profits) if daily_profits else 1
    total_profit_daily = sum(product['total_profit'] for product in daily_profits)

    # Calculate weekly profit
    weekly_profits = (
        Transaction_Sale.objects.annotate(week=TruncWeek('timestamp'))
        .values('week')
        .annotate(total_profit=Sum((F('product__price') - F('product__buying_price')) * F('quantity')))
        .order_by('week')
    )
    total_profit_week = sum(product['total_profit'] for product in weekly_profits)

    # Adding week number to the context
    week_names = ["First Week", "Second Week", "Third Week", "Fourth Week", "Fifth Week"]
    weekly_profits_with_names = []
    for i, week_profit in enumerate(weekly_profits):
        week_profit['week_name'] = week_names[i % len(week_names)]
        weekly_profits_with_names.append(week_profit)

    # Calculate monthly profit
    monthly_profits = Transaction_Sale.objects.annotate(month=TruncMonth('timestamp')).values('month').annotate(
        total_profit=Sum((F('product__price') - F('product__buying_price')) * F('quantity'))
    )
    today = timezone.now().date()
    today_profit = (
        Transaction_Sale.objects.filter(timestamp__date=today)
        .annotate(profit_per_item=(F('product__price') - F('product__buying_price')) * F('quantity'))
        .aggregate(total_profit=Sum('profit_per_item'))
    )

    context = {
        'today_profit':today_profit,
        'product_profits': product_profits,
        'daily_profits': daily_profits,
        'weekly_profits': weekly_profits_with_names,
        'monthly_profits': monthly_profits,
        'max_profit': max_profit,
        'today':today,
        'total_profit_cat':total_profit_cat,
        'total_profit_daily':total_profit_daily,
        'total_profit_week':total_profit_week
    }
    return render(request, 'Billingapp/Profit.html', context)


def customer_profit_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    total_profit = customer.total_profit()
    return render(request, 'customer_profit.html', {'customer': customer, 'total_profit': total_profit})





def index(request):
    product_names = Product.objects.values_list('name', flat=True)
    
    product_name = request.POST.get('product')  # Provide a default value if key is missing
    quantity = request.POST.get('quantity')
    print(product_name)
    return render(request,'Billingapp/billing_form.html',{'product_names': product_names})


def Billing(request):
    product_names = Product.objects.values_list('name', flat=True)
   
    if request.method=='POST':
        pass
        
    return render (request,'Billingapp/form1.html',{'product_names': product_names})

def get_product_price1(request):
    product_name = request.GET.get('product')
    if product_name:
        product = get_object_or_404(Product, name=product_name)
        price = product.price
        return HttpResponse(price)  # Ensure price is returned as JSON
    return HttpResponse(0.00)

def calculate_total_price(request):
    product_name = request.POST.get('product')
    quantity = request.POST.get('quantity')
    
    if product_name and quantity:
        product = get_object_or_404(Product, name=product_name)
        price_per_unit = product.price
        total_price = float(quantity) * float(price_per_unit)  # Convert price_per_unit to float
        return HttpResponse(total_price)  # Return the total price as JSON
    return HttpResponse(0.00)


def billing_form_view(request,id):
    customer = get_object_or_404(Customer, id=id)
    products = Product.objects.all()
    return render(request, 'Billingapp/billingform.html', {'products': products, 'customer': customer})

def get_product_price(request):
    product_id = request.GET.get('product_id')

    product = Product.objects.filter(id=product_id).values('price').first()
    print(product)
    return JsonResponse(product)

def get_product_buying_price(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.filter(id=product_id).values('buying_price').first()
    return JsonResponse({'price': product['buying_price'] if product else None})


def generate_pdf_bill(transaction_data, transcode, customer):
    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)

    # Set the font for the document
    p.setFont("Helvetica", 12)

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Draw the customer details
    p.drawString(100, 750, f"Customer: {customer.name}")
    p.drawString(100, 735, f"Date: {current_date}")  # Display date on the left side
    # p.drawRightString(550, 735, f"Phone: {customer.phone_number}")  # Display phone number on the right side
    p.drawString(100, 720, f"TC: {transcode}")

    # Draw a line above the column headers (extending across the page width)
    p.line(50, 695, 550, 695)  # Line above headers

    # Set up the column headers
    p.drawString(60, 675, "S. No.")   # S. No. column
    p.drawString(110, 675, "Product")   # Adjusted X position for "Product"
    p.drawString(260, 675, "Quantity") # Adjusted X position for "Quantity"
    p.drawString(360, 675, "Price")    # Adjusted X position for "Price"
    p.drawString(460, 675, "Total")    # Adjusted X position for "Total"

    # Draw vertical lines for columns
    p.line(50, 695, 50, 683)   # Left border
    p.line(100, 695, 100, 683) # After S. No.
    p.line(250, 695, 250, 683)  # After Product
    p.line(350, 695, 350, 683)  # After Quantity
    p.line(450, 695, 450, 683)  # After Price
    p.line(550, 695, 550, 683)  # Right border

    p.line(50, 695, 50, 675 - (len(transaction_data) * 27))   # Left border
    p.line(100, 695, 100, 665 - (len(transaction_data) * 24)) # After S. No.
    p.line(250, 695, 250, 665 - (len(transaction_data) * 24))  # After Product
    p.line(350, 695, 350, 665 - (len(transaction_data) * 24))  # After Quantity
    p.line(450, 695, 450, 665 - (len(transaction_data) * 24))  # After Price
    p.line(550, 695, 550, 665 - (len(transaction_data) * 24))  # Right border

    # Draw a line below the column headers (extending across the page width)
    p.line(50, 675, 550, 675)  # Line below headers

    # Initialize the Y position for the rows
    y = 655
    total_amount = 0

    # Loop through the transaction data and draw each row
    for i, item in enumerate(transaction_data, start=1):
        product = Product.objects.get(id=item['product_id'])
        quantity = int(item['quantity'])
        price = product.price
        total_price = quantity * price
        total_amount += total_price

        # Draw the product details in their respective columns
        p.drawString(60, y, str(i))           # Serial number
        p.drawString(110, y, product.name)    # Adjusted X position for Product
        p.drawString(260, y, str(quantity))   # Adjusted X position for Quantity
        p.drawString(360, y, f"{price:.2f}")  # Adjusted X position for Price
        p.drawString(460, y, f"{total_price:.2f}") # Adjusted X position for Total

        # Move to the next line
        y -= 20

    # Draw the total amount below the table
    p.line(50, y - 0, 550, y - 0)  # Line above total amount
    p.drawString(360, y - 35, "Total Amount:")
    p.drawString(460, y - 35, f"{total_amount:.2f}")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and return it.
    buffer.seek(0)
    return buffer
def submit_transaction(request, id):
    customer = get_object_or_404(Customer, id=id)
    mobile = customer.phone_number
    transcode = generate_unique_transaction_id(customer, mobile)

    if request.method == 'POST':
        transaction_data = request.POST.get('transactionData')

        if not transaction_data:
            return HttpResponseBadRequest("No transaction data provided.")

        try:
            transaction_data = json.loads(transaction_data)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid transaction data.")

        for i, item in enumerate(transaction_data):
            product = Product.objects.get(id=item['product_id'])
            quantity = int(item['quantity'])
            transaction_id = f"{transcode}-{i}"  # Unique transaction ID
            transcode = transcode  # Example transcode

            Transaction_Sale.objects.create(
                transaction_id=transaction_id,
                transcode=transcode,
                customer=customer,
                product=product,
                quantity=quantity
            )

        # Generate the PDF bill
        pdf_buffer = generate_pdf_bill(transaction_data, transcode, customer)

        # Return the PDF file as a response
        return FileResponse(pdf_buffer, as_attachment=True, filename=f"bill_{transcode}.pdf")

    # If not a POST request, redirect to 'bview' with the customer ID
    return redirect('bview', id=id)
# def submit_transaction(request, id):
#     customer = get_object_or_404(Customer, id=id)
#     mobile = customer.phone_number
#     transcode = generate_unique_transaction_id(customer, mobile)
    
#     if request.method == 'POST':
#         transaction_data = request.POST.get('transactionData')

#         if not transaction_data:
#             return HttpResponseBadRequest("No transaction data provided.")

#         try:
#             transaction_data = json.loads(transaction_data)
#         except json.JSONDecodeError:
#             return HttpResponseBadRequest("Invalid transaction data.")

#         for i, item in enumerate(transaction_data):
#             product = Product.objects.get(id=item['product_id'])
#             quantity = int(item['quantity'])
#             transaction_id = f"{transcode}-{i}"  # Unique transaction ID
#             transcode = transcode  # Example transcode

#             Transaction_Sale.objects.create(
#                 transaction_id=transaction_id,
#                 transcode=transcode,
#                 customer=customer,
#                 product=product,
#                 quantity=quantity
#             )

#         # Redirect to 'bview' with the customer ID
#         return redirect('bview', id=id)

#     # If not a POST request, redirect to 'bview' with the customer ID
#     return redirect('bview', id=id)

def purchase_form_view(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    products = Product.objects.all()
    return render(request, 'Billingapp/Purchaseform.html', {'products': products, 'supplier': supplier})


def submit_purchase_transaction(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    mobile = supplier.phone_number
    transcode = generate_unique_transaction_id(supplier, mobile)

    if request.method == 'POST':
        transaction_data = request.POST.get('transactionData')

        if not transaction_data:
            return HttpResponseBadRequest("No transaction data provided.")

        try:
            transaction_data = json.loads(transaction_data)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid transaction data.")

        for i, item in enumerate(transaction_data):
            product = Product.objects.get(id=item['product_id'])
            quantity = int(item['quantity'])
            transaction_id = f"{transcode}-{i}"  # Unique transaction ID

            Transaction_Buy.objects.create(
                transaction_id=transaction_id,
                transcode=transcode,
                vendor=supplier,
                product=product,
                quantity=quantity
            )

        # Redirect to a view that displays the purchase details, e.g., purchase details view
        return redirect('Pview', id=id)

    # If not a POST request, redirect to the purchase form with the supplier ID
    return redirect('Pview', id=id)


