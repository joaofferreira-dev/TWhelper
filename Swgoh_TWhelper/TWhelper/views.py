from django.shortcuts import render, redirect
from .models import Team, Rooster, ZetasNames
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from TWhelper.tasks import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import Edit_Team, Mandalorians_actions
from rest_framework import viewsets, generics, status
from django.urls import reverse_lazy
from .serializers import TeamSerializer, RoosterSerializer
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.forms.utils import ErrorList
from django import forms
from django.urls import reverse

from model_utils import Choices
from django.db.models import Q
from rest_framework.response import Response
import xlwt
import datetime
from django.utils import timezone

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

"""
Defines order of column by which the table is sorted
"""
ORDER_COLUMN_CHOICES = Choices(
    ('0', 'toon1__name'),
    ('1', 'toon1__num_zetas'),
    ('2', 'toon1__speed'),
    ('3', 'toon2__name'),
    ('4', 'toon2__num_zetas'),
    ('5', 'toon2__speed'),
    ('6', 'toon3__name'),
    ('7', 'toon3__num_zetas'),
    ('8', 'toon3__speed'),
    ('9', 'toon4__name'),
    ('10', 'toon4__num_zetas'),
    ('11', 'toon4__speed'),
    ('12', 'toon5__name'),
    ('13', 'toon5__num_zetas'),
    ('14', 'toon5__speed'),
    ('15', 'Totalgp'),
    ('16', 'date_posted'),
    ('17', 'author_username')
    # ('12', 'assignment'),
)


def home(request):

    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
            else:
                return HttpResponse("Fuck you.")
            return redirect('teams/')
    else:
        form = AuthenticationForm()
    return render(request, 'TWhelper/home.html', {'form': form})


@login_required
def teams(request):
    username = request.user.username

    context = {
        'teams_test': Team.objects.filter(author__username=username)
    }
    return render(request, 'TWhelper/teams.html', context)


# @login_required
@staff_member_required
def mandalorians(request):

    if request.method == 'POST':
        form = Mandalorians_actions(data=request.POST)

        if form.is_valid():
            val = form.cleaned_data.get("btn")
            print("VALLLL:", val)

            if val == 'Reset':
                Team.objects.update(assignment='1')
                print("All teams placement were RESET!")

            if val == 'Colocações':
                print("DO THE COLOCATIONS")

    else:
        form = Mandalorians_actions()

    return render(request, 'TWhelper/mandalorians.html')


def teste(request):
    return render(request, 'TWhelper/teste.html')


@staff_member_required
def export_teams_xls(request):
    """
    Description: Handles the creation of a excel file containing information of
    availableteams
    """
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="teams.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Toon1', 'z', 'Spd', 'Toon2', 'z', 'Spd', 'Toon3', 'z', 'Spd',
               'Toon4', 'z', 'Spd', 'Toon5', 'z', 'Spd', 'Totalgp', 'Player']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Team.objects.all().values_list('toon1__name', 'toon1__num_zetas', 'toon1__speed',
                                          'toon2__name', 'toon2__num_zetas', 'toon2__speed',
                                          'toon3__name', 'toon3__num_zetas', 'toon3__speed',
                                          'toon4__name', 'toon4__num_zetas', 'toon4__speed',
                                          'toon5__name', 'toon5__num_zetas', 'toon5__speed',
                                          'Totalgp', 'author_username')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


class TeamsViewSet(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def query_teams_by_args(**kwargs):
        draw = int(kwargs.get('draw', None)[0])
        length = int(kwargs.get('length', None)[0])
        start = int(kwargs.get('start', None)[0])
        search_value = kwargs.get('search[value]', None)[0]
        order_column = kwargs.get('order[0][column]', None)[0]
        order = kwargs.get('order[0][dir]', None)[0]

        queryset = Team.objects.all()
        total = queryset.count()

        order_column = ORDER_COLUMN_CHOICES[order_column]
        # django orm '-' -> desc
        if order == 'desc':
            order_column = '-' + order_column

        if search_value:
            queryset = queryset.filter(Q(toon1__name__icontains=search_value) |
                                       Q(toon2__name__icontains=search_value) |
                                       Q(toon3__name__icontains=search_value) |
                                       Q(toon4__name__icontains=search_value) |
                                       Q(toon5__name__icontains=search_value) |
                                       Q(author_username__icontains=search_value))

        count = queryset.count()
        queryset = queryset.order_by(order_column)[start:start + length]

        return {
            'items': queryset,
            'count': count,
            'total': total,
            'draw': draw
        }

    def list(self, request):
        try:
            teams = TeamsViewSet.query_teams_by_args(**request.query_params)
            serializer = TeamSerializer(teams['items'], many=True)
            result = dict()
            result['data'] = serializer.data
            result['draw'] = teams['draw']
            result['recordsTotal'] = teams['total']
            result['recordsFiltered'] = teams['count']
            return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

        except Exception as e:
            return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)


class TeamsPostView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Team.objects.all()
    # lookup_field = 'pk'
    serializer_class = TeamSerializer


@login_required
def mandalorians_json(request):
    teams = Team.objects.all()
    data = [team.to_dict_json() for team in teams]

    response = {'data': data}

    return JsonResponse(response)


class TeamListView(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'TWhelper/teams_edit.html'
    context_object_name = 'teams_test'

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
        username = self.request.user

        context = {
            'teams_test': Team.objects.filter(author__username=username),
            'rooster': Rooster.objects.filter(player__username=username),
        }

        return context


class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team


class TeamCreateView(LoginRequiredMixin, CreateView):
    model = Team
    fields = ['toon1', 'toon2', 'toon3', 'toon4', 'toon5']

    def get_context_data(self, **kwargs):
            # Call the base implementation first to get a context
        context = super(TeamCreateView, self).get_context_data(**kwargs)
        username = self.request.user

        context = {
            'teams_test': Team.objects.filter(author__username=username),
            'rooster': Rooster.objects.filter(player__username=username),
            'form': Edit_Team(user=username)
        }

        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Every toon must be different!')
        return self.render_to_response(self.get_context_data(form=form))


class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Team
    fields = ['toon1', 'toon2', 'toon3', 'toon4', 'toon5']

    # Capture url PrimaryKey
    def to_python(self, pk):
        return int(pk)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TeamUpdateView, self).get_context_data(**kwargs)
        username = self.request.user

        current_team = Team.objects.get(id=int(self.kwargs.get('pk')))

        context = {
            'teams_test': Team.objects.filter(author__username=username),
            'rooster': Rooster.objects.filter(player__username=username),
            'form': Edit_Team(user=username, current_team=current_team),
            'pk_current': int(self.kwargs.get('pk'))
        }

        return context

    def form_valid(self, form):
        if form.is_valid():
            form.instance.author = self.request.user
            return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Every toon must be different!')
        return self.render_to_response(self.get_context_data(form=form))

    def test_func(self):
        team = self.get_object()
        if self.request.user == team.author:
            return True
        return False


class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Team
    success_url = reverse_lazy('TWhelper-editteams')

    # No confirm delete
    def test_func(self):
        team = self.get_object()
        if self.request.user == team.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TeamDeleteView, self).get_context_data(**kwargs)
        username = self.request.user

        context = {
            'teams_test': Team.objects.filter(author__username=username).filter(id=self.kwargs.get('pk')),
            'rooster': Rooster.objects.filter(player__username=username),
            'form': Edit_Team()
        }

        return context


@csrf_exempt
def tasks(request):
    if request.method == 'POST':
        return _post_tasks(request)
    else:
        return JsonResponse({}, status=405)


def _post_tasks(request):
    message = request.POST['message']
    logger.debug('calling demo_task. message={0}'.format(message))
    update_db()
    return JsonResponse({}, status=302)
