from client import get_client


def on_match_success(match):
    coffee_request = match.coffee_request

    requested_user = coffee_request.user_id
    matched_user = match.user_id

    get_client().post_to_channel(f"<@{requested_user}> is going to grab coffee with <@{matched_user}>")

