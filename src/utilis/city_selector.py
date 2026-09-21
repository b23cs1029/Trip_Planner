def final_city_list(web_response, agent_response):
    final_list = []
    for agent_city in agent_response:
        for res in web_response:
            if res["name"] in agent_city:
                final_list.append(res["name"])
                break
    return final_list