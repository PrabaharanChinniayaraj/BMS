from django.urls import path

from . import views

urlpatterns = [
 
 
    path('', views.homepage, name='homepage'),
    path('home/', views.home, name='home'),
    path('Login/',views.user_login,name='Login'),
    path('user_register/', views.user_register, name='user_register'),
    path('register/', views.Customerregister, name='register'),
    # path('salesf1/<int:id>/', views.billing_form, name='salesf1'),
    path('Vendor_register/', views.Vendor_register, name='Vendor_register'),
    path('Purchase/<int:id>/', views.Purchase_billing_form, name='Purchase'),
    path('logout/',views.logout_page,name='logout'),
    path('Stock',views.Stock_Detail,name='Stock'),
    path('Orders',views.Order_Detail,name='Orders'),
    path('Transactions',views.Transactions,name='Transactions'),
    path('Salesummary',views.Transactions_summary,name='Salesummary'),
    path('Detailing/<str:transcode>/',views.delailing_view, name='Detailing'),
    path('Buysummary',views.Buy_summary,name='Buysummary'),
    path('Buying/<str:transcode>/',views.Buying_view, name='Buying'),
    path('Sellingqty/',views.Product_Sale_view, name='Sellingqty'),
    path('top-customers/', views.top_customers, name='top-customers'),
    path('Message/', views.send_whatsapp_message, name='Message'),
    path('profit-report/',views. profit_report, name='profit-report'),
    path('bform/',views. index, name='bform'),
    path('Billing/',views. Billing, name='Billing'),

    path('bview/<int:id>/', views.billing_form_view, name='bview'),
    path('get-product-price/', views.get_product_price, name='get-product-price'),
    path('get_product_buying_price/', views.get_product_buying_price, name='get_product_buying_price'),
    path('salesf/<int:id>/', views.submit_transaction, name='salesf'),

    path('Pview/<int:id>/', views.purchase_form_view, name='Pview'),
    path('Purchasef/<int:id>/', views.submit_purchase_transaction, name='Purchasef'),


    path('edit-customer/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('delete-customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),

    path('edit-vendor/<int:vendor_id>/', views.edit_vendor, name='edit_vendor'),
    path('delete-vendor/<int:vendor_id>/', views.delete_vendor, name='delete_vendor'),

    # path('billing/pdf/<int:customer_id>/', views.generate_bill_pdf, name='generate_bill_pdf'),
  



]



hmtx_views = [
 
    path('search/', views.search_customer, name='search'),
    path('search_vendor/', views.search_Vendor, name='search_vendor'),
    path('get_product_price1/', views.get_product_price1, name='get_product_price1'),
    path('calculate_total_price/', views.calculate_total_price, name='calculate_total_price'),
    
   
]

urlpatterns += hmtx_views