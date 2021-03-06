from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin

from accountapp.decorators import account_ownership_required
from accountapp.forms import AccountCreationForm
from accountapp.models import HelloWorld
from articleapp.models import Article


# @login_required
# def hello_world(request):
#
#         if request.method == 'POST':
#             temp = request.POST.get('hello_world_input')
#             new_hello_world = HelloWorld()
#             new_hello_world.text = temp
#             new_hello_world.save()
#
#             return HttpResponseRedirect(reverse('accountapp:hello_world'))
#
#             # hello_world_list = HelloWorld.objects.all()
#             # return render(request, 'accountapp/hello_world.html', context={'hello_kkc_list':  hello_world_list})
#         else:
#             hello_world_list = HelloWorld.objects.all()
#             return render(request, 'accountapp/hello_world.html', context={'hello_kkc_list':  hello_world_list})
#





class AccountCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    # success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/create.html'

    def get_success_url(self):
        return reverse('accountapp:detail', kwargs={'pk': self.object.pk})

class AccountDetailView(DetailView, MultipleObjectMixin):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'

    paginate_by = 20

    def get_context_data(self, **kwargs):
        article_list = Article.objects.filter(writer=self.object)
        return super().get_context_data(object_list=article_list, **kwargs)


has_decorator = [login_required, account_ownership_required]


@method_decorator(has_decorator, 'get')
@method_decorator(has_decorator, 'post')
class AccountUpdateView(UpdateView):
    model = User
    context_object_name = 'target_user'
    form_class = AccountCreationForm
    # success_url = reverse_lazy('accountapp:hello_world')
    template_name = 'accountapp/update.html'

    def get_success_url(self):
        return reverse('accountapp:detail', kwargs={'pk': self.object.pk})

@method_decorator(has_decorator, 'get')
@method_decorator(has_decorator, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('articleapp:list')
    template_name = 'accountapp/delete.html'
