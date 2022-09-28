# pylint: disable=too-many-lines
# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
from typing import Any, AsyncIterable, Callable, Dict, IO, Optional, TypeVar, Union, overload
from urllib.parse import parse_qs, urljoin, urlparse

from azure.core.async_paging import AsyncItemPaged, AsyncList
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError, ResourceExistsError, ResourceNotFoundError, ResourceNotModifiedError, map_error
from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpResponse
from azure.core.rest import HttpRequest
from azure.core.tracing.decorator import distributed_trace
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.utils import case_insensitive_dict
from azure.mgmt.core.exceptions import ARMErrorFormat

from ... import models as _models
from ..._vendor import _convert_request
from ...operations._jit_network_access_policies_operations import build_create_or_update_request, build_delete_request, build_get_request, build_initiate_request, build_list_by_region_request, build_list_by_resource_group_and_region_request, build_list_by_resource_group_request, build_list_request
T = TypeVar('T')
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]

class JitNetworkAccessPoliciesOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~azure.mgmt.security.v2020_01_01.aio.SecurityCenter`'s
        :attr:`jit_network_access_policies` attribute.
    """

    models = _models

    def __init__(self, *args, **kwargs) -> None:
        input_args = list(args)
        self._client = input_args.pop(0) if input_args else kwargs.pop("client")
        self._config = input_args.pop(0) if input_args else kwargs.pop("config")
        self._serialize = input_args.pop(0) if input_args else kwargs.pop("serializer")
        self._deserialize = input_args.pop(0) if input_args else kwargs.pop("deserializer")


    @distributed_trace
    def list(
        self,
        **kwargs: Any
    ) -> AsyncIterable["_models.JitNetworkAccessPolicy"]:
        """Policies for protecting resources using Just-in-Time access control.

        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either JitNetworkAccessPolicy or the result of
         cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicy]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop('api_version', _params.pop('api-version', "2020-01-01"))  # type: str
        cls = kwargs.pop('cls', None)  # type: ClsType[_models.JitNetworkAccessPoliciesList]

        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError, 304: ResourceNotModifiedError
        }
        error_map.update(kwargs.pop('error_map', {}) or {})
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_list_request(
                    subscription_id=self._config.subscription_id,
                    api_version=api_version,
                    template_url=self.list.metadata['url'],
                    headers=_headers,
                    params=_params,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)  # type: ignore

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urlparse(next_link)
                _next_request_params = case_insensitive_dict(parse_qs(_parsed_next_link.query))
                _next_request_params["api-version"] = self._config.api_version
                request = HttpRequest("GET", urljoin(next_link, _parsed_next_link.path), params=_next_request_params)
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)  # type: ignore
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("JitNetworkAccessPoliciesList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
                request,
                stream=False,
                **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response


        return AsyncItemPaged(
            get_next, extract_data
        )
    list.metadata = {'url': "/subscriptions/{subscriptionId}/providers/Microsoft.Security/jitNetworkAccessPolicies"}  # type: ignore

    @distributed_trace
    def list_by_region(
        self,
        asc_location: str,
        **kwargs: Any
    ) -> AsyncIterable["_models.JitNetworkAccessPolicy"]:
        """Policies for protecting resources using Just-in-Time access control for the subscription,
        location.

        :param asc_location: The location where ASC stores the data of the subscription. can be
         retrieved from Get locations. Required.
        :type asc_location: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either JitNetworkAccessPolicy or the result of
         cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicy]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop('api_version', _params.pop('api-version', "2020-01-01"))  # type: str
        cls = kwargs.pop('cls', None)  # type: ClsType[_models.JitNetworkAccessPoliciesList]

        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError, 304: ResourceNotModifiedError
        }
        error_map.update(kwargs.pop('error_map', {}) or {})
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_list_by_region_request(
                    asc_location=asc_location,
                    subscription_id=self._config.subscription_id,
                    api_version=api_version,
                    template_url=self.list_by_region.metadata['url'],
                    headers=_headers,
                    params=_params,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)  # type: ignore

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urlparse(next_link)
                _next_request_params = case_insensitive_dict(parse_qs(_parsed_next_link.query))
                _next_request_params["api-version"] = self._config.api_version
                request = HttpRequest("GET", urljoin(next_link, _parsed_next_link.path), params=_next_request_params)
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)  # type: ignore
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("JitNetworkAccessPoliciesList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
                request,
                stream=False,
                **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response


        return AsyncItemPaged(
            get_next, extract_data
        )
    list_by_region.metadata = {'url': "/subscriptions/{subscriptionId}/providers/Microsoft.Security/locations/{ascLocation}/jitNetworkAccessPolicies"}  # type: ignore

    @distributed_trace
    def list_by_resource_group(
        self,
        resource_group_name: str,
        **kwargs: Any
    ) -> AsyncIterable["_models.JitNetworkAccessPolicy"]:
        """Policies for protecting resources using Just-in-Time access control for the subscription,
        location.

        :param resource_group_name: The name of the resource group within the user's subscription. The
         name is case insensitive. Required.
        :type resource_group_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either JitNetworkAccessPolicy or the result of
         cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicy]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop('api_version', _params.pop('api-version', "2020-01-01"))  # type: str
        cls = kwargs.pop('cls', None)  # type: ClsType[_models.JitNetworkAccessPoliciesList]

        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError, 304: ResourceNotModifiedError
        }
        error_map.update(kwargs.pop('error_map', {}) or {})
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_list_by_resource_group_request(
                    resource_group_name=resource_group_name,
                    subscription_id=self._config.subscription_id,
                    api_version=api_version,
                    template_url=self.list_by_resource_group.metadata['url'],
                    headers=_headers,
                    params=_params,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)  # type: ignore

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urlparse(next_link)
                _next_request_params = case_insensitive_dict(parse_qs(_parsed_next_link.query))
                _next_request_params["api-version"] = self._config.api_version
                request = HttpRequest("GET", urljoin(next_link, _parsed_next_link.path), params=_next_request_params)
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)  # type: ignore
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("JitNetworkAccessPoliciesList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
                request,
                stream=False,
                **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response


        return AsyncItemPaged(
            get_next, extract_data
        )
    list_by_resource_group.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Security/jitNetworkAccessPolicies"}  # type: ignore

    @distributed_trace
    def list_by_resource_group_and_region(
        self,
        resource_group_name: str,
        asc_location: str,
        **kwargs: Any
    ) -> AsyncIterable["_models.JitNetworkAccessPolicy"]:
        """Policies for protecting resources using Just-in-Time access control for the subscription,
        location.

        :param resource_group_name: The name of the resource group within the user's subscription. The
         name is case insensitive. Required.
        :type resource_group_name: str
        :param asc_location: The location where ASC stores the data of the subscription. can be
         retrieved from Get locations. Required.
        :type asc_location: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: An iterator like instance of either JitNetworkAccessPolicy or the result of
         cls(response)
        :rtype:
         ~azure.core.async_paging.AsyncItemPaged[~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicy]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop('api_version', _params.pop('api-version', "2020-01-01"))  # type: str
        cls = kwargs.pop('cls', None)  # type: ClsType[_models.JitNetworkAccessPoliciesList]

        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError, 304: ResourceNotModifiedError
        }
        error_map.update(kwargs.pop('error_map', {}) or {})
        def prepare_request(next_link=None):
            if not next_link:
                
                request = build_list_by_resource_group_and_region_request(
                    resource_group_name=resource_group_name,
                    asc_location=asc_location,
                    subscription_id=self._config.subscription_id,
                    api_version=api_version,
                    template_url=self.list_by_resource_group_and_region.metadata['url'],
                    headers=_headers,
                    params=_params,
                )
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)  # type: ignore

            else:
                # make call to next link with the client's api-version
                _parsed_next_link = urlparse(next_link)
                _next_request_params = case_insensitive_dict(parse_qs(_parsed_next_link.query))
                _next_request_params["api-version"] = self._config.api_version
                request = HttpRequest("GET", urljoin(next_link, _parsed_next_link.path), params=_next_request_params)
                request = _convert_request(request)
                request.url = self._client.format_url(request.url)  # type: ignore
                request.method = "GET"
            return request

        async def extract_data(pipeline_response):
            deserialized = self._deserialize("JitNetworkAccessPoliciesList", pipeline_response)
            list_of_elem = deserialized.value
            if cls:
                list_of_elem = cls(list_of_elem)
            return deserialized.next_link or None, AsyncList(list_of_elem)

        async def get_next(next_link=None):
            request = prepare_request(next_link)

            pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
                request,
                stream=False,
                **kwargs
            )
            response = pipeline_response.http_response

            if response.status_code not in [200]:
                map_error(status_code=response.status_code, response=response, error_map=error_map)
                raise HttpResponseError(response=response, error_format=ARMErrorFormat)

            return pipeline_response


        return AsyncItemPaged(
            get_next, extract_data
        )
    list_by_resource_group_and_region.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Security/locations/{ascLocation}/jitNetworkAccessPolicies"}  # type: ignore

    @distributed_trace_async
    async def get(
        self,
        resource_group_name: str,
        asc_location: str,
        jit_network_access_policy_name: str,
        **kwargs: Any
    ) -> _models.JitNetworkAccessPolicy:
        """Policies for protecting resources using Just-in-Time access control for the subscription,
        location.

        :param resource_group_name: The name of the resource group within the user's subscription. The
         name is case insensitive. Required.
        :type resource_group_name: str
        :param asc_location: The location where ASC stores the data of the subscription. can be
         retrieved from Get locations. Required.
        :type asc_location: str
        :param jit_network_access_policy_name: Name of a Just-in-Time access configuration policy.
         Required.
        :type jit_network_access_policy_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: JitNetworkAccessPolicy or the result of cls(response)
        :rtype: ~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicy
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError, 304: ResourceNotModifiedError
        }
        error_map.update(kwargs.pop('error_map', {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop('api_version', _params.pop('api-version', "2020-01-01"))  # type: str
        cls = kwargs.pop('cls', None)  # type: ClsType[_models.JitNetworkAccessPolicy]

        
        request = build_get_request(
            resource_group_name=resource_group_name,
            asc_location=asc_location,
            jit_network_access_policy_name=jit_network_access_policy_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.get.metadata['url'],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('JitNetworkAccessPolicy', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    get.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Security/locations/{ascLocation}/jitNetworkAccessPolicies/{jitNetworkAccessPolicyName}"}  # type: ignore


    @overload
    async def create_or_update(
        self,
        resource_group_name: str,
        asc_location: str,
        jit_network_access_policy_name: str,
        body: _models.JitNetworkAccessPolicy,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.JitNetworkAccessPolicy:
        """Create a policy for protecting resources using Just-in-Time access control.

        :param resource_group_name: The name of the resource group within the user's subscription. The
         name is case insensitive. Required.
        :type resource_group_name: str
        :param asc_location: The location where ASC stores the data of the subscription. can be
         retrieved from Get locations. Required.
        :type asc_location: str
        :param jit_network_access_policy_name: Name of a Just-in-Time access configuration policy.
         Required.
        :type jit_network_access_policy_name: str
        :param body: Required.
        :type body: ~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicy
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: JitNetworkAccessPolicy or the result of cls(response)
        :rtype: ~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicy
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def create_or_update(
        self,
        resource_group_name: str,
        asc_location: str,
        jit_network_access_policy_name: str,
        body: IO,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.JitNetworkAccessPolicy:
        """Create a policy for protecting resources using Just-in-Time access control.

        :param resource_group_name: The name of the resource group within the user's subscription. The
         name is case insensitive. Required.
        :type resource_group_name: str
        :param asc_location: The location where ASC stores the data of the subscription. can be
         retrieved from Get locations. Required.
        :type asc_location: str
        :param jit_network_access_policy_name: Name of a Just-in-Time access configuration policy.
         Required.
        :type jit_network_access_policy_name: str
        :param body: Required.
        :type body: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: JitNetworkAccessPolicy or the result of cls(response)
        :rtype: ~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicy
        :raises ~azure.core.exceptions.HttpResponseError:
        """


    @distributed_trace_async
    async def create_or_update(
        self,
        resource_group_name: str,
        asc_location: str,
        jit_network_access_policy_name: str,
        body: Union[_models.JitNetworkAccessPolicy, IO],
        **kwargs: Any
    ) -> _models.JitNetworkAccessPolicy:
        """Create a policy for protecting resources using Just-in-Time access control.

        :param resource_group_name: The name of the resource group within the user's subscription. The
         name is case insensitive. Required.
        :type resource_group_name: str
        :param asc_location: The location where ASC stores the data of the subscription. can be
         retrieved from Get locations. Required.
        :type asc_location: str
        :param jit_network_access_policy_name: Name of a Just-in-Time access configuration policy.
         Required.
        :type jit_network_access_policy_name: str
        :param body: Is either a model type or a IO type. Required.
        :type body: ~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicy or IO
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: JitNetworkAccessPolicy or the result of cls(response)
        :rtype: ~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicy
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError, 304: ResourceNotModifiedError
        }
        error_map.update(kwargs.pop('error_map', {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop('api_version', _params.pop('api-version', "2020-01-01"))  # type: str
        content_type = kwargs.pop('content_type', _headers.pop('Content-Type', None))  # type: Optional[str]
        cls = kwargs.pop('cls', None)  # type: ClsType[_models.JitNetworkAccessPolicy]

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(body, (IO, bytes)):
            _content = body
        else:
            _json = self._serialize.body(body, 'JitNetworkAccessPolicy')

        request = build_create_or_update_request(
            resource_group_name=resource_group_name,
            asc_location=asc_location,
            jit_network_access_policy_name=jit_network_access_policy_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            template_url=self.create_or_update.metadata['url'],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('JitNetworkAccessPolicy', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    create_or_update.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Security/locations/{ascLocation}/jitNetworkAccessPolicies/{jitNetworkAccessPolicyName}"}  # type: ignore


    @distributed_trace_async
    async def delete(  # pylint: disable=inconsistent-return-statements
        self,
        resource_group_name: str,
        asc_location: str,
        jit_network_access_policy_name: str,
        **kwargs: Any
    ) -> None:
        """Delete a Just-in-Time access control policy.

        :param resource_group_name: The name of the resource group within the user's subscription. The
         name is case insensitive. Required.
        :type resource_group_name: str
        :param asc_location: The location where ASC stores the data of the subscription. can be
         retrieved from Get locations. Required.
        :type asc_location: str
        :param jit_network_access_policy_name: Name of a Just-in-Time access configuration policy.
         Required.
        :type jit_network_access_policy_name: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: None or the result of cls(response)
        :rtype: None
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError, 304: ResourceNotModifiedError
        }
        error_map.update(kwargs.pop('error_map', {}) or {})

        _headers = kwargs.pop("headers", {}) or {}
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        api_version = kwargs.pop('api_version', _params.pop('api-version', "2020-01-01"))  # type: str
        cls = kwargs.pop('cls', None)  # type: ClsType[None]

        
        request = build_delete_request(
            resource_group_name=resource_group_name,
            asc_location=asc_location,
            jit_network_access_policy_name=jit_network_access_policy_name,
            subscription_id=self._config.subscription_id,
            api_version=api_version,
            template_url=self.delete.metadata['url'],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200, 204]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        if cls:
            return cls(pipeline_response, None, {})

    delete.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Security/locations/{ascLocation}/jitNetworkAccessPolicies/{jitNetworkAccessPolicyName}"}  # type: ignore


    @overload
    async def initiate(
        self,
        resource_group_name: str,
        asc_location: str,
        jit_network_access_policy_name: str,
        body: _models.JitNetworkAccessPolicyInitiateRequest,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.JitNetworkAccessRequest:
        """Initiate a JIT access from a specific Just-in-Time policy configuration.

        :param resource_group_name: The name of the resource group within the user's subscription. The
         name is case insensitive. Required.
        :type resource_group_name: str
        :param asc_location: The location where ASC stores the data of the subscription. can be
         retrieved from Get locations. Required.
        :type asc_location: str
        :param jit_network_access_policy_name: Name of a Just-in-Time access configuration policy.
         Required.
        :type jit_network_access_policy_name: str
        :param body: Required.
        :type body: ~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicyInitiateRequest
        :keyword content_type: Body Parameter content-type. Content type parameter for JSON body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword jit_network_access_policy_initiate_type: Type of the action to do on the Just-in-Time
         access policy. Default value is "initiate". Note that overriding this default value may result
         in unsupported behavior.
        :paramtype jit_network_access_policy_initiate_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: JitNetworkAccessRequest or the result of cls(response)
        :rtype: ~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessRequest
        :raises ~azure.core.exceptions.HttpResponseError:
        """

    @overload
    async def initiate(
        self,
        resource_group_name: str,
        asc_location: str,
        jit_network_access_policy_name: str,
        body: IO,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> _models.JitNetworkAccessRequest:
        """Initiate a JIT access from a specific Just-in-Time policy configuration.

        :param resource_group_name: The name of the resource group within the user's subscription. The
         name is case insensitive. Required.
        :type resource_group_name: str
        :param asc_location: The location where ASC stores the data of the subscription. can be
         retrieved from Get locations. Required.
        :type asc_location: str
        :param jit_network_access_policy_name: Name of a Just-in-Time access configuration policy.
         Required.
        :type jit_network_access_policy_name: str
        :param body: Required.
        :type body: IO
        :keyword content_type: Body Parameter content-type. Content type parameter for binary body.
         Default value is "application/json".
        :paramtype content_type: str
        :keyword jit_network_access_policy_initiate_type: Type of the action to do on the Just-in-Time
         access policy. Default value is "initiate". Note that overriding this default value may result
         in unsupported behavior.
        :paramtype jit_network_access_policy_initiate_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: JitNetworkAccessRequest or the result of cls(response)
        :rtype: ~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessRequest
        :raises ~azure.core.exceptions.HttpResponseError:
        """


    @distributed_trace_async
    async def initiate(
        self,
        resource_group_name: str,
        asc_location: str,
        jit_network_access_policy_name: str,
        body: Union[_models.JitNetworkAccessPolicyInitiateRequest, IO],
        **kwargs: Any
    ) -> _models.JitNetworkAccessRequest:
        """Initiate a JIT access from a specific Just-in-Time policy configuration.

        :param resource_group_name: The name of the resource group within the user's subscription. The
         name is case insensitive. Required.
        :type resource_group_name: str
        :param asc_location: The location where ASC stores the data of the subscription. can be
         retrieved from Get locations. Required.
        :type asc_location: str
        :param jit_network_access_policy_name: Name of a Just-in-Time access configuration policy.
         Required.
        :type jit_network_access_policy_name: str
        :param body: Is either a model type or a IO type. Required.
        :type body: ~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessPolicyInitiateRequest or IO
        :keyword jit_network_access_policy_initiate_type: Type of the action to do on the Just-in-Time
         access policy. Default value is "initiate". Note that overriding this default value may result
         in unsupported behavior.
        :paramtype jit_network_access_policy_initiate_type: str
        :keyword content_type: Body Parameter content-type. Known values are: 'application/json'.
         Default value is None.
        :paramtype content_type: str
        :keyword callable cls: A custom type or function that will be passed the direct response
        :return: JitNetworkAccessRequest or the result of cls(response)
        :rtype: ~azure.mgmt.security.v2020_01_01.models.JitNetworkAccessRequest
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        error_map = {
            401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError, 304: ResourceNotModifiedError
        }
        error_map.update(kwargs.pop('error_map', {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

        jit_network_access_policy_initiate_type = kwargs.pop('jit_network_access_policy_initiate_type', "initiate")  # type: str
        api_version = kwargs.pop('api_version', _params.pop('api-version', "2020-01-01"))  # type: str
        content_type = kwargs.pop('content_type', _headers.pop('Content-Type', None))  # type: Optional[str]
        cls = kwargs.pop('cls', None)  # type: ClsType[_models.JitNetworkAccessRequest]

        content_type = content_type or "application/json"
        _json = None
        _content = None
        if isinstance(body, (IO, bytes)):
            _content = body
        else:
            _json = self._serialize.body(body, 'JitNetworkAccessPolicyInitiateRequest')

        request = build_initiate_request(
            resource_group_name=resource_group_name,
            asc_location=asc_location,
            jit_network_access_policy_name=jit_network_access_policy_name,
            subscription_id=self._config.subscription_id,
            jit_network_access_policy_initiate_type=jit_network_access_policy_initiate_type,
            api_version=api_version,
            content_type=content_type,
            json=_json,
            content=_content,
            template_url=self.initiate.metadata['url'],
            headers=_headers,
            params=_params,
        )
        request = _convert_request(request)
        request.url = self._client.format_url(request.url)  # type: ignore

        pipeline_response = await self._client._pipeline.run(  # type: ignore # pylint: disable=protected-access
            request,
            stream=False,
            **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [202]:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response, error_format=ARMErrorFormat)

        deserialized = self._deserialize('JitNetworkAccessRequest', pipeline_response)

        if cls:
            return cls(pipeline_response, deserialized, {})

        return deserialized

    initiate.metadata = {'url': "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Security/locations/{ascLocation}/jitNetworkAccessPolicies/{jitNetworkAccessPolicyName}/{jitNetworkAccessPolicyInitiateType}"}  # type: ignore
