from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import make_naive
from django.utils import timezone
from .models import Poll, PollOption, Vote
from .forms import PollForm, OptionForm,PollOptionForm
from django.contrib import messages
import datetime

from django.forms import inlineformset_factory
# Create your views here.

# ------------------------------
# ADMIN VIEWS
# ------------------------------

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_poll(request):
    # Admin View: Create Poll
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        option_form = OptionForm(request.POST)
        if poll_form.is_valid() and option_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.created_by = request.user
            poll.save()

            options = []
            for i in range(1, 5):
                opt = option_form.cleaned_data.get(f'option{i}')
                if opt:
                    if opt in options:
                        messages.error(request, 'Duplicate option detected.')
                        poll.delete()
                        return redirect('create_poll')
                    options.append(opt)
                    PollOption.objects.create(poll=poll, text=opt)

            return redirect('admin_poll_list')
    else:
        poll_form = PollForm()
        option_form = OptionForm()
    return render(request, 'polls/create_poll.html', {'poll_form': poll_form, 'option_form': option_form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_poll_list(request):
    # Admin View: List All Polls
    polls = Poll.objects.all()
    for poll in polls:
        if not poll.is_closed and make_naive(poll.close_time) < datetime.datetime.now():
            poll.is_closed = True
            poll.save()
    return render(request, 'polls/admin_poll_list.html', {'polls': polls})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_poll(request, poll_id):
    # Admin View: Delete Poll
    poll = get_object_or_404(Poll, id=poll_id)
    poll.delete()
    return redirect('admin_poll_list')

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_poll(request, poll_id):
    # Admin View: Edit Poll
    poll = get_object_or_404(Poll, id=poll_id)
    PollOptionFormSet = inlineformset_factory(Poll,PollOption,fields=('text',),extra=0,can_delete=False)
    poll_form = PollForm(request.POST or None, instance=poll)
    formset = PollOptionFormSet(request.POST or None, instance=poll)
    if request.method == 'POST' and poll_form.is_valid():
        if make_naive(poll.close_time) < datetime.datetime.now():
            poll.is_closed = True
        else:
            poll.is_closed = False
        poll.save()
        print("Poll manually closed")
        poll_form.save()
        return redirect('admin_poll_list')
    return render(request, 'polls/edit_poll.html', {'poll_form': poll_form, 'poll': poll, 'formset':formset })


@login_required
@user_passes_test(lambda u: u.is_staff)
def poll_results_admin(request, poll_id):
    # Admin View: View Poll Results (only after voting and poll closure
    poll = get_object_or_404(Poll, id=poll_id)
    # print(make_naive(poll.close_time))
    # print(datetime.datetime.now())
    if not poll.is_closed and make_naive(poll.close_time) < datetime.datetime.now():
        poll.is_closed = True
        poll.save()
        print("Poll manually closed")

    results = []
    for option in poll.options.all():
        count = Vote.objects.filter(option=option).count()
        results.append((option.text, count))
    return render(request, 'polls/results.html', {'poll': poll, 'results': results})



# ------------------------------
# USER VIEWS
# ------------------------------

@login_required
@user_passes_test(lambda u: not u.is_staff)
def poll_list(request):
    # User View: List Open Polls
    now = timezone.now()
    polls = Poll.objects.all()
    for poll in polls:
        if not poll.is_closed and make_naive(poll.close_time) < datetime.datetime.now():
            poll.is_closed = True
            poll.save()
    polls = Poll.objects.filter()
    return render(request, 'polls/poll_list.html', {'polls': polls})

@login_required
@user_passes_test(lambda u: not u.is_staff)
def vote_poll(request, poll_id):
    # User View: Vote in a Poll
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.is_closed and make_naive(poll.close_time) < datetime.datetime.now():
        poll.is_closed = True
        poll.save()

    if not poll.is_open():
        return redirect('poll_results_user', poll_id=poll_id)

    if Vote.objects.filter(user=request.user, poll=poll).exists():
        return render(request, 'polls/already_voted.html')

    if request.method == 'POST':
        option_id = request.POST.get('option')
        if option_id:
            option = get_object_or_404(PollOption, id=option_id, poll=poll)
            Vote.objects.create(user=request.user, poll=poll, option=option)
            return redirect('poll_list')
    return render(request, 'polls/vote.html', {'poll': poll})

@login_required
@user_passes_test(lambda u: not u.is_staff)
def poll_results_user(request, poll_id):
    # User View: View Poll Results (only after voting and poll closure)
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.is_closed and make_naive(poll.close_time) < datetime.datetime.now():
        poll.is_closed = True
        poll.save()

    results = []
    for option in poll.options.all():
        count = Vote.objects.filter(option=option).count()
        results.append((option.text, count))
    print(poll)
    
    return render(request, 'polls/closed.html', {'poll': poll, 'results': results})
