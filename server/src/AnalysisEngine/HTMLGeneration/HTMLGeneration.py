
from AnalysisEngine.HTMLGeneration.Charting import create_chart
from AnalysisEngine.HTMLGeneration.UserProfileCharting import get_user_profile_chart


def get_html(result_obj, html_type):


    option = {
        "chart": create_chart,
        "userProfile": get_user_profile_chart
    }

    return option.get(html_type, lambda x:  "")(result_obj)