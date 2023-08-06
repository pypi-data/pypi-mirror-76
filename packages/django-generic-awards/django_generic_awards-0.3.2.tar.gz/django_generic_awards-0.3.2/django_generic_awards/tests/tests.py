from contextlib import contextmanager

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth import authenticate

from django_generic_awards.actions import AddAward
from django_generic_awards.models import Award, AwardScoreOption, AwardableModel, ObjectAwardScore
from django_generic_awards.admin import ObjectAwardScoreInline


class AwardingTestCase(TestCase):

    def test_awards_creation(self):
        guiness_award = Award.objects.create(name='Guinness world records')
        fallstaf_award = Award.objects.create(name='Fallstaf', help_text='Fallstaf {}/10 points')
        self.assertEqual(Award.objects.count(), 2)

        guiness_award_values = ('longest test case', 'very best python award module')
        for value in guiness_award_values:
            AwardScoreOption.objects.create(award=guiness_award, value=value)
        self.assertEqual(guiness_award.awardscoreoption_set.count(), len(guiness_award_values))
        self.assertEqual(guiness_award.awardscoreoption_set.first().value, guiness_award_values[0])

        fallstaf_award_values = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        for value in fallstaf_award_values:
            AwardScoreOption.objects.create(award=fallstaf_award, value=value)
        self.assertEqual(fallstaf_award.awardscoreoption_set.count(), len(fallstaf_award_values))
        fallstaf_award_option = fallstaf_award.awardscoreoption_set.last()
        self.assertIn('10/10 points', str(fallstaf_award_option))

    def test_awardable_object(self):
        guiness_award = Award.objects.create(name='Guinness world records')
        fallstaf_award = Award.objects.create(name='Fallstaf', help_text='Fallstaf {}/10 points')
        guiness_award_option = AwardScoreOption.objects.create(award=guiness_award, value='longest test case')

        with self.assertRaises(ValidationError):
            ObjectAwardScore.objects.create(
                generic_object=guiness_award,
                award_score_option=guiness_award_option,
            )

        # make Award awardable model - this is a valid case
        awardable = AwardableModel.objects.create(content_type=ContentType.objects.get_for_model(guiness_award))
        awardable.award_for_concrete_model.set([guiness_award, fallstaf_award])

        ObjectAwardScore.objects.create(
            generic_object=guiness_award,
            award_score_option=guiness_award_option,
        )


class LoginMixin(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_superuser(self.username, 'test@example.com', self.password)

    @contextmanager
    def login(self):
        self.client.login(username=self.username, password=self.password)
        yield
        self.client.logout()


class AddAwardActionTestCase(LoginMixin, TestCase):

    def setUp(self):
        super().setUp()

        guiness_award = Award.objects.create(name='Guinness world records')
        Award.objects.create(name='Fallstaf', help_text='Fallstaf {}/10 points')
        AwardScoreOption.objects.create(award=guiness_award, value='longest test case')

    def make_awardable(self, model):
        awardable = AwardableModel.objects.create(content_type=ContentType.objects.get_for_model(model))
        awardable.award_for_concrete_model.set(Award.objects.all())

    def test_action_showing_up_in_action_list(self):
        url_name = 'admin:django_generic_awards_award_changelist'
        change_awards_url = reverse(url_name)

        with self.login():
            response = self.client.get(change_awards_url)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(AddAward.name, response.rendered_content)
            self.assertNotIn(str(AddAward.short_description), response.rendered_content)

            self.make_awardable(Award)

            response = self.client.get(change_awards_url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(AddAward.name, response.rendered_content)
            self.assertIn(str(AddAward.short_description), response.rendered_content)

    def test_check_action_template(self):
        url_name = 'admin:django_generic_awards_award_changelist'
        change_awards_url = reverse(url_name)
        self.make_awardable(Award)

        with self.login():
            response = self.client.get(change_awards_url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(AddAward.name, response.rendered_content)
            self.assertIn(str(AddAward.short_description), response.rendered_content)

        data = {
            'action': AddAward.name,
            '_selected_action': list(Award.objects.values_list('pk', flat=True))
        }

        with self.login():
            response = self.client.post(change_awards_url, data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(AddAward.name, response.rendered_content)
            self.assertIn(str(AddAward.short_description), response.rendered_content)

            self.assertIn(AddAward.template_name, response.template_name)


class GenericAwardsAdminMixinTestCase(LoginMixin, TestCase):
    def setUp(self):
        super().setUp()

        guiness_award = Award.objects.create(name='Guinness world records')
        AwardScoreOption.objects.create(award=guiness_award, value='longest test case')

        self.factory = RequestFactory()

    def make_awardable(self, model):
        awardable = AwardableModel.objects.create(content_type=ContentType.objects.get_for_model(model))
        awardable.award_for_concrete_model.set(Award.objects.all())

    def test_change_object_awardable_adds_mixins_to_model(self):
        url_name = 'admin:django_generic_awards_award_changelist'
        change_awards_url = reverse(url_name)

        request = self.factory.get(change_awards_url)
        session_middleware = SessionMiddleware()
        session_middleware.process_request(request)
        auth_middleware = AuthenticationMiddleware()
        auth_middleware.process_request(request)
        request.user = authenticate(request, username=self.username, password=self.password)

        award_admin_model_object = admin.site._registry[Award]

        previous_actions = award_admin_model_object.get_actions(request)
        previous_inlines = award_admin_model_object.get_inlines(request)

        self.make_awardable(Award)

        current_actions = award_admin_model_object.get_actions(request)
        current_inlines = award_admin_model_object.get_inlines(request)

        self.assertNotEqual(len(previous_actions), len(current_actions))
        self.assertNotEqual(len(previous_inlines), len(current_inlines))

        self.assertNotIn(ObjectAwardScoreInline, previous_inlines)
        self.assertIn(ObjectAwardScoreInline, current_inlines)

        self.assertNotIn(AddAward.name, previous_actions)
        self.assertIn(AddAward.name, current_actions)
