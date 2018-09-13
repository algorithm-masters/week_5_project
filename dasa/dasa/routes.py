from pyramid_restful.routers import ViewSetRouter

from .views.auth import AuthAPIView
from .views.nltk_output import NLTKAPIView
from .views.nltk_admin import NLTKAPIAdmin
from .views.nltk_charts import NLTKAPICharts
from .views.get_users import GetAPIUsers

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    router = ViewSetRouter(config, trailing_slash=False)
    router.register('api/v1/auth/{auth}', AuthAPIView, 'auth')
    router.register('api/v1/analysis', NLTKAPIView, 'analysis')
    router.register('api/v1/users', GetAPIUsers, 'users_list')
    router.register('api/v1/charts/{graph_type}', NLTKAPICharts, 'charts')
    router.register('api/v1/admin/delete/{user_id}', NLTKAPIAdmin, 'user_delete')
    router.register('api/v1/admin/{graph_type}/{user_id}', NLTKAPIAdmin, 'admin_visuals')
