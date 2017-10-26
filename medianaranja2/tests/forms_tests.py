# coding=utf-8
from .adapter_tests import MediaNaranjaAdaptersBase
from elections.models import Area
from medianaranja2.forms import SetupForm, QuestionsForm, ProposalsForm, MediaNaranjaWizardForm
from django.conf import settings
from elections.models import Candidate, Election, Area
from constance import config
from django import forms
from popular_proposal.models import (PopularProposal,
                                     Commitment,
                                     )
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from constance.test import override_config

class FormsTestCase(MediaNaranjaAdaptersBase):
    def setUp(self):
        super(FormsTestCase, self).setUp()
        self.setUpProposals()
        self.setUpQuestions()
        self.area = Area.objects.create(name="children",
                                        classification=settings.FILTERABLE_AREAS_TYPE[0])
        self.election.area = self.area
        self.election.save()

    def test_instanciate_category_selection_form(self):
        data = {
            'area': self.area.id,
            'categories': [self.category1.id, self.category2.id]
        }
        form = SetupForm(data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['area'], self.area)
        self.assertIn(self.category1, form.cleaned_data['categories'])
        self.assertIn(self.category2, form.cleaned_data['categories'])

    @override_config(DEFAULT_AREA='argentina')
    def test_if_no_area_given_then_selects_the_default_area(self):
        argentina = Area.objects.create(name=u'Argentina', id='argentina')
        data = {
            'categories': [self.category1.id, self.category2.id]
        }
        form = SetupForm(data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['area'], argentina)

    def test_questions_form_instanciate(self):
        kwargs = {'categories': [self.category1, self.category2]}
        form = QuestionsForm(**kwargs)
        self.assertEquals(len(form.fields), 2)
        self.assertIn(self.topic1.slug, form.fields)
        self.assertIsInstance(form.fields[self.topic1.slug], forms.ModelChoiceField)
        topic_1_choices = list(form.fields[self.topic1.slug].choices)
        self.assertIn((self.position1.id, self.position1.label), topic_1_choices)
        self.assertIn((self.position2.id, self.position2.label), topic_1_choices)
        self.assertIn(self.topic2.slug, form.fields)
        self.assertIsInstance(form.fields[self.topic2.slug], forms.ModelChoiceField)
        topic_2_choices = list(form.fields[self.topic2.slug].choices)
        self.assertIn((self.position3.id, self.position3.label), topic_2_choices)
        self.assertIn((self.position4.id, self.position4.label), topic_2_choices)

    def test_get_cleaned_data_from_questions_form(self):
        data = {self.topic1.slug: self.position1.id,
                self.topic2.slug: self.position3.id}
        kwargs = {'categories': [self.category1, self.category2], 'data': data}
        form = QuestionsForm(**kwargs)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        self.assertIn(self.position1, form.cleaned_data['positions'])
        self.assertIn(self.position3, form.cleaned_data['positions'])

    def test_proposals_form_instanciate(self):
        kwargs = {'proposals': [self.p1, self.p2, self.p3]}
        form = ProposalsForm(**kwargs)
        proposals_choices = list(form.fields['proposals'].choices)
        self.assertIn((self.p1.id, unicode(self.p1)), proposals_choices)
        self.assertIn((self.p2.id, unicode(self.p2)), proposals_choices)
        self.assertIn((self.p3.id, unicode(self.p3)), proposals_choices)

    def test_posting_proposals_form(self):
        data = {'proposals': [self.p1.id, self.p2.id]}
        kwargs = {'proposals': [self.p1, self.p2, self.p3], 'data':data}
        form = ProposalsForm(**kwargs)
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        self.assertIn(self.p1, form.cleaned_data['proposals'])
        self.assertIn(self.p1, form.cleaned_data['proposals'])


class MediaNaranjaWizardFormTests(MediaNaranjaAdaptersBase):
    def setUp(self):
        super(MediaNaranjaWizardFormTests, self).setUp()
        self.setUpProposals()
        self.setUpQuestions()
        proposer = User.objects.create_user(username="proposer2")
        self.p5 = PopularProposal.objects.create(proposer=proposer,
                                                 title=u'p5',
                                                 data={}
                                                 )
        self.p6 = PopularProposal.objects.create(proposer=proposer,
                                                 title=u'p6',
                                                 data={}
                                                 )
        self.p7 = PopularProposal.objects.create(proposer=proposer,
                                                 title=u'p7',
                                                 data={}
                                                 )
        self.child = Area.objects.create(name="children",
                                        classification=settings.FILTERABLE_AREAS_TYPE[0])
        mother = Area.objects.create(name="mother")
        # Circunscripcion
        self.election2 = Election.objects.create(name='election2')
        self.election2.area = mother
        self.election2.save()
        self.candidate_2_1 = Candidate.objects.create(name="candidate_2_1")
        self.candidate_2_2 = Candidate.objects.create(name="candidate_2_2")
        self.election2.candidates.add(self.candidate_2_1)
        self.election2.candidates.add(self.candidate_2_2)
        Commitment.objects.create(commited=True, candidate=self.candidate_2_2, proposal=self.p5)
        mother.children.add(self.child)
        # Distrito
        grand_mother = Area.objects.create(name="grand_mother")
        self.election3 = Election.objects.create(name='election3')

        self.election3.area = self.child
        self.election3.save()
        self.candidate_3_1 = Candidate.objects.create(name="candidate_3_1")
        self.candidate_3_2 = Candidate.objects.create(name="candidate_3_2")
        self.election3.candidates.add(self.candidate_3_1)
        self.election3.candidates.add(self.candidate_3_2)
        Commitment.objects.create(commited=True, candidate=self.candidate_3_2, proposal=self.p6)

        grand_mother.children.add(mother)

        self.assertIn(grand_mother, self.child.parents)
        self.assertIn(mother, self.child.parents)
        # Pais
        self.election.area = grand_mother
        self.election.save()
        self.data_to_be_posted = [
            {'0-area': self.child.id,
             '0-categories': [self.category1.id, self.category2.id]
            },
            {'1-' + self.topic1.slug: self.position1.id,
             '1-' + self.topic2.slug: self.position4.id
            },
            {'2-proposals': [self.p1.id, self.p3.id, self.p6.id]}
        ]
        self.expected_forms_classes = [
            SetupForm,
            QuestionsForm,
            ProposalsForm
        ]
        self.url = reverse('medianaranja2:index')

    def complete_wizard(self):
        response = self.client.get(self.url)
        steps = response.context['wizard']['steps']

        for i in range(steps.count):
            self.assertEquals(steps.current, unicode(i))
            data = {'media_naranja_wizard_form-current_step': unicode(i)}
            data.update(self.data_to_be_posted[i])
            self.assertIsInstance(response.context['form'], self.expected_forms_classes[i])
            response = self.client.post(self.url, data=data)
            if 'form' in response.context:
                steps = response.context['wizard']['steps']
                self.assertFalse(response.context['form'].errors)
        is_done = False
        for template in response.templates:
            if template.name.endswith('medianaranja2/resultado.html'):
                is_done = True
        self.assertTrue(is_done)
        return response

    def test_wizard_til_the_end(self):
        self.assertTrue(self.complete_wizard())

    def test_get_done(self):
        response = self.complete_wizard()
        self.assertEquals(len(response.context['results']), 3)
        result_0 = response.context['results'][0]
        expected_0 = [{'candidate':self.candidate_3_2, 'value': 1},
                    {'candidate':self.candidate_3_1, 'value': 0}]
        self.assertEquals(result_0, expected_0)
        expected_1 = [{'candidate':self.candidate_2_1, 'value': 0},
                    {'candidate':self.candidate_2_2, 'value': 0}]
        result_1 = response.context['results'][1]
        self.assertEquals(result_1, expected_1)
        expected = [{'candidate':self.c1, 'value': 1.5},
                    {'candidate':self.c2, 'value': 1},
                    {'candidate':self.c3, 'value': 0}]
        result_2 = response.context['results'][2]
        self.assertEquals(result_2, expected)