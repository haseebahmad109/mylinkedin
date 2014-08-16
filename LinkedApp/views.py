# Create your views here.

from django.shortcuts import render_to_response
from LinkedApp.forms import UserCreationForm, UserCreationForm2, LoginForm, AdvanceSearchForm, ProfilePic
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from LinkedApp.models import User, Invitations, Connection, Notifications, Message, Status, Comment, Like, Forgot_Pass
from django.db.models import Q
from django.conf import settings
import re,json,requests , ntpath
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from os.path import join, normpath
from bs4 import BeautifulSoup
from LinkedApp.simplefunctions import handle_uploaded_file
from random import randint
from django.core.mail import EmailMultiAlternatives
from django.http import Http404



""" Simple Pages """

def whatisLinkedIn(request):
    return render_to_response('screen3(what is linkden page).html', RequestContext(request))


def cookie_policy(request):
    return render_to_response('cookies.html', RequestContext(request))


def user_agreement(request):
    return render_to_response('screen9 (User agreement).html', RequestContext(request))


def privacy_policy(request):
    return render_to_response('privacyPolicy.html', RequestContext(request))


def search_by_country(request):
    return render_to_response('screen10(bu country).html', RequestContext(request))


def default_for_links(request):
    return render_to_response('DefaultForLinks.html', RequestContext(request))


#######################complex dynamic views ############################


def main(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/logged-in-view/')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = authenticate(username=request.POST['email'], password=request.POST['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                    else:
                        return "not activated"
                else:
                    return HttpResponse("<h1>User Cannot be authenticated</h1>")
                args = {}
                args.update(csrf(request))
                args['form'] = UserCreationForm2()

                return HttpResponseRedirect("/reg-step-2/", args)
        else:
            form = UserCreationForm()

        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render_to_response('screen1(main page).html', args , RequestContext(request))


def join_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/default-for-links/')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = authenticate(username=request.POST['email'], password=request.POST['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.user.save()
                    else:
                        return "not activated"
                else:
                    return HttpResponse("<h1>User Cannot be authenticated</h1>")
                args = {}
                args.update(csrf(request))
                args['form'] = UserCreationForm2()

                return HttpResponseRedirect("/reg-step-2/", args)
        else:
            form = UserCreationForm()

        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render_to_response('screen4 (join in).html', args)


def sign_in(request):
    if not request.user.is_authenticated():
        args = {}
        args.update(csrf(request))
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(username=request.POST["username"], password=request.POST["password"])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect('/logged-in-view/')
                    else:
                        args['myErrors'] = "User Not Activated."
                else:
                    args['myErrors'] = "Username or passwords Don't match."
        else:
            form = LoginForm()
        args['form'] = form
        return render_to_response('screen5(sign in).html', args, RequestContext(request))
    else:
        return HttpResponseRedirect('/logged-in-view/');


def reset_password(request):
    return render_to_response('screen6(passwordreset.html', RequestContext(request))


@login_required()
def reg_step_2(request):
    if request.method == 'POST':
        form = UserCreationForm2(request.POST)
        form2 = ProfilePic(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect('/email_api/')
    else:
        form = UserCreationForm2()
        form2 = ProfilePic()

    args = {}
    args.update(csrf(request))
    args['form2'] = form2
    args['form'] = form
    return render_to_response('redistrationFormNo2.html', args, RequestContext(request))


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/sign-in/', RequestContext(request))


@login_required()
def email_api(request):
        args = {}
        args.update(csrf(request))
        return render_to_response('Email_api_step.html', args, RequestContext(request))


@login_required()
def email_sent(request):
        args = {}
        if request.method == 'POST':
            email = request.POST['address']
            domain = re.search("@[\w.]+", email)
            if domain.group() == '@gmail.com':
                return HttpResponseRedirect('/login/google-oauth2')
            elif domain.group() == '@live.com' or domain.group() == '@hotmail.com':
                return HttpResponseRedirect('/login/live')
            elif domain.group() == '@yahoo.com':
                return HttpResponseRedirect('/login/yahoo')
            elif domain.group() == '@facebook.com':
                return HttpResponseRedirect('/login/facebook')
            else:
                args['myErrors'] = "Not Suppported"
                return render_to_response('Email_api_step.html', args, RequestContext(request))

        args['emails'] = []
        if settings.CONTACTS != {}:
            for email in settings.CONTACTS['emails']:
                try:
                    x = User.objects.get(email=email)
                    args['emails'].append(x)
                except User.DoesNotExist:
                    myUser = None
        return render_to_response('email_sent.html', args, RequestContext(request))


@login_required()
def invite_friends(request):
        args = {}
        args['emails'] = []
        if settings.CONTACTS != {}:
            for email in settings.CONTACTS['emails']:
                try:
                    User.objects.get(email=email)
                except User.DoesNotExist:
                    args['emails'].append(email)
        return render_to_response('invite_friends.html', args, RequestContext(request))


@login_required()
def final_step(request):
        return render_to_response('final_step.html', RequestContext(request))


@login_required()
def upload_image(request):
    if request.method == "POST":
        args = {}
        args['form'] = ProfilePic(request.POST, request.FILES)
        if args['form'].is_valid():
            log_in_user = request.user
            log_in_user.profile_pic = request.FILES['pic']
            log_in_user.save()
            return HttpResponse(log_in_user.profile_pic)
        else:
            return HttpResponse("<p>null</P>")


@login_required()
def get_prof_pic(request):
    arr = {"path": request.user.profile_pic.url}
    return HttpResponse(json.dumps(arr), content_type='application/json')


@login_required()
def search_result_ajax(request):
    if request.GET['search_query']:
        args = {}
        result = []
        keyword = request.GET['search_query']
        list_of_keywords = keyword.split()
        first_keyword = ""
        if list_of_keywords:
            first_keyword = list_of_keywords[0].lower()
        result = User.objects.filter(Q(first_name__iexact=first_keyword)
                                     | Q(email=first_keyword)
                                     | Q(country__icontains=first_keyword)
                                     | Q(last_name__iexact=first_keyword)
                                     | Q(student__School_University__icontains=first_keyword)
                                     | Q(jobseeker__most_recent_job_title__icontains=first_keyword)
                                     | Q(jobseeker__MostRecentCompany__icontains=first_keyword)
                                     | Q(employed__Job_title__icontains=first_keyword)
                                     | Q(employed__Company__icontains=first_keyword)).distinct()

        for keyword in list_of_keywords:
            result = result.filter(Q(first_name__iexact=keyword)
                                   | Q(email=keyword)
                                   | Q(country__icontains=keyword)
                                   | Q(last_name__iexact=keyword)
                                   | Q(student__School_University__icontains=keyword)
                                   | Q(jobseeker__most_recent_job_title__icontains=keyword)
                                   | Q(jobseeker__MostRecentCompany__icontains=keyword)
                                   | Q(employed__Job_title__icontains=keyword)
                                   | Q(employed__Company__icontains=keyword))

        args['results'] = result
        return render_to_response('search_result_ajax.html', args, RequestContext(request))


@login_required()
def search_result(request):
    if request.method == "POST":
        first = request.POST["keyword"]
        list_of_keywords = first.split()
        advform = AdvanceSearchForm(request.POST)

        if first:


            #results = User.objects.filter(first_name__iregex=r"\b{0}\b".format(first))
            first_to_search = list_of_keywords[0]
            results = User.objects.filter(Q(first_name__iregex=r"\y{0}\y".format(first_to_search))
                                                    | Q(email__iregex=r"\y{0}\y".format(first_to_search))
                                                    | Q(country__iregex=r"\y{0}\y".format(first_to_search))
                                                    | Q(last_name__iregex=r"\y{0}\y".format(first_to_search))
                                                    | Q(student__School_University__iregex=r"\y{0}\y".format(first_to_search))
                                                    | Q(jobseeker__most_recent_job_title__iregex=r"\y{0}\y".format(first_to_search))
                                                    | Q(jobseeker__MostRecentCompany__iregex=r"\y{0}\y".format(first_to_search))
                                                    | Q(employed__Job_title__iregex=r"\y{0}\y".format(first_to_search))
                                                    | Q(employed__Company__iregex=r"\y{0}\y".format(first_to_search))).distinct()

            for keywords in list_of_keywords:
                results = results.filter(Q(first_name__iregex=r"\y{0}\y".format(keywords))
                                                    | Q(email__iregex=r"\y{0}\y".format(keywords))
                                                    | Q(country__iregex=r"\y{0}\y".format(keywords))
                                                    | Q(last_name__iregex=r"\y{0}\y".format(keywords))
                                                    | Q(student__School_University__iregex=r"\y{0}\y".format(keywords))
                                                    | Q(jobseeker__most_recent_job_title__iregex=r"\y{0}\y".format(keywords))
                                                    | Q(jobseeker__MostRecentCompany__iregex=r"\y{0}\y".format(keywords))
                                                    | Q(employed__Job_title__iregex=r"\y{0}\y".format(keywords))
                                                    | Q(employed__Company__iregex=r"\y{0}\y".format(keywords))).distinct()

        else:
            results = User.objects.all()



        if request.POST["first_name"]:
            first_name_search = request.POST["first_name"]
            list_of_first_names = first_name_search.split()
            for first_names in list_of_first_names:
                results = results.filter(Q(first_name__iregex=r"\y{0}\y".format(first_names)))
        if request.POST["last_name"]:
            last_name_search = request.POST["last_name"]
            list_of_last_names = last_name_search.split()
            for last_names in list_of_last_names:
                results = results.filter(Q(last_name__iregex=r"\y{0}\y".format(last_names)))

        if request.POST["country"]:
            results = results.filter(Q(country__iregex=r"\y{0}\y".format(request.POST["country"])))

        if request.POST["title"]:
            results = results.filter(Q(employed__Job_title__iregex=r"\y{0}\y".format(request.POST["title"])))

        if request.POST["company"]:
            company_search = request.POST["company"]
            list_of_companys = company_search.split()
            for companys in list_of_companys:
                results = results.filter(Q(employed__Company__iregex=r"\y{0}\y".format(companys)))

        if request.POST["school"]:
            school_search = request.POST["school"]
            list_of_schools = school_search.split()
            for schools in list_of_schools:
                results = results.filter(Q(student__School_University__iregex=r"\y{0}\y".format(schools)))



        args1 = {}
        args1['form'] = advform
        args1['results'] = results
        args1.update(csrf(request))


        return render_to_response('search_ajax.html', args1,  RequestContext(request))

    elif request.method == "GET":
        advform = AdvanceSearchForm()
        result = []
        if request.GET != {}:
            keyword = request.GET['search_query']
            list_of_keywords = keyword.split()
            first_keyword = ""
            if list_of_keywords:
                first_keyword = list_of_keywords[0]


            result = User.objects.filter(Q(first_name__iregex=r"\y{0}\y".format(first_keyword))
                                         | Q(email=first_keyword)
                                         | Q(country__iregex=r"\y{0}\y".format(first_keyword))
                                         | Q(last_name__iregex=r"\y{0}\y".format(first_keyword))
                                         | Q(student__School_University__iregex=r"\y{0}\y".format(first_keyword))
                                         | Q(jobseeker__most_recent_job_title__iregex=r"\y{0}\y".format(first_keyword))
                                         | Q(jobseeker__MostRecentCompany__iregex=r"\y{0}\y".format(first_keyword))
                                         | Q(employed__Job_title__iregex=r"\y{0}\y".format(first_keyword))
                                         | Q(employed__Company__iregex=r"\y{0}\y".format(first_keyword))).distinct()

            for keyword in list_of_keywords:
                result = result.filter(Q(first_name__iregex=r"\y{0}\y".format(keyword))
                                         | Q(email=keyword)
                                         | Q(country__iregex=r"\y{0}\y".format(keyword))
                                         | Q(last_name__iregex=r"\y{0}\y".format(keyword))
                                         | Q(student__School_University__iregex=r"\y{0}\y".format(keyword))
                                         | Q(jobseeker__most_recent_job_title__iregex=r"\y{0}\y".format(keyword))
                                         | Q(jobseeker__MostRecentCompany__iregex=r"\y{0}\y".format(keyword))
                                         | Q(employed__Job_title__iregex=r"\y{0}\y".format(keyword))
                                         | Q(employed__Company__iregex=r"\y{0}\y".format(keyword)))

        args = {}
        args['form'] = advform
        args['results'] = result
        args.update(csrf(request))

        return render_to_response('search_Result.html', args,  RequestContext(request))


@login_required()
def connect_invitation_form(request, con=None):
    if con:
        invite = Invitations.objects.filter(receiver_id=con, sender_id=request.user.id)
        if Connection.objects.filter(Q(of_whom=request.user) & Q(with_whom_id=con)):
            settings.MESSAGE = "Already Connected"
            return HttpResponseRedirect('/logged-in-view/')
        try:
            if request.user == User.objects.get(id=con):
                settings.MESSAGE = "cannot connect to yourself"
                return HttpResponseRedirect('/logged-in-view/')
        except User.DoesNotExist:
            raise Http404
        if not invite:
            args = {}
            try:
                args['receiver'] = User.objects.get(id=con)
                args['con'] = con
            except User.DoesNotExist:
                raise Http404
            return render_to_response("connect_invitation.html", args, RequestContext(request))
        else:
            settings.MESSAGE = "Already Pending"
            return HttpResponseRedirect('/logged-in-view/')


@login_required()
def send_invitation(request):
    if request.method == "POST":
        try:
            receiver = User.objects.get(id=request.POST['receiver'])
        except User.DoesNotExist:
            settings.MESSAGE = "not good"
            return HttpResponseRedirect('/logged-in-view/')
        if Invitations.objects.filter(receiver_id=receiver.id, sender_id=request.user.id):
            settings.MESSAGE = "Already Pending"
        elif Connection.objects.filter(Q(of_whom=request.user) & Q(with_whom=receiver)):
            settings.MESSAGE = "Already connected !"
        elif receiver:
            invite = Invitations()
            invite.receiver_id = receiver
            invite.sender_id = request.user
            invite.invitation_message = request.POST['note']
            invite.relationship_type = request.POST['relation']
            invite.save()
            settings.MESSAGE = "Invitation has been sent to " + receiver.get_full_name()
        else:
            settings.MESSAGE = "not good"

    return HttpResponseRedirect('/logged-in-view/')


@login_required()
def accept_or_ignore(request):
    if request.method == "POST":
        query = request.POST['query']
        invite_no = request.POST['invite_no']
        try:
            invitation = Invitations.objects.get(id=invite_no)
        except Invitations.DoesNotExist:
            invitation = None
        response_data = {}
        if invitation and invitation.receiver_id.id == request.user.id:
            if query == "accept":
                new_connection_1 = Connection()
                new_connection_1.of_whom = request.user
                new_connection_1.with_whom = invitation.sender_id
                new_connection_1.related_how = invitation.relationship_type
                new_connection_1.save()
                new_connection_2 = Connection()
                new_connection_2.of_whom = invitation.sender_id
                new_connection_2.with_whom = request.user
                new_connection_2.related_how = invitation.relationship_type
                new_connection_2.save()
                response_data['message'] = invitation.sender_id.get_full_name() + " is added in you connections"
                notification = Notifications()
                notification.of_whom = invitation.sender_id
                notification.type = "invite accepted"
                notification.description = "<a  href='/user/" + str(invitation.receiver_id.id) + "'>" +invitation.receiver_id.get_full_name()+"</a>" + " <i style='color:#525252;'>has accepted your invitation</i>"
                notification.save()
                invitation.delete()
                response_data['notificationid'] = notification.id
                print notification.id
            elif query == "ignore":
                response_data['message'] = "Invitation request from " + invitation.sender_id.get_full_name() + " has been ignored"
                invitation.delete()
            else:
                response_data['message'] = "bad data !"
        else:
            response_data['message'] = "bad data !"

        return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponseRedirect('/logged-in-view/')


@login_required()
def profile_page(request, id=None):
    try:
        user_profile = User.objects.get(id=id)
    except User.DoesNotExist:
        raise Http404
    user_profile_connected = []
    x = user_profile.ofWhome.all()
    for con in x:
        user_profile_connected.append(con.with_whom)

    args = {}
    args['user_profile'] = user_profile
    args['user_profile_connected'] = user_profile_connected
    return render_to_response('profile_page.html', args, RequestContext(request))


@login_required()
def notifications_viewed(request):
    notifications = Notifications.objects.filter(of_whom=request.user)
    for note in notifications:
        if not note.viewed_status:
            note.viewed_status = True
            note.save()

    return HttpResponse(json.dumps({"message": "True"}), content_type='application/json')


@login_required()
def messages_viewed(request):
    messages = Message.objects.filter(of_whom=request.user)
    for message in messages:
        if not message.viewed_status:
            message.viewed_status = True
            message.save()

    return HttpResponse(json.dumps({"message": "True"}), content_type='application/json')


@login_required()
def email_invite_connection(request):
    if request.method == "POST":
        list_of_users = request.POST.getlist('connectUser')
        for user_id in list_of_users:
            if Invitations.objects.filter(receiver_id=user_id, sender_id=request.user.id):
                settings.MESSAGE = ""
            elif Connection.objects.filter(Q(of_whom=request.user) & Q(with_whom=user_id)):
                settings.MESSAGE = ""
            else:
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return HttpResponse(json.dumps({'message':'no'}) , content_type="application/json")
                invite = Invitations()
                invite.receiver_id = user
                invite.sender_id = request.user
                invite.invitation_message = "I'd like to add you to my professional network on LinkedIN " + request.user.get_full_name()
                invite.relationship_type = "other"
                invite.save()
                settings.MESSAGE = ""
        return HttpResponse(json.dumps({'message':'yes'}) , content_type="application/json")


@login_required()
def find_alumini(request):
    if request.is_ajax() and 'countries_list' and 'counting'in request.POST:
        t = User.objects.get(id=request.user.id)
        keyword = t.student_set.values_list('School_University', flat=True)

        country_list = json.loads(request.POST['countries_list'])
        country_count = request.POST['counting']

        if request.POST['Type'] == 'Attended':
            q = User.objects.filter(Q(student__School_University__icontains=keyword[0])).filter(Q(student__DateAttended_from__range=(request.POST['start'], request.POST['end'])))
        else:
            q = User.objects.filter(Q(student__School_University__icontains=keyword[0])).filter(Q(student__DateAttended_to__range=(request.POST['start'], request.POST['end'])))

        q = q.filter(~Q(id = request.user.id))
        z2 = User.objects.none()
        if country_count > 0:
            for x in country_list:
                z1 = q.filter(country=x)
                z2 = z1 | z2

        return render_to_response('alumini_results_layout.html', {'results': z2}, RequestContext(request))

    elif request.is_ajax() and 'countries' in request.POST:
        t = User.objects.get(id=request.user.id)
        keyword = t.student_set.values_list('School_University', flat=True)
        q = User.objects.filter(Q(student__School_University__icontains=keyword[0]))

        q = q.values('country').annotate(count = Count('country')).order_by('-count')
        q = q.filter(~Q(id = request.user.id))
        return render_to_response('country_filters.html', {'q': q}, RequestContext(request))

    elif request.is_ajax() and 'results' in request.POST:
        t = User.objects.get(id=request.user.id)
        keyword = t.student_set.values_list('School_University', flat=True)
        q = User.objects.filter(Q(student__School_University__icontains=keyword[0]))
        q = q.filter(~Q(id = request.user.id))
        return render_to_response('alumini_results_layout.html', {'results': q}, RequestContext(request))

    else:
        t = User.objects.get(id=request.user.id)
        # keyword = t.student_set.values_list('School_University', flat=True)
        #
        return render_to_response('Alumini.html',{'school': t },RequestContext(request))


@login_required()
def logged_in_view(request):
    args = {}
    args['msg'] = settings.MESSAGE
    args['posts'] = Status.objects.all().order_by('-id')
    if request.is_ajax():
        return render_to_response('loggedinajax.html', args, RequestContext(request))
    connected = Connection.objects.filter(of_whom=request.user).values('with_whom')
    may_know = []
    for _user in connected:
        try:
            may_know += Connection.objects.filter(of_whom=_user['with_whom']).values_list('with_whom')
        except Exception, e:
            print e
    may_know = set(may_know)
    may_know_filtered = []
    for _user in may_know:
        try:
            may_know_filtered.append(User.objects.get(id=_user[0]))
        except Exception, e:
            print e
    args['may_know'] = may_know_filtered

    settings.MESSAGE = ""
    return render_to_response('loggedInPage.html', args, RequestContext(request))


@login_required()
def post_attachments(request):
    if request.method == "POST":
        att_form = ProfilePic(request.POST, request.FILES)
        if att_form.is_valid():
            handle_uploaded_file(request.FILES['pic'])
            name = request.FILES['pic'].name
            name = str(name)
            request.session['attached'] ="/uploads/" + name

            send = "/media/uploads/" + name

            return HttpResponse('<p>' + send + '</p>')
    else:
        return HttpResponse("<p>null</P>")


@login_required()
def post_status(request):
    if request.is_ajax():
        new_status = Status()
        new_status.of_whom = request.user
        new_status.share_type = request.POST['status-type']
        new_status.simple_text = request.POST['main_status']
        new_status.link_subject = request.POST['link-subject']
        new_status.link_description = request.POST['para']
        if 'attachment' in request.POST \
                and request.POST['attachment'] == "true"\
                and 'attached' in request.session:
            new_status.attached_image = request.session['attached']
            del request.session['attached']
            request.session.modified = True
        elif 'link' in request.POST and request.POST['link'] == "true" and 'link' in request.session:
            new_status.link = request.session['link']
            new_status.attached_image = request.session['imagelink']
            del request.session['link']
            del request.session['imagelink']
            request.session.modified = True
        new_status.save()
        post = new_status
    return render_to_response('single_post.html', {'post': post}, RequestContext(request))


@login_required()
def post_comment(request):
    if 'which-post' and 'comment-text' in request.POST:
        if request.POST['comment-text'] == "":
            return
        new_comment = Comment()
        new_comment.of_whom = request.user
        x = Status.objects.filter(id=request.POST['which-post'])[0]
        new_comment.comment_of = x
        new_comment.comment_text = request.POST['comment-text']
        new_comment.save()
        if x.of_whom != request.user:
            new_notification = Notifications()
            new_notification.of_whom = x.of_whom
            new_notification.type = "comment"
            new_notification.description = '<a style="color:#525252;"  href="/logged-in-view/#cc' + request.POST['which-post'] + 'cc' +\
                                            '"><b>' + request.user.get_full_name() + '</b> <i>has commented on your post</i></a>'
            new_notification.save()
        return render_to_response('ComentContainer.html', {'comment': new_comment}, RequestContext(request))
    else:
        return HttpResponse("<p>null</p>")


@login_required()
def like_it(request):
    if request.is_ajax() and 'which_post' in request.POST:
        x = ""
        try:
            x = Status.objects.get(id=request.POST['which_post'])
            like = Like.objects.get(on_which_status=x, of_which_user=request.user)
            like.delete()
            return render_to_response("single_post.html", {'post':Status.objects.get(id=request.POST['which_post'])}, RequestContext(request))
        except Like.DoesNotExist:
            new_like = Like()
            new_like.of_which_user = request.user
            new_like.on_which_status = x
            new_like.save()
            if x.of_whom != request.user:
                new_notification = Notifications()
                new_notification.of_whom = x.of_whom
                new_notification.type = "liked"
                new_notification.description = '<a style="color:#525252;" href="/logged-in-view/#cc' + request.POST['which_post'] + 'cc' +\
                                            '"><b>' + request.user.get_full_name() + '</b><i> has liked your post</i></a>'
                new_notification.save()
            return render_to_response("single_post.html", {'post':Status.objects.get(id=request.POST['which_post'])}, RequestContext(request))


@login_required()
def get_content(request):
    if request.is_ajax():
        if 'to_open' in request.POST:
            args = {}
            to_open = request.POST['to_open']
            try:
                if "http://" not in to_open:
                    to_open = "http://" + request.POST['to_open']
                x = requests.get(to_open)
            except Exception, e:
                args['error'] = "Url Not Found";
                return HttpResponse(json.dumps(args), content_type="application/json")
            if x.status_code != 200:
                args['error'] = "Url Not Found";
                return HttpResponse(json.dumps(args), content_type="application/json")
            soup = BeautifulSoup(x.text)
            args['title'] = soup.title.string
            p = soup.find_all('p')

            h = soup.find_all('h1')
            m = soup.find(attrs={"name":"description"})
            newM = soup.find(attrs={"name":"og:description"})
            if m:
                args['para'] = m['content']
            elif newM:
                args['para'] = newM['content']
            elif len(p) != 0:
                args['para'] = p[0].string
            elif len(h) != 0:
                args['para'] = h[0].string
            else:
                args['para'] = ""
            ico = soup.find(attrs={"property":"og:image"})
            ico2 = soup.find(attrs={"name":"og:image"})
            if ico:
                image_source = ico['content']
            elif ico2:
                image_source = ico2['content']
            else:
                i = soup.find_all('img')
                if len(i) != 0:
                    image_source = i[(len(i)-1)/2]['src']
                if "http://" not in image_source and "https://" not in image_source:
                    if "//" in image_source:
                        image_source = "http:" + image_source
                    else:
                        image_source = str(request.POST['to_open'] + '/' + image_source)
            filename = ntpath.basename(image_source)
            filename = filename.split('?')[0]
        try:
            image = requests.get(image_source)
            if image.status_code == 200:
                with open(normpath(join(settings.SITE_ROOT, 'LinkedApp/media/uploads/' + filename)), 'wb') as f:
                    for chunk in image.iter_content():
                        f.write(chunk)
            else:
                args['images'] = "/media/uploads/image-not-found.gif"
            request.session['imagelink'] = "/uploads/" + filename
            request.session['link'] = request.POST['to_open']
        except Exception, e:
            print e
        args['images'] = "/media/uploads/" + filename
        return HttpResponse(json.dumps(args), content_type="application/json")


#################################### Message work ##############################################

@login_required()
def message_inbox(request):
    return render_to_response('Message_view.html', RequestContext(request))


@login_required()
def invitation_list(request):
    return render_to_response('Invitation_view.html', RequestContext(request))


@login_required()
def send_message(request):
    if request.method=="POST" and 'Subject' in request.POST:
        sub = request.POST['Subject'] ;
        body = request.POST['Message_body'];

        ids = request.POST.getlist("ids[]")

        for x in ids:
            New = Message()
            New.body = body
            New.subject = sub
            New.of_whom = request.user
            try:
                q = User.objects.get(id=x)
            except User.DoesNotExist:
                return
            New.to = q
            New.viewed_status = "false"
            New.save()
        return render_to_response('Message_view.html', RequestContext(request))

    else:
        return render_to_response('Compose_Message.html', RequestContext(request))


@login_required()
def message_result_ajax(request):

    if request.GET['search_query']:
        args = {}
        result = []
        keyword = request.GET['search_query']
        list_of_keywords = keyword.split()
        first_keyword = ""
        if list_of_keywords:
            first_keyword = list_of_keywords[0].lower()
        result = User.objects.filter(Q(first_name__iexact=first_keyword)
                                     | Q(email=first_keyword)
                                     | Q(country__icontains=first_keyword)
                                     | Q(last_name__iexact=first_keyword)
                                     | Q(student__School_University__icontains=first_keyword)
                                     | Q(jobseeker__most_recent_job_title__icontains=first_keyword)
                                     | Q(jobseeker__MostRecentCompany__icontains=first_keyword)
                                     | Q(employed__Job_title__icontains=first_keyword)
                                     | Q(employed__Company__icontains=first_keyword)).distinct()

        for keyword in list_of_keywords:
            result = result.filter(Q(first_name__iexact=keyword)
                                   | Q(email=keyword)
                                   | Q(country__icontains=keyword)
                                   | Q(last_name__iexact=keyword)
                                   | Q(student__School_University__icontains=keyword)
                                   | Q(jobseeker__most_recent_job_title__icontains=keyword)
                                   | Q(jobseeker__MostRecentCompany__icontains=keyword)
                                   | Q(employed__Job_title__icontains=keyword)
                                   | Q(employed__Company__icontains=keyword))

        args['results'] = result
        return render_to_response('msg_ajax_results.html', args, RequestContext(request))


@login_required()
def sent_box_messages(request):
    return render_to_response('sent_box.html',RequestContext(request))


@login_required()
def send_emails(request):
    if request.method == "POST":
        list_of_users = request.POST.getlist('InviteUsers')
        print list_of_users

        for x in list_of_users:
            subject, from_email, to = 'Confirmation Email', 'LinkedIN', x
            text_content = 'This is an important message on behalf of LinkedIN . Please Click on the button below to join LinkedIN'
            html_content = ' <p style="font-size: 20px"><strong>The worlds largest professional network: 225 million strong.</strong></p><p style="font-size: 20px;"> <strong>Discover professional opportunities, business deals, and new ventures.</strong></p><span style="font-size: 25px; margin-right: 5px;"><strong>Its Free</strong></span><a href="mylinkedin.herokuapp.com/join-in"><button style="background-color: #2670ac ; border:none; margin-top:35px;  height: 40px; width: 130px; border-radius: 9px; cursor: pointer "><strong style="color:#ffffff">JOIN LINKEDIN</strong></button></a>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return render_to_response('final_step.html',RequestContext(request))
    return render_to_response('button_test.html')


def forgot_password(request):
    if request.method == "POST":
        email_id = request.POST['address']
        try:
            object = User.objects.get(email=email_id)
            random_number = randint(1000000, 99999999)
            Forgot = Forgot_Pass()
            Forgot.key = random_number
            Forgot.user_id = object
            Forgot.save()

            subject, from_email, to = 'Forgot Password', 'LinkedIN', object.email
            text_content = 'This is an important message on behalf of LinkedIN . Please Click on the button below to join LinkedIN'
            html_content = '<a href="mylinkedin.herokuapp.com/set_pass/'+str(random_number)+'"><button style="background-color: #2670ac ; border:none; margin-top:35px;  height: 40px; width: 130px; border-radius: 9px; cursor: pointer "><strong style="color:#ffffff">JOIN LINKEDIN</strong></button></a>'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponseRedirect('/sign-in/')

        except User.DoesNotExist:
            object = None
            error= "No     such     Email Address      Exists"
            return render_to_response('Forgot_Password.html', {'myErrors':error}, RequestContext(request))

    error = ""
    return render_to_response('Forgot_Password.html', {'myErrors':error}, RequestContext(request))


def pass_link(request, rand=None):

    if rand:
        try:
            q = Forgot_Pass.objects.get(key=rand)
            return render_to_response('Reset_Password.html', {'random': rand}, RequestContext(request))
        except Forgot_Pass.DoesNotExist:
            q = None
            error=" Page Expired"
            return render_to_response('screen5(sign in).html',{'myErrors':error}, RequestContext(request))


def set_new_pass(request):
    if request.method == "POST" and 'random_no' and 'password_confirm' and 'password_new' in request.POST:
        new_pas = request.POST['password_new']
        password_confirm = request.POST['password_confirm']
        rand_value = request.POST['random_no']

        if new_pas != password_confirm:
            return render_to_response('Reset_Password.html', {'myErrors': "Passwords Donot Match"},  RequestContext(request))
        usr = Forgot_Pass.objects.get(key=rand_value)
        usr.user_id.set_password(new_pas)
        usr.user_id.save()
        Forgot_Pass.objects.filter(key=rand_value).delete()

        return HttpResponseRedirect('/sign-in/')
    return render_to_response('Reset_Password.html', RequestContext(request))