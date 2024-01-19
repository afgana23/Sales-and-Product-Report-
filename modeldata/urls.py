from django.urls import path
from . import views


urlpatterns = [
    path('',views.home_page,name="index"),
      path('tabledata/',views.table_data,name="tabledata"),  
       path('savedata/',views.save_data,name="savedata"),  
       path('updatedata/<int:cid>',views.update_data,name="updatedata"),
        path('dashboard/',views.dashboard_data,name="dashboard"),   
           path('singledata/<int:cid>',views.single_data,name="singledata"),   
           path('price',views.calculate_price,name="price"), 
           path('sale/<int:cid>',views.make_sale,name="sale"), 
            path('salereport/',views.sale_report,name="salereport"), 
            path('select/',views.asset_selected_view,name="select"), 
            path('login/',views.login_page,name="login"), 
              path('logout/',views.logout_page,name="logout"), 
              path('signup/', views.signup_user, name='signup'),
              path('order/<int:cid>', views.order_page, name='order'),
              

]