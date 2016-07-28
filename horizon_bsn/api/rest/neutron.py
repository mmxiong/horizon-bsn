#
#    (c) Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""API over the neutron service.
"""

from django.views import generic

from openstack_dashboard.api.rest import urls
from openstack_dashboard.api.rest import utils as rest_utils

from horizon_bsn.api import neutron as bsnneutron
from openstack_dashboard.api import neutron

from horizon_bsn.content.connections.tabs import get_stack_topology
from django.utils.safestring import mark_safe

from horizon_bsn.content.connections.routerrules.rulemanager import routerrule_list, add_rule

@urls.register
class ReachabilityTest(generic.View):
    """API for BSN Neutron Reachability Tests"""
    url_regex = r'neutron/reachabilitytests/(?P<reachabilitytest_id>[^/]+|default)/$'

    # @rest_utils.ajax()
    # def get(self, request, networktemplate_id):
    #     result = bsnneutron.networktemplate_get(request, networktemplate_id)
    #     return result

    @rest_utils.ajax()
    def patch(self, request, reachabilitytest_id):
        result = bsnneutron.reachabilitytest_update(request, reachabilitytest_id, run_test=True)
        return result

    @rest_utils.ajax()
    def delete(self, request, reachabilitytest_id):
        result = bsnneutron.reachabilitytest_delete(request, reachabilitytest_id)
        return result

@urls.register
class ReachabilityTests(generic.View):
    """API for BSN Neutron Reachability Tests"""
    url_regex = r'neutron/reachabilitytests/$'

    @rest_utils.ajax()
    def get(self, request):
        result = bsnneutron.reachabilitytest_list(request)
        return {'items': [n.to_dict() for n in result]}

    @rest_utils.ajax()
    def post(self, request):
        result = bsnneutron.reachabilitytest_create(request, **request.DATA)
        return result

@urls.register
class NetworkTemplate(generic.View):
    """API for BSN Neutron Network Template"""
    url_regex = r'neutron/networktemplate/(?P<networktemplate_id>[^/]+|default)/$'

    @rest_utils.ajax()
    def get(self, request, networktemplate_id):
        result = bsnneutron.networktemplate_get(request, networktemplate_id)
        return result

    @rest_utils.ajax()
    def patch(self, request, networktemplate_id):
        result = bsnneutron.networktemplate_update(request, networktemplate_id, **request.DATA)
        return result

    @rest_utils.ajax()
    def delete(self, request, networktemplate_id):
        result = bsnneutron.networktemplate_delete(request, networktemplate_id)
        return result

@urls.register
class NetworkTemplates(generic.View):
    """API for BSN Neutron Network Template"""
    url_regex = r'neutron/networktemplate/$'

    @rest_utils.ajax()
    def post(self, request):
        result = bsnneutron.networktemplate_create(request, **request.DATA)
        return result

    @rest_utils.ajax()
    def get(self, request):
        result = bsnneutron.networktemplate_list(request)
        return {'items': [n.to_dict() for n in result]}

@urls.register
class NetworkTemplateAssignment(generic.View):
    """API for BSN Neutron Network Template Assignment"""
    url_regex = r'neutron/networktemplateassignment/(?P<networktemplate_id>[^/]+|default)/$'

    @rest_utils.ajax()
    def delete(self, request, networktemplate_id):
        result = bsnneutron.networktemplateassignment_delete(request, networktemplate_id)
        return result

@urls.register
class NetworkTemplateAssignments(generic.View):
    """API for BSN Neutron Network Template Assignment"""
    url_regex = r'neutron/networktemplateassignment/$'

    @rest_utils.ajax()
    def get(self, request):
        try:
            topology = get_stack_topology(request)
            if not topology.get('assign'):
                return []
            tabledata = {
                'id': topology['template'].id,
                'name': topology['template'].name,
                'stack_id': topology['stack'].id,
                'heat_stack_name': topology['stack'].stack_name,
                'description': topology['stack'].description,
                'status': topology['stack'].status,
                'stack_status': topology['stack'].stack_status,
                'stack_status_reason': topology['stack'].stack_status_reason,
                'resources': mark_safe('<br>'.join([
                    ('%s (%s)' % (r.resource_name,
                                  r.resource_type)).replace(' ', '&nbsp;')
                    for r in topology['stack_resources']]))
            }
            return {'items': [tabledata]}
        except Exception:
            return []

@urls.register
class Router(generic.View):
    """API for Router_get"""
    url_regex = r'neutron/router/$'

    @rest_utils.ajax()
    def get(self, request):
        result = neutron.router_list(request)[0]
        return result

@urls.register
class RouterRule(generic.View):
    """API for BSN Neutron Network Template Assignment"""
    url_regex = r'neutron/routerrules/(?P<routerrule_id>[^/]+|default)/$'

@urls.register
class RouterRules(generic.View):
    """API for BSN Neutron Network Template"""
    url_regex = r'neutron/routerrules/$'

    @rest_utils.ajax()
    def post(self, request):
        # router rule creation
        router_id = neutron.router_list(request)[0].id
        result = add_rule(request, router_id, request.DATA);
        return result

    @rest_utils.ajax()
    def get(self, request):
        # get router_id from tenant id and a call to neutron
        router = neutron.router_list(request)
        router_id = neutron.router_list(request)[0].id
        # pass router_id as part of the call to routerrule_list
        status, result = routerrule_list(request, router_id=router_id)
        return {'items': result}
