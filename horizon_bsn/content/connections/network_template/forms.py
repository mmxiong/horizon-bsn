# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.core.urlresolvers import reverse
from django.forms import ValidationError  # noqa
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms
from horizon_bsn.api import neutron

from openstack_dashboard.api import heat


def findDefault(template_list, key):
    """Finds if a key exist within a dictionary.

    Returns empty string if not found.
    return: String
    """
    result = ''

    if key in template_list:
        result = template_list[key]

    return result


class SelectTemplateForm(forms.SelfHandlingForm):
    network_templates = forms.ChoiceField(
        label=_('Default Network Templates'),
        required=True,
    )

    def __init__(self, request, *args, **kwargs):
        super(SelectTemplateForm, self).__init__(request, *args, **kwargs)
        templates = neutron.networktemplate_list(request, **{})
        field_templates = []
        if templates:
            field_templates.append(
                ('default', _('--- Select Network Template ---')))
            for template in templates:
                field_templates.append(
                    (template.id, template.name))
        else:
            field_templates.append(
                ('default', _('--- No Available Templates  ---')))
        self.fields['network_templates'].choices = field_templates

    def clean(self):
        cleaned_data = super(SelectTemplateForm, self).clean()

        def update_cleaned_data(key, value):
            cleaned_data[key] = value
            self.errors.pop(key, None)

        network_template_id = cleaned_data.get('network_templates')

        if network_template_id == 'default':
            msg = _('A template must be selected.')
            raise ValidationError(msg)
        record = neutron.networktemplate_get(self.request, network_template_id)
        if not record:
            msg = _('A template must be selected.')
            raise ValidationError(msg)
        return cleaned_data

    def handle(self, request, data):
        # nothing is done until the apply step because the required fields
        # need to be extracted.
        return data


class RemoveTemplateForm(forms.SelfHandlingForm):

    def handle(self, request, data):
        try:
            assign = neutron.networktemplateassignment_get(
                request, request.user.tenant_id)
            hc = heat.heatclient(request)
            # we only want the one that matches the network template
            stacks = \
                [s for s in hc.stacks.list(tenant_id=request.user.tenant_id)
                 if s.id == assign.stack_id]
            if stacks:
                hc.stacks.delete(assign.stack_id)
            # delete the network template assignment too
            neutron.networktemplateassignment_delete(request, assign.id)
            return True
        except Exception:
            return False


def extract_fields_from_body(request, body):
    hc = heat.heatclient(request)
    res = hc.stacks.validate(template=body)
    return res


class ApplyTemplateForm(forms.SelfHandlingForm):
    failure_url = 'horizon:project:connections:index'

    def __init__(self, *args, **kwargs):
        super(ApplyTemplateForm, self).__init__(*args, **kwargs)
        try:
            template_id = self.request.path_info.split('/')[-1]
            try:
                template_db = neutron.networktemplate_get(self.request,
                                                          template_id)
            except Exception:
                raise Exception(_("Could not find a template with that ID."))
            try:
                assign = neutron.networktemplateassignment_get(
                    self.request, self.request.user.tenant_id)
                if assign:
                    raise Exception(_("This tenant has already deployed "
                                      "a network template."))
            except Exception:
                pass
            template = extract_fields_from_body(self.request, template_db.body)
            # Sorts the parameters in the template.
            parameters = template['Parameters'].keys()
            parameters.sort()
            parameters.reverse()
            # Populates the form dynamically with information from the template
            for parameter in parameters:
                self.fields[parameter] = forms.CharField(
                    max_length="255",
                    label=template['Parameters'][parameter]['Label'],
                    initial=findDefault(template['Parameters'][parameter],
                                        'Default'),
                    help_text=template['Parameters'][parameter]['Description'],
                    required=True
                )
        except Exception as e:
            msg = _("Failed preparing template. You may not have "
                    "permissions to use Heat templates. %s") % e
            exceptions.handle(self.request, msg,
                              redirect=reverse(self.failure_url))

    def handle(self, request, data):
        try:
            template_id = request.path_info.split('/')[-1]
            try:
                template_db = neutron.networktemplate_get(request, template_id)
            except Exception:
                raise Exception(_("Could not find a template with that ID."))
            # validate the body
            extract_fields_from_body(request, template_db.body)
            templateassignment_dict = {
                'tenant_id': request.user.tenant_id,
                'template_id': template_db.id,
                'stack_id': 'PENDING'}
            neutron.networktemplateassignment_create(
                request, **templateassignment_dict)
            args = {
                'stack_name': "auto-%s" % template_db.name,
                'parameters': data,
                'template': template_db.body
            }
            hc = heat.heatclient(request)
            try:
                req = hc.stacks.create(**args)
            except Exception as e:
                raise e
            neutron.networktemplateassignment_update(
                request, request.user.tenant_id,
                **{'stack_id': req['stack']['id']})
        except Exception as e:
            msg = _("Error loading template: %s") % e
            exceptions.handle(self.request, msg, redirect=self.failure_url)
        return True
