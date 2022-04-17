"""
All the team functionality
"""

from api_adapter.database import (
    add_user_to_team,
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


def list_team_invoices(team_name: str) -> dict:
    pass


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


def team_stats(token: str, chart: str) -> dict:
    user = get_user_from_token(token)
    if chart == "pie":
        stats = team_pie_chart(user["team"])
        msg = f"Successfully got pie chart data from {user['team']}"
    elif chart == "OTHER":
        pass
    return {"msg": msg, "stats": stats}


def team_pie_chart(team_name: str) -> dict:
    """
    Given a team name, get pie chart stats
    """
    stats = {"users": []}
    total = 0
    _, members = get_members_of(team_name, None)
    for member in members:
        num_invoices = len(member["invoices"])
        stats["users"].append(
            {
                "email": member["email"],
                "firstname": member["firstname"],
                "lastname": member["lastname"],
                "num_invoices": num_invoices,
            }
        )
        total += num_invoices

    stats["total_invoices"] = total
    return stats


def leave_team():
    pass
