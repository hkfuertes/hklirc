from django.urls import path
from .views import views_lirc, views_mapping

urlpatterns = [
    path('', views_lirc.index, name="index"),
    #path('refresh', views_mapping.update_map, name="refresh_mapping"),
    path('lirc', views_lirc.lircd_remotes, name="lircd_remotes"),
    path('lirc/<remote_file>', views_lirc.lircd_remote, name="lircd_remote"),
    path('lirc/<remote_file>/download', views_lirc.lircd_remote_download, name="lircd_remote_download"),
    path('lirc/<remote_file>/delete', views_lirc.lircd_remote_delete, name="lircd_remote_delete"),
    path('mapping', views_mapping.index, name="mapping_index"),
    path('mapping/<mapping_id>', views_mapping.detail, name="mapping_detail"),
    path('mapping/<mapping_id>/activate', views_mapping.activate, name="mapping_activate"),
    path('mapping/<mapping_id>/delete', views_mapping.delete, name="mapping_delete"),
]