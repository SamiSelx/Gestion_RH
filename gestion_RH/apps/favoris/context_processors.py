from apps.app.models import Favoris

def favoris_context(request):
    if request.user.is_authenticated:
        favoris_list = Favoris.objects.filter(user=request.user)
        return {'favoris_list': favoris_list}
    return {}