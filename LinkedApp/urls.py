from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'LinkedApp.views.main' , name='home'),
    url(r'^what-is-linkedIN/$', 'LinkedApp.views.whatisLinkedIn'),
    url(r'^cookie-policy/$', 'LinkedApp.views.cookie_policy'),
    url(r'^user-agreement/$', 'LinkedApp.views.user_agreement'),
    url(r'^privacy-policy/$', 'LinkedApp.views.privacy_policy'),
    url(r'^join-in/$', 'LinkedApp.views.join_in'),
    url(r'^sign-in/$', 'LinkedApp.views.sign_in'),
    url(r'^password-reset/$', 'LinkedApp.views.forgot_password'),
    url(r'^search-by-country/$', 'LinkedApp.views.search_by_country'),
    url(r'^default-for-links/$', 'LinkedApp.views.default_for_links', name='default'),
    url(r'^reg-step-2/$', 'LinkedApp.views.reg_step_2'),
    url(r'^log-out/$', 'LinkedApp.views.user_logout'),
    url(r'^email_api/$', 'LinkedApp.views.email_api' ),
    url(r'^email_sent/$', 'LinkedApp.views.email_sent' ),
    url(r'^invite_friends/$', 'LinkedApp.views.invite_friends' ),
    url(r'^final-step/$', 'LinkedApp.views.final_step'),
    url(r'^upload-image/$', 'LinkedApp.views.upload_image'),
    url(r'^get-profile-pic/$', 'LinkedApp.views.get_prof_pic'),
    url(r'^logged-in-view/$', 'LinkedApp.views.logged_in_view'),
    url(r'^search-result/$', 'LinkedApp.views.search_result'),
    url(r'^connection/(?P<con>\d+)/$', 'LinkedApp.views.connect_invitation_form'),
    url(r'^send-invite/$', 'LinkedApp.views.send_invitation'),
    url(r'^accept-or-ignore/$', 'LinkedApp.views.accept_or_ignore'),
    url(r'^user/(?P<id>\d+)/$', 'LinkedApp.views.profile_page'),
    url(r'^notifications-viewed/$', 'LinkedApp.views.notifications_viewed'),
    url(r'^messages-viewed/$', 'LinkedApp.views.messages_viewed'),
    url(r'^search-result-ajax/$', 'LinkedApp.views.search_result_ajax'),
    url(r'^email-invite-connection/', 'LinkedApp.views.email_invite_connection'),
    url(r'^alumini/', 'LinkedApp.views.find_alumini'),
    url(r'^post-attachment/', 'LinkedApp.views.post_attachments'),
    url(r'^post-status/', 'LinkedApp.views.post_status'),
    url(r'^post-comment/', 'LinkedApp.views.post_comment'),
    url(r'^like-it/', 'LinkedApp.views.like_it'),
    url(r'^get-content/', 'LinkedApp.views.get_content'),
    url(r'^messages/$', 'LinkedApp.views.message_inbox'),
    url(r'^invitations/$', 'LinkedApp.views.invitation_list'),
    url(r'^compose_message/$', 'LinkedApp.views.send_message'),
    url(r'^message_result/$', 'LinkedApp.views.message_result_ajax'),
    url(r'^send_message/$', 'LinkedApp.views.send_message'),
    url(r'^sent/$', 'LinkedApp.views.sent_box_messages'),
    url(r'^sending_emails/$', 'LinkedApp.views.send_emails'),
    url(r'^set_pass/(?P<rand>\d+)/$', 'LinkedApp.views.pass_link'),
    url(r'^resetting/$', 'LinkedApp.views.set_new_pass'),

    # url(r'^email_sent/$', 'LinkedApp.views.email_sent'),
    # url(r'^$', 'LinkedIN.views.home', name='home'),
    # url(r'^LinkedIN/', include('LinkedIN.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)