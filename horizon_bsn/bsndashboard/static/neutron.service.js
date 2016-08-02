/**
 * Copyright 2015 IBM Corp.
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
(function () {
  'use strict';

  angular
    .module('horizon.app.core.openstack-service-api')
    .factory('horizon.app.core.openstack-service-api.bsnneutron', neutronAPI);

  neutronAPI.$inject = [
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service'
  ];

  /**
   * @ngdoc service
   * @name neutronAPI
   * @param {Object} apiService
   * @param {Object} toastService
   * @description Provides access to Neutron APIs.
   * @returns {Object} The service
   */
  function neutronAPI(apiService, toastService) {
    var service = {
      reachabilitytest_create: reachabilitytest_create,
      reachabilitytest_list: reachabilitytest_list,
      // reachabilitytest_get: reachabilitytest_get,
      reachabilitytest_run: reachabilitytest_run,
      reachabilitytest_delete: reachabilitytest_delete,

      networktemplate_create: networktemplate_create,
      networktemplate_list: networktemplate_list,
      networktemplate_get: networktemplate_get,
      networktemplate_update: networktemplate_update,
      networktemplate_delete: networktemplate_delete,

      // networktemplateassignment_create: networktemplateassignment_create,
      networktemplateassignment_list: networktemplateassignment_list,
      // networktemplateassignment_get: networktemplateassignment_get,
      // networktemplateassignment_update: networktemplateassignment_update,
      networktemplateassignment_delete: networktemplateassignment_delete,
      //
      reachabilityquicktest_create: reachabilityquicktest_create,
      // reachabilityquicktest_list: reachabilityquicktest_list,
      reachabilityquicktest_get: reachabilityquicktest_get,
      reachabilityquicktest_update: reachabilityquicktest_update,
      // reachabilityquicktest_delete: reachabilityquicktest_delete

      router_get: router_get,
      router_update: router_update
    };

    return service;

    /////////////

    // Neutron Services


    /**
     * //////////////////////////////////////////
     * REACHABILITY TESTS
     * //////////////////////////////////////////
     */
    /**
     * @name reachabilitytest_create
     * @param {Object} test - The test
     * @description Create a reachability test.
     *
     * @returns {Object} The result of the creation call.
     */
    function reachabilitytest_create(test) {
      return apiService.post('api/neutron/reachabilitytests/', test)
        .error(function () {
          toastService.add('error', gettext('Error creating reachability test'));
        });
    }

    /**
     * @name reachabilitytest_list
     * @description Get the list of reachability tests.
     *
     * @returns {Object} An object with property "items." Each item is a test.
     */
    function reachabilitytest_list() {
      return apiService.get('api/neutron/reachabilitytests/')
        .error(function () {
          toastService.add('error', gettext('Error getting reachability tests'));
        });
    }

    /**
     * @name reachabilitytest_list
     * @description Get the list of reachability tests.
     *
     * @returns {Object} An object with property "items." Each item is a test.
     */
    function reachabilitytest_run(id) {
      return apiService.patch('api/neutron/reachabilitytests/' + id + '/')
        .error(function () {
          toastService.add('error', gettext('Error running reachability tests'));
        });
    }

    /**
     * @name reachabilitytest_delete
     * @description Delete a reachability test.
     *
     * @returns {Object} An object with property "items." Each item is a test.
     */
    function reachabilitytest_delete(id) {
      return apiService.delete('api/neutron/reachabilitytests/' + id + '/')
        .error(function() {
          toastService.add('error', gettext('Error deleting reachability test'));
        });
    }

    /**
     * //////////////////////////////////////////
     * QUICK TESTS
     * //////////////////////////////////////////
     */

    /**
     * @name reachabilityquicktest_get
     * @param {Object} test - The test
     * @description Get a reachability quick test.
     *
     * @returns {Object} The result of the get call.
     */
    function reachabilityquicktest_get(tenant_id) {
      return apiService.get('api/neutron/reachabilitytests/' + tenant_id + '/')
        .error(function () {
          toastService.add('error', gettext('Error getting reachability test'));
        });
    }

    /**
     * @name reachabilityquicktest_create
     * @param {Object} test - The test
     * @description Create a reachability quick test.
     *
     * @returns {Object} The result of the creation call.
     */
    function reachabilityquicktest_create(test) {
      return apiService.post('api/neutron/reachabilitytests/', test)
        .error(function () {
          toastService.add('error', gettext('Error creating reachability test'));
        });
    }

    /**
     * @name reachabilityquicktest_patch
     * @param {Object} test - The test
     * @description Patch a reachability quick test.
     *
     * @returns {Object} The result of the patch call.
     */
    function reachabilityquicktest_update(tenant_id, test) {
      return apiService.patch('api/neutron/reachabilitytests/' + tenant_id + '/', test)
        .error(function () {
          toastService.add('error', gettext('Error patching reachability test'));
        });
    }

    /**
     * //////////////////////////////////////////
     * ADMIN NETWORK TEMPLATES
     * //////////////////////////////////////////
     */

    /**
     * @name reachabilitytest_list
     * @description Get the list of reachability tests.
     *
     * @returns {Object} An object with property "items." Each item is a test.
     */
    function networktemplate_create(template) {
      return apiService.post('api/neutron/networktemplate/', template)
        .error(function() {
          toastService.add('error', gettext('Error creating networktemplate'));
        });
    }

    /**
     * @name reachabilitytest_list
     * @description Get the list of reachability tests.
     *
     * @returns {Object} An object with property "items." Each item is a test.
     */
    function networktemplate_list() {
      return apiService.get('api/neutron/networktemplate/')
        .error(function() {
          toastService.add('error', gettext('Error getting network templates'));
        });
    }

    /**
     * @name reachabilitytest_list
     * @description Get the list of reachability tests.
     *
     * @returns {Object} An object with property "items." Each item is a test.
     */
    function networktemplate_get(id) {
      return apiService.get('api/neutron/networktemplate/' + id + '/')
        .error(function() {
          toastService.add('error', gettext('Error getting networktemplate'));
        });
    }

    /**
     * @name reachabilitytest_list
     * @description Get the list of reachability tests.
     *
     * @returns {Object} An object with property "items." Each item is a test.
     */
    function networktemplate_update(id, template) {
      return apiService.patch('api/neutron/networktemplate/' + id + '/', template)
        .error(function() {
          toastService.add('error', gettext('Error updating networktemplate'));
        });
    }

    /**
     * @name reachabilitytest_list
     * @description Get the list of reachability tests.
     *
     * @returns {Object} An object with property "items." Each item is a test.
     */
    function networktemplate_delete(id) {
      return apiService.delete('api/neutron/networktemplate/' + id + '/')
        .error(function() {
          toastService.add('error', gettext('Error deleting networktemplate'));
        });
    }

    /**
     * //////////////////////////////////////////
     * NETWORK TEMPLATE ASSIGNMENT
     * //////////////////////////////////////////
     */

    /**
     * @name reachabilitytest_list
     * @description Get the list of reachability tests.
     *
     * @returns {Object} An object with property "items." Each item is a test.
     */
    function networktemplateassignment_list() {
      return apiService.get('api/neutron/networktemplateassignment/')
        .error(function() {
          toastService.add('error', gettext('Error getting network template assignment'));
        });
    }

    /**
     * @name reachabilitytest_list
     * @description Get the list of reachability tests.
     *
     * @returns {Object} An object with property "items." Each item is a test.
     */
    function networktemplateassignment_delete(id) {
      return apiService.delete('api/neutron/networktemplateassignment/' + id + '/').then(
        function success(response) {
          debugger;
          return response;
        },
        function error() {
          debugger;
          toastService.add('error', gettext('Error deleting network template assignment'));
        },
        function notify() {
          debugger;
          console.log("Here's a notification");
        }
      );
    }

    /**
     * //////////////////////////////////////////
     * ROUTER RULES
     * //////////////////////////////////////////
     */

    function router_get() {
      return apiService.get('api/neutron/router/')
        .error(function() {
          toastService.add('error', gettext('Error getting router id'));
        });
    }

    function router_update(router) {
      return apiService.patch('api/neutron/router/', router)
        .error(function() {
          toastService.add('error', gettext('Error updating router'));
        });
    }

  }

}());