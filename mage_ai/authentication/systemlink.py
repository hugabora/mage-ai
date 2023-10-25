from typing import Dict
from mage_ai import settings
from mage_ai.orchestration.db.models.oauth import Role
from sl_userservices_client.policy_evaluator import PolicyEvaluator
from sl_userservices_client.user_services_client import UserServicesClient
from sl_userservices_client.resource_id import ResourceId
import requests


def get_systemlink_auth_info(session_id: str) -> Dict:
    url = settings.SYSTEMLINK_UI_URL + "/niauth/v1/auth"

    headers = {
        "Accept": "application/json",
        "Cookie": "session-id={};".format(session_id),
    }

    resp = requests.get(url, headers=headers)
    result = resp.json()

    if settings.SYSTEMLINK_SSO_TRY_FAKE_AUTH:
        import os
        import json
        fake_path = '/home/src/mage_ai/authentication/auth_fake.json'
        if os.path.isfile(fake_path):
            f = open(fake_path, "r")
            result = json.loads(f.read())

    return result


def translate_user_privs_to_role(workspace_id: str, auth_resp: Dict) -> [Role]:
    print("TODO Correct rules for privilege mappings")

    policies_json = auth_resp.get("policies")
    policies = UserServicesClient._convert_to_auth_policies(policies_json)

    resource_id = ResourceId("Notebook", workspace_id)

    can_create = PolicyEvaluator.is_resource_allowed(
        resource_id, "webapp:CreateWebApp", policies
    )
    if can_create:
        return [Role.get_role(Role.DefaultRole.OWNER)]

    can_read = PolicyEvaluator.is_resource_allowed(
        resource_id, "webapp:GetWebApp", policies
    )
    if can_read:
        return [Role.get_role(Role.DefaultRole.VIEWER)]

    return None
