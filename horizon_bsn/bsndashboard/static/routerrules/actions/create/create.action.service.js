/**
 * (c) Copyright 2016 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  angular
    .module('bsn.bsndashboard.routerrules.actions')
    .factory('bsn.bsndashboard.routerrules.actions.create.service', createService);

  createService.$inject = [
    'bsn.bsndashboard.routerrules.resourceType',
    'bsn.bsndashboard.routerrules.router',
    'horizon.app.core.openstack-service-api.bsnneutron',
    'horizon.framework.widgets.toast.service',
    '$modal',
    'horizon.framework.util.actions.action-result.service',
  ];

  /**
   * @ngDoc factory
   * @name horizon.app.core.images.actions.createService
   * @Description A service to open the user wizard.
   */
  function createService(
    resourceType,
    router,
    bsnneutron,
    toast,
    $modal,
    actionResultService
  ) {
    var message = {
      success: gettext('Template was successfully created.')
    };

    var service = {
      perform: perform,
      allowed: allowed
    };

    return service;

    //////////////
    function allowed() {
      var promise = new Promise(function (resolve) {
        resolve(true);
      });

      return promise;
    }

    function perform() {

      var localSpec = {
        backdrop: 'static',
        controller: 'CreateController as ctrl',
        templateUrl: '/static/routerrules/actions/create/createModal.html'
      };

      return $modal.open(localSpec).result.then(function create(result) {
        if(result.nexthops != "") {
          result.nexthops = result.nexthops.split(",");
        }
        else {
          result.nexthops = [];
        }
        return submit(result);
      });
    }

    function submit(result) {
      return bsnneutron.routerrules_create(result).then(onCreateTemplate);
    }

    function onCreateTemplate(response) {
      var newRule = response.data;
      toast.add('success', interpolate(message.success, [newRule.name]));
      return actionResultService.getActionResult()
        .created(resourceType, newRule.name)
        .result;
    }

  } // end of createService
})(); // end of IIFE
