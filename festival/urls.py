from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("api/data", views.api_data),
    path("api/login", views.api_login),
    path("api/change-password", views.api_change_password),
    path("api/settings", views.api_update_settings),

    path("api/schedule", views.api_schedule_create),
    path("api/schedule/<int:item_id>", views.api_schedule_delete),

    path("api/collections", views.api_collections_create),
    path("api/collections/<int:item_id>", views.api_collections_delete),

    path("api/expenditures", views.api_expenditures_create),
    path("api/expenditures/<int:item_id>", views.api_expenditures_delete),
]
