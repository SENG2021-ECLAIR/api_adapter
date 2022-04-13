"""
All the team functionality
"""

from api_adapter.database import get_user_from_token, register_team


def create_team(token: str, team_name: str) -> dict:
    user = get_user_from_token(token)
    msg = register_team(team_name, user)
    return msg


def invite_member():
    pass


def list_team_invoices():
    pass


def list_team_members():
    pass


def team_stats():
    pass


def leave_team():
    pass
