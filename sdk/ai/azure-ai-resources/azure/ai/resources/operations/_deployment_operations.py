# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import ast
import os
import tempfile
import uuid
from pathlib import Path
from typing import Any, List, Union

import mlflow
import yaml

from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineDeployment, ManagedOnlineEndpoint, Model
from azure.core.exceptions import ResourceExistsError
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.v2020_10_01_preview.models import RoleAssignmentCreateParameters

from .._utils._registry_utils import get_registry_model
from .._utils._deployment_utils import get_default_allowed_instance_type_for_hugging_face
from ..entities.deployment import Deployment
from ..entities.models import FoundationModel, LocalModel


class DeploymentOperations:
    def __init__(self, ml_client: MLClient, connections, **kwargs) -> None:
        self._ml_client = ml_client
        self._connections = connections
        self._role_definition_client = AuthorizationManagementClient(
            credential=self._ml_client._credential,
            subscription_id=self._ml_client.subscription_id,
            api_version="2018-01-01-preview",
        )
        self._role_assignment_client = AuthorizationManagementClient(
            credential=self._ml_client._credential,
            subscription_id=self._ml_client.subscription_id,
            api_version="2020-10-01-preview",
        )

    def create_or_update(self, deployment: Deployment) -> Any:
        model = deployment.model
        endpoint_name = deployment.endpoint_name if deployment.endpoint_name else deployment.name

        if deployment.managed_identity:
            from azure.ai.ml.entities import IdentityConfiguration, ManagedIdentityConfiguration

            endpoint_identity = IdentityConfiguration(
                type="user_assigned",
                user_assigned_identities=[
                    ManagedIdentityConfiguration(
                        client_id=deployment.managed_identity.client_id,
                        resource_id=deployment.managed_identity.resource_id,
                        principal_id=deployment.managed_identity.principal_id,
                    )
                ],
            )
        else:
            endpoint_identity = None
        v2_endpoint = ManagedOnlineEndpoint(
            name=endpoint_name,
            auth_mode="key",
            identity=endpoint_identity,
        )
        created_endpoint = self._ml_client.begin_create_or_update(v2_endpoint).result()
        model = deployment.model
        if isinstance(model, LocalModel):
            if not deployment.instance_type:
                deployment.instance_type = "Standard_DS3_v2"
            if model.conda_file and model.loader_module:
                with tempfile.TemporaryDirectory() as tmpdir:
                    mlflow_model_path = f"{tmpdir}/mlflow_model"
                    mlflow.pyfunc.save_model(
                        mlflow_model_path,
                        loader_module=model.loader_module.removesuffix(".py"),
                        data_path=Path(model.path).resolve().as_posix(),
                        code_path=[str(path) for path in Path(model.path).glob("**/*")],
                        conda_env=str(Path(model.path).joinpath(model.conda_file).as_posix()),
                    )

                    if os.name == "nt":
                        # we have to hack the MLModel's "data" field since it logs paths according to the underlying OS
                        # i.e. windows will have "\" in the path instead of "/". This causes issues when the deployment has
                        # to read from the path since this path is it not a standard posix path.
                        with open(f"{mlflow_model_path}/MLModel", "r") as f:
                            d = yaml.safe_load(f)
                            d["flavors"]["python_function"]["data"] = d["flavors"]["python_function"]["data"].replace(
                                "\\", "/"
                            )

                        with open(f"{mlflow_model_path}/MLModel", "w+") as f:
                            yaml.dump(d, f)
            else:
                # validate that path has an mlmodel file and continue
                if "mlmodel" not in [path.lower() for path in os.listdir(model.path)]:
                    raise Exception(
                        "An MLModel file must be present in model directory if not"
                        " specifying conda file and loader module for deployment."
                    )
                mlflow_model_path = model.path

            # attempt to grant endpoint SAI access to workspace:
            if not endpoint_identity:
                try:
                    role_name = "AzureML Data Scientist"
                    scope = self._ml_client.workspaces.get(name=self._ml_client.workspace_name).id
                    system_principal_id = created_endpoint.identity.principal_id

                    role_defs = self._role_definition_client.role_definitions.list(scope=scope)
                    role_def = next((r for r in role_defs if r.role_name == role_name))

                    self._role_assignment_client.role_assignments.create(
                        scope=scope,
                        role_assignment_name=str(uuid.uuid4()),
                        parameters=RoleAssignmentCreateParameters(
                            role_definition_id=role_def.id, principal_id=system_principal_id
                        ),
                    )
                except ResourceExistsError as e:
                    print(
                        "System-assigned identity already has access to project. Skipping granting it access to project"
                    )
                except Exception as e:
                    print(
                        "Unable to grant endpoint system-assigned identity access to workspace. "
                        "Please pass a user-assigned identity through the 'managed_identity' field of the Deployment object "
                        "with permissions to the project instead. Please see https://aka.ms/aistudio/docs/endpoints for more information."
                    )
                    raise e
                uai_env_var = {}
            else:
                uai_env_var = {
                    "UAI_CLIENT_ID": deployment.managed_identity.client_id,
                }
            deployment_environment_variables = (
                deployment.environment_variables if deployment.environment_variables else {}
            )
            v2_deployment = ManagedOnlineDeployment(
                name=deployment.name,
                endpoint_name=endpoint_name,
                model=Model(name=f"{deployment.name}-deployment-model", path=mlflow_model_path, type="mlflow_model"),
                instance_type=deployment.instance_type,
                instance_count=1,
                environment_variables={
                    "AZURE_SUBSCRIPTION_ID": self._ml_client.subscription_id,
                    "AZURE_RESOURCE_GROUP_NAME": self._ml_client.resource_group_name,
                    "AZURE_PROJECT_NAME": self._ml_client.workspace_name,
                    **uai_env_var,
                    **deployment_environment_variables,
                },
            )
            create_deployment_poller = self._ml_client.begin_create_or_update(v2_deployment)
            created_deployment = create_deployment_poller.result()

            created_endpoint.traffic = {deployment.name: 100}
            update_endpoint_poller = self._ml_client.begin_create_or_update(created_endpoint)
            updated_endpoint = update_endpoint_poller.result()

            return Deployment(
                name=created_deployment.name,
                model=created_deployment.model,
                endpoint_name=updated_endpoint.name,
                environment_variables=deployment.environment_variables,
                instance_type=deployment.instance_type,
            )
        if isinstance(model, FoundationModel):
            model_details = get_registry_model(
                model.registry_name,
                self._ml_client._credential,
                model_name=model.name,
                version=model.version,
                label="latest" if not model.version else None,
            )
            model_id = model_details.id

            if not deployment.instance_type:
                if model.registry_name == "HuggingFace":
                    default_instance_type, allowed_instance_types = get_default_allowed_instance_type_for_hugging_face(
                        model_details, self._ml_client._credential
                    )
                    self._check_default_instance_type_and_populate(
                        default_instance_type, deployment, allowed_instance_types=allowed_instance_types
                    )

                if model.registry_name == "azureml":
                    default_instance_type = model_details.properties["inference-recommended-sku"]
                    min_sku_spec = model_details.properties["inference-min-sku-spec"].split("|")
                    self._check_default_instance_type_and_populate(
                        default_instance_type, deployment, min_sku_spec=min_sku_spec
                    )
                if model.registry_name == "azureml-meta":
                    allowed_skus = ast.literal_eval(model_details.tags["inference_compute_allow_list"])
                    # check available quota for each sku in the allowed_sku list
                    # pick the sku that has available quota and is the cheapest
                    vm_sizes = self._ml_client.compute._vmsize_operations.list(
                        location=self._ml_client.compute._get_workspace_location()
                    )
                    # create mapping of allowed SKU to (SKU family, number of vCPUs, and cost per hour on linux)
                    filtered_vm_sizes = [vm_size for vm_size in vm_sizes.value if vm_size.name in allowed_skus]
                    sku_to_family_vcpu_cost_map = {}
                    sku_families = []
                    for vm_size in filtered_vm_sizes:
                        cost = None
                        for vm_price in vm_size.estimated_vm_prices.values:
                            if vm_price.os_type == "Linux" and vm_price.vm_tier == "Standard":
                                cost = vm_price.retail_price
                        sku_to_family_vcpu_cost_map[vm_size.name] = (vm_size.family, vm_size.v_cp_us, cost)
                        sku_families.append(vm_size.family)

                    # sort allowed skus by price and find the first vm that has enough quota
                    sku_to_family_vcpu_cost_map = dict(
                        sorted(sku_to_family_vcpu_cost_map.items(), key=lambda item: item[1][2])
                    )
                    # get usage info and filter it down to dedicated usage for each SKU family
                    usage_info = self._ml_client.compute.list_usage()
                    filtered_usage_info = {
                        filtered_usage.name["value"]: filtered_usage
                        for filtered_usage in [
                            usage
                            for usage in usage_info
                            if usage.name["value"] in sku_families and "Dedicated" in usage.name["localized_value"]
                        ]
                    }

                    # loop over each sku and check if the family has enough cores available that will not
                    # exceed family limit
                    for sku_name, sku_details in sku_to_family_vcpu_cost_map.items():
                        family, vcpus, cost = sku_details
                        family_usage = filtered_usage_info[family]
                        if deployment.instance_count * vcpus + family_usage.current_value <= family_usage.limit:
                            deployment.instance_type = sku_name
                            break
                    if not deployment.instance_type:
                        # if not enough quota, raise an exception and list out SKUs that user needs to request quota for
                        raise Exception(
                            f"There is no quota in the project's region for these model's allowed inference instance types: {allowed_skus}. "
                            "Please request a quota increase for one of these instance types or try to deploying to a project in a region "
                            "with more quota."
                        )

            v2_deployment = ManagedOnlineDeployment(
                name=deployment.name,
                endpoint_name=endpoint_name,
                model=model_id,
                instance_type=deployment.instance_type,
                instance_count=1,
            )

            create_deployment_poller = self._ml_client.begin_create_or_update(v2_deployment)
            created_deployment = create_deployment_poller.result()

            created_endpoint.traffic = {deployment.name: 100}
            update_endpoint_poller = self._ml_client.begin_create_or_update(created_endpoint)
            updated_endpoint = update_endpoint_poller.result()

            return Deployment(
                name=created_deployment.name,
                model=created_deployment.model,
                endpoint_name=updated_endpoint.name,
                instance_type=deployment.instance_type,
            )

    def get(self, name: str, endpoint_name: str = None) -> Any:
        deployment = self._ml_client.online_deployments.get(
            name=name,
            endpoint_name=endpoint_name if endpoint_name else name,
        )

        return Deployment(
            name=deployment.name,
            model=deployment.model,
            endpoint_name=deployment.endpoint_name,
            environment_variables=deployment.environment_variables,
            instance_type=deployment.instance_type,
        )

    def delete(self, name: str, endpoint_name: str = None) -> None:
        self._ml_client.online_deployments.delete(
            name=name,
            endpoint_name=endpoint_name if endpoint_name else name,
        ).result()

    def invoke(self, name: str, request_file: Union[str, os.PathLike], endpoint_name: str = None) -> Any:
        return self._ml_client.online_endpoints.invoke(
            endpoint_name=endpoint_name if endpoint_name else name,
            request_file=request_file,
            deployment_name=name,
        )

    def _check_default_instance_type_and_populate(
        self,
        instance_type: str,
        deployment: Deployment,
        allowed_instance_types: List[str] = None,
        min_sku_spec: str = None,
    ) -> bool:
        vm_sizes = self._ml_client.compute.list_sizes()
        inference_sku_vm_info = [vm for vm in vm_sizes if vm.name == instance_type][0]
        usage_info = self._ml_client.compute.list_usage()
        # from the list of all usage, get the usage specific to the recommend sku's family
        sku_family_usage = next(
            (
                usage
                for usage in usage_info
                if (
                    usage.name["value"] == inference_sku_vm_info.family and "Dedicated" in usage.name["localized_value"]
                )
            )
        )

        # if the family has enough cores available that will not exceed family limit, choose as deployment sku
        if (
            sku_family_usage.current_value + inference_sku_vm_info.v_cp_us * deployment.instance_count
            <= sku_family_usage.limit
        ):
            deployment.instance_type = instance_type
        else:
            exception_message = f"The recommended inference instance type for this model is {instance_type}, for which there is not enough quota.\n"
            if allowed_instance_types:
                exception_message += (
                    f"The following instance types are allowed for this model: {allowed_instance_types}. Please provide an instance type from this "
                    "list for which there is enough quota."
                )
            elif min_sku_spec:
                cpu, gpu, ram, storage = min_sku_spec.split("|")

                exception_message += (
                    f"Please provide an instance_type that meets the following minimum parameters: {cpu} vCPU cores, {gpu} GPU cores, "
                    f"{ram} GB of vRAM, {storage} GB of storage."
                )
            raise Exception(exception_message)
