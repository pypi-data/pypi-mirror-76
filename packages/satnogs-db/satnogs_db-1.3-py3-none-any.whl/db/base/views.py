"""Base django views for SatNOGS DB"""
import logging
from datetime import timedelta

from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import OperationalError
from django.db.models import Count, Max, Prefetch, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from db.base.forms import SatelliteModelForm, TransmitterModelForm, \
    TransmitterUpdateForm
from db.base.helpers import get_apikey
from db.base.models import SERVICE_TYPE, TRANSMITTER_STATUS, \
    TRANSMITTER_TYPE, DemodData, Mode, Satellite, Transmitter, \
    TransmitterEntry, TransmitterSuggestion
from db.base.tasks import export_frames
from db.base.utils import cache_statistics, millify, read_influx

LOGGER = logging.getLogger('db')


def superuser_check(user):
    """Returns True if user is a superuser, for use with @user_passes_test
    """
    return user.is_superuser


def home(request):
    """View to render home page.

    :returns: base/home.html
    """
    newest_sats = Satellite.objects.all().order_by('-id')[:5].prefetch_related(
        Prefetch(
            'transmitter_entries',
            queryset=Transmitter.objects.all(),
            to_attr='approved_transmitters'
        ),
        Prefetch(
            'transmitter_entries',
            queryset=TransmitterSuggestion.objects.all(),
            to_attr='suggested_transmitters'
        )
    )
    latest_data = Satellite.objects.annotate(latest=Max('telemetry_data__pk')
                                             ).order_by('-latest')[:5].prefetch_related(
                                                 Prefetch(
                                                     'transmitter_entries',
                                                     queryset=Transmitter.objects.all(),
                                                     to_attr='approved_transmitters'
                                                 )
                                             )  # noqa: E126 flake8 and yapf disagree

    # Calculate latest contributors
    date_from = timezone.now() - timedelta(days=1)
    latest_submitters = DemodData.objects.filter(timestamp__gte=date_from
                                                 ).values('station').annotate(c=Count('station')
                                                                              ).order_by('-c')

    cached_stats = cache.get('stats_transmitters')
    if not cached_stats:
        try:
            cache_statistics()
            cached_stats = cache.get('stats_transmitters')
        except OperationalError:
            pass
    return render(
        request, 'base/home.html', {
            'newest_sats': newest_sats,
            'latest_data': latest_data,
            'latest_submitters': latest_submitters,
            'statistics': cached_stats
        }
    )


def transmitters_list(request):
    """View to render transmitters list page.

    :returns: base/transmitters.html
    """
    transmitters = Transmitter.objects.prefetch_related('satellite', 'downlink_mode')

    return render(request, 'base/transmitters.html', {'transmitters': transmitters})


def robots(request):
    """robots.txt handler

    :returns: robots.txt
    """
    data = render(request, 'robots.txt', {'environment': settings.ENVIRONMENT})
    response = HttpResponse(data, content_type='text/plain; charset=utf-8')
    return response


def satellites(request):
    """View to render satellites page.

    :returns: base/satellites.html
    """
    satellite_objects = Satellite.objects.prefetch_related(
        'operator',
        Prefetch(
            'transmitter_entries',
            queryset=Transmitter.objects.all(),
            to_attr='approved_transmitters'
        )
    )
    suggestion_count = TransmitterSuggestion.objects.count()
    contributor_count = User.objects.filter(is_active=1).count()
    cached_stats = cache.get('stats_transmitters')
    if not cached_stats:
        try:
            cache_statistics()
            cached_stats = cache.get('stats_transmitters')
        except OperationalError:
            pass
    return render(
        request, 'base/satellites.html', {
            'satellites': satellite_objects,
            'statistics': cached_stats,
            'contributor_count': contributor_count,
            'suggestion_count': suggestion_count
        }
    )


def satellite(request, norad):
    """View to render satellite page.

    :returns: base/satellite.html
    """
    satellite_obj = get_object_or_404(Satellite.objects, norad_cat_id=norad)
    transmitter_suggestions = TransmitterSuggestion.objects.filter(satellite=satellite_obj)
    for suggestion in transmitter_suggestions:
        try:
            original_transmitter = satellite_obj.transmitters.get(uuid=suggestion.uuid)
            suggestion.transmitter = original_transmitter
        except Transmitter.DoesNotExist:
            suggestion.transmitter = None
    modes = Mode.objects.all()
    types = TRANSMITTER_TYPE
    services = SERVICE_TYPE
    statuses = TRANSMITTER_STATUS
    sat_cache = cache.get(satellite_obj.id)
    frame_count = 0
    if sat_cache is not None:
        frame_count = sat_cache['count']

    try:
        latest_frame = DemodData.objects.filter(satellite=satellite_obj).order_by('-id')[0]
    except (ObjectDoesNotExist, IndexError):
        latest_frame = ''

    try:
        # pull the last 5 observers and their submission timestamps for this satellite
        recent_observers = DemodData.objects.filter(satellite=satellite_obj) \
            .values('observer').annotate(latest_payload=Max('timestamp')) \
            .order_by('-latest_payload')[:5]
    except (ObjectDoesNotExist, IndexError):
        recent_observers = ''

    return render(
        request, 'base/satellite.html', {
            'satellite': satellite_obj,
            'transmitter_suggestions': transmitter_suggestions,
            'modes': modes,
            'types': types,
            'services': services,
            'statuses': statuses,
            'latest_frame': latest_frame,
            'frame_count': frame_count,
            'mapbox_token': settings.MAPBOX_TOKEN,
            'recent_observers': recent_observers,
            'badge_telemetry_count': millify(satellite_obj.telemetry_data_count)
        }
    )


@login_required
def request_export(request, norad, period=None):
    """View to request frames export download.

    This triggers a request to collect and zip up the requested data for
    download, which the user is notified of via email when the celery task is
    completed.
    :returns: the originating satellite page
    """
    get_object_or_404(Satellite, norad_cat_id=norad)
    export_frames.delay(norad, request.user.id, period)
    messages.success(
        request, ('Your download request was received. '
                  'You will get an email when it\'s ready')
    )
    return redirect(reverse('satellite', kwargs={'norad': norad}))


# <cshields> leaving this in place for reference while the New UI is fixed up
# and the functionality below is moved into new modals accordingly.
# @login_required
# @require_POST
# def transmitter_suggestion(request):
#     """View to process transmitter suggestion form

#     :returns: the originating satellite page unless an error occurs
#     """
#     transmitter_form = TransmitterEntryForm(request.POST)
#     if transmitter_form.is_valid():
#         transmitter = transmitter_form.save(commit=False)
#         transmitter.user = request.user
#         transmitter.reviewed = False
#         transmitter.approved = False
#         uuid = transmitter_form.cleaned_data['uuid']
#         if uuid:
#             transmitter.uuid = uuid
#         transmitter.save()

#         # Notify admins
#         admins = User.objects.filter(is_superuser=True)
#         site = get_current_site(request)
#         subject = '[{0}] A new suggestion for {1} was submitted'.format(
#             site.name, transmitter.satellite.name
#         )
#         template = 'emails/new_transmitter_suggestion.txt'
#         saturl = '{0}{1}'.format(
#             site.domain,
#             reverse('satellite', kwargs={'norad': transmitter.satellite.norad_cat_id})
#         )
#         data = {
#             'satname': transmitter.satellite.name,
#             'saturl': saturl,
#             'sitedomain': site.domain,
#             'contributor': transmitter.user
#         }
#         message = render_to_string(template, {'data': data})
#         for user in admins:
#             try:
#                 user.email_user(subject, message, from_email=settings.DEFAULT_FROM_EMAIL)
#             except Exception:  # pylint: disable=W0703
#                 LOGGER.error('Could not send email to user', exc_info=True)

#         messages.success(
#             request,
#             ('Your transmitter suggestion was stored successfully. '
#              'Thanks for contibuting!')
#         )
#         redirect_page = redirect(
#             reverse('satellite', kwargs={'norad': transmitter.satellite.norad_cat_id})
#         )
#     else:
#         LOGGER.error(
#             'Suggestion form was not valid %s',
#             format(transmitter_form.errors),
#             exc_info=True,
#             extra={
#                 'form': transmitter_form.errors,
#             }
#         )
#         messages.error(request, 'We are sorry, but some error occured :(')
#         redirect_page = redirect(reverse('home'))

#     return redirect_page


@login_required
@require_POST
@user_passes_test(superuser_check)
def transmitter_suggestion_handler(request):
    """Returns the Satellite page after approving or rejecting a suggestion

    :returns: Satellite page
    """
    transmitter = TransmitterSuggestion.objects.get(uuid=request.POST['uuid'])
    if 'approve' in request.POST:
        transmitter.approved = True
        messages.success(request, ('Transmitter approved.'))
    elif 'reject' in request.POST:
        transmitter.approved = False
        messages.success(request, ('Transmitter rejected.'))
    transmitter.reviewed = True
    transmitter.created = timezone.now()
    transmitter.user = request.user

    # Need to determine if we will attribute the suggestion or the approval
    # transmitter.user = request.user

    transmitter.save()

    # the way we handle suggestions in admin is to update the suggestion as
    # reviewed and save a new object. This feels hacky but preserves the
    # admin workflow
    TransmitterSuggestion.objects.filter(uuid=request.POST['uuid']).update(
        reviewed=True, approved=transmitter.approved
    )
    redirect_page = redirect(
        reverse('satellite', kwargs={'norad': transmitter.satellite.norad_cat_id})
    )
    return redirect_page


def about(request):
    """View to render about page.

    :returns: base/about.html
    """
    return render(request, 'base/about.html')


def satnogs_help(request):
    """View to render help modal. Have to avoid builtin 'help' name

    :returns: base/modals/help.html
    """
    return render(request, 'base/modals/satnogs_help.html')


def search(request):
    """View to render search page.

    :returns: base/search.html
    """
    query_string = ''
    results = Satellite.objects.none()
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

    if query_string:
        results = Satellite.objects.filter(
            Q(name__icontains=query_string) | Q(names__icontains=query_string)
            | Q(norad_cat_id__icontains=query_string)  # noqa: W503 google W503 it is evil
        ).order_by('name').prefetch_related(
            Prefetch(
                'transmitter_entries',
                queryset=Transmitter.objects.all(),
                to_attr='approved_transmitters'
            )
        )

    if results.count() == 1:
        return redirect(reverse('satellite', kwargs={'norad': results[0].norad_cat_id}))

    return render(request, 'base/search.html', {'results': results, 'q': query_string})


def stats(request):
    """View to render stats page.

    :returns: base/stats.html
    """
    cached_satellites = []
    ids = cache.get('satellites_ids')
    observers = cache.get('stats_observers')
    suggestion_count = TransmitterSuggestion.objects.count()
    contributor_count = User.objects.filter(is_active=1).count()
    cached_stats = cache.get('stats_transmitters')
    if not ids or not observers:
        try:
            cache_statistics()
            cached_stats = cache.get('stats_transmitters')
            ids = cache.get('satellites_ids')
            observers = cache.get('stats_observers')
        except OperationalError:
            pass
    for sid in ids:
        stat = cache.get(sid['id'])
        cached_satellites.append(stat)

    return render(
        request, 'base/stats.html', {
            'satellites': cached_satellites,
            'observers': observers,
            'statistics': cached_stats,
            'contributor_count': contributor_count,
            'suggestion_count': suggestion_count,
        }
    )


def statistics(request):
    """Triggers a refresh of cached statistics if the cache does not exist

    :returns: JsonResponse of statistics
    """
    cached_stats = cache.get('stats_transmitters')
    if not cached_stats:
        cache_statistics()
        cached_stats = []
    return JsonResponse(cached_stats, safe=False)


@login_required
def users_edit(request):
    """View to render user settings page.

    :returns: base/users_edit.html
    """
    token = get_apikey(request.user)
    return render(request, 'base/modals/users_edit.html', {'token': token})


def recent_decoded_cnt(request, norad):
    """Returns a query of InfluxDB for a count of points across a given measurement
    (norad) over the last 30 days, with a timestamp in unixtime.

    :returns: JSON of point counts as JsonResponse
    """
    results = read_influx(norad)
    return JsonResponse(results, safe=False)


class TransmitterCreateView(LoginRequiredMixin, BSModalCreateView):
    """A django-bootstrap-modal-forms view for creating transmitter suggestions"""
    template_name = 'base/modals/transmitter_create.html'
    model = TransmitterEntry
    form_class = TransmitterModelForm
    success_message = 'Your transmitter suggestion was stored successfully and will be \
                       reviewed by a moderator. Thanks for contibuting!'

    satellite = Satellite()
    user = User()

    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `Satellite` instance exists first
        """
        self.satellite = get_object_or_404(Satellite, pk=kwargs['satellite_pk'])
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Overridden to add the `Satellite` relation to the `Transmitter` instance.
        """
        form.instance.satellite = self.satellite
        form.instance.user = self.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class TransmitterUpdateView(LoginRequiredMixin, BSModalUpdateView):
    """A django-bootstrap-modal-forms view for updating transmitter entries"""
    template_name = 'base/modals/transmitter_update.html'
    model = TransmitterEntry
    form_class = TransmitterUpdateForm
    success_message = 'Your transmitter suggestion was stored successfully and will be \
                       reviewed by a moderator. Thanks for contibuting!'

    user = User()

    def get_initial(self):
        initial = {}
        initial['created'] = timezone.now()
        return initial

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')


class SatelliteUpdateView(PermissionRequiredMixin, BSModalUpdateView):
    """A django-bootstrap-modal-forms view for updating satellite fields"""
    permission_required = 'base.change_satellite'
    model = Satellite
    template_name = 'base/modals/satellite_update.html'
    form_class = SatelliteModelForm
    success_message = 'Satellite was updated.'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
