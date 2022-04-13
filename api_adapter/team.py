"""
All the team functionality
"""

from api_adapter.database import add_user_to_team, get_user_from_token, register_team


def create_team(token: str, team_name: str) -> dict:
    user = get_user_from_token(token)
    msg = register_team(team_name, user)
    return {"msg": msg}


def invite_member(team_name: str, invitee_email: str, role: str) -> dict:
    valid_roles = ["Owner", "Member"]
    if role not in valid_roles:
        role = "Member"
    msg = add_user_to_team(team_name, invitee_email, role)
    return {"msg": msg}


def list_team_invoices(team_name: str) -> dict:
    pass


def list_team_members(team_name: str) -> dict:
    pass


def team_stats():
    pass


def leave_team():
    pass
