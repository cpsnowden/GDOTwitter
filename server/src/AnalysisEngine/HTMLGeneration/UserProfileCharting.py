from string import Template
import os
from AnalysisEngine.UserProfiling.UserProfile import UserProfile

DIR_NAME = os.path.dirname(__file__)

base_chart = {
    "paletteColors": "#0075c2,#1aaf5d,#f2c500,#f45b00,#8e0000",
    "bgColor": "#000000,#000000",
    "showBorder": "0",
    "canvasBgAlpha": "0",
    "bgAlpha": "100",
    "use3DLighting": "0",
    "showShadow": "0",
    "enableSmartLabels": "0",
    "startingAngle": "0",
    "decimals": "1",
    "subcaptionFontSize": "14",
    "subcaptionFontBold": "0",
    "toolTipColor": "#ffffff",
    "toolTipBorderThickness": "0",
    "toolTipBgColor": "#000000",
    "toolTipBgAlpha": "80",
    "toolTipBorderRadius": "2",
    "toolTipPadding": "5",
    "showLegend": "0",
    "useDataPlotColorForLabels": "1",
    "chartLeftMargin": "0",
    "chartRightMargin": "0",
    "charTopMargin": "0",
    "charBottomMargin": "0"
}


def get_user_profile_chart(user_profile):
    return get_html(os.path.join(DIR_NAME, "Templates", "UserProfileTemplateBlack.html"), user_profile)


def get_html(file, u):
    s = Template(open(os.path.join(DIR_NAME, "Templates", file)).read())
    return s.safe_substitute({
        "profileImage": u.profileImage,
        "name": u.name,
        "screenName": u.screenName,
        "location": u.location,
        "description": u.description,
        "createdAt": u.createdAt.strftime("%c"),
        "timeZone": u.timeZone,
        "retweetData": get_retweet_chart(u, base_chart),
        "followingData": get_following_data(u, base_chart),
        "tbody": get_tbody(u),
        "markers": u.marker,
        "dataSetName": u.dataSetName,
        "timestamp": u.timestamp.strftime("%c")
    })


def get_tbody(u):
    body = "<tbody>"
    for t in u.tweets:
        if t["retweet_author"] != "":
            body += '<tr class="retweet_row">'
        else:
            body += '<tr>'
        body += "<td>" + t["dt"].strftime("%c") + "</td><td>" + t["text"] + "</td><td>" + t[
            "retweet_author"] + "</td></tr>"
    return body + "</tbody>"


def get_following_data(u, bc):
    return {
        "chart": bc,
        "data": [
            {
                "label": "Followers",
                "value": u.no_followers
            },
            {
                "label": "Friends",
                "value": u.no_friends
            },
        ]
    }


def get_retweet_chart(u, bc):
    return {
        "chart": bc,
        "data": [
            {
                "label": "Retweets",
                "value": u.no_retweets
            },
            {
                "label": "Original",
                "value": u.no_original
            },
        ]
    }

if __name__ == "__main__":

    import datetime
    u = UserProfile("Joe Blogs", "Demo")
    u.profileImage = "http://pbs.twimg.com/profile_images/723651801673818113/lAuGLkjk.jpg"
    u.no_followers = 20
    u.name = "Joe Blogs"
    u.screenName = "Someone"
    u.tweets = [{"dt":datetime.datetime.now(),"text":"sdagsdg","retweet_author":"blob"},
                {"dt":datetime.datetime.now(),"text":"sdagsdg","retweet_author":""}]  * 500
    u.marker = [{"position":{"lat": -25.363, "lng": 131.044},"title":"blah"}]
    html = get_user_profile_chart(u)
    with open("out.html","w") as f:
        f.write(html)
