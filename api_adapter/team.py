"""
All the team functionality
"""

from api_adapter.database import (
    add_user_to_team,
    check_logged_in_token,
    connect_to_db,
    get_invoices_email,
    get_members_of,
    get_user_from_token,
    register_team,
)


def check_role(role: str) -> bool:
    valid_roles = ["Owner", "Member"]
    return role in valid_roles


def create_team(token: str, team_name: str) -> dict:
    user = get_user_from_token(token)
    msg = register_team(team_name, user)
    return {"msg": msg}


def invite_member(team_name: str, invitee_email: str, role: str) -> dict:
    if not check_role(role):
        role = "Member"
    msg = add_user_to_team(team_name, invitee_email, role)
    return {"msg": msg}


def list_team_invoices(token: str) -> Tuple[list, str]:
    """
    Given a team name, create a dictionary of all invoices
    associated with that team.
    """

    if not check_logged_in_token(token):
        return {"message": "The following user could not be logged in"}
    user = get_user_from_token(token)
    team_name = user["team"]
    team_members = get_members_of(team_name, None)
    created = []
    received = []
    for member in team_members[1]:
        member_email = member["email"]
        member_invoices = get_invoices_email(member_email)
        for created_invoice in member_invoices[0]["created"]:
            created.append(created_invoice)
        for received_invoice in member_invoices[0]["received"]:
            received.append(received_invoice)
    return (
        {"created": created, "received": received},
        f"Successfully retreived invoices for team {team_name}",
    )


def list_team_members(token: str, role: str) -> dict:
    """
    Given a token and a role, list the members of the
    logged_in users team with that role.
    """
    user = get_user_from_token(token)
    if not check_role(role):
        role = None
    msg, members = get_members_of(user["team"], role)
    return {"msg": msg, "members": members}


def team_stats():
    pass


def leave_team():
    pass
