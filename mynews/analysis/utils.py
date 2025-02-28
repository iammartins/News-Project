from user_agents import parse

def get_client_info(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)

    device_type = 'other'
    if user_agent.is_mobile:
        device_type = 'mobile'
    elif user_agent.is_tablet:
        device_type = 'tablet'
    elif user_agent.is_pc:
        device_type = 'desktop'

    return {
        'http_referer': request.META.get('HTTP_REFERER'),
        'user_agent': user_agent_string,
        'device_type': device_type
    }