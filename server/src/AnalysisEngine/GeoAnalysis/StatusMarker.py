class StatusMarker:
    def __init__(self, id):
        self.id = id
        self.text = None
        self.user_pic = None
        self.user_screen_name = None
        self.user_name = None
        self.date = None
        self.retweet_count = None
        self.retweeted_author = None
        self.latitude = None
        self.longitude = None

    def get_profile_pic_html(self):
        return "<img src=" + str(self.user_name) + ">"

    def get_user_name_html(self):
        return "<span style='font-size:6px;color:#000;margin:0'>" + str(self.user_name) + " (@" + \
               str(self.user_screen_name) + ")</span>"

    def get_text_html(self):
        return "<p style='text-align:center;font-size:6px;color:#999;margin:0'>\"" \
               + self.text.replace("\n", "").replace('"', "'") + "\"</p>"

    def get_header_row(self):
        return "<tr><th style='border-bottom: 1px solid #D4EFFC;'>" \
               + self.get_user_name_html() + "    " + self.get_date_html() + "</th></tr>"

    def get_normal_row(self, item):
        return "<tr><td>" + item + "</td></tr>"

    def get_date_html(self):
        return "<span style='font-size:6px;color:#999;margin:0'>" + self.date.strftime("%c") + "</span>"

    def get_image_html(self):
        return "<img src=" + str(self.user_pic) + ">"

    def get_html(self):
        return (("<table bgcolor='#FFFFFF' style='border-collapse: collapse; border-spacing:0'>"
                 "<tr>" +
                 "<td style='max-width:15%;'>" + self.get_image_html() + "</td>" +
                 "<td style='width:85%;'>" + self.get_info_table() + "</td>" +
                 "</tr>" +
                 "</table>").replace("<td>", "<td style=padding: ""0rem;text-align: left; margin: 0'>")) \
            .replace("<th>", "<th style=padding:0rem;text-align: left; margin: 0'>")

    def get_other_info(self):
        return "<p style='font-size:6px;color:#999;margin:0'>#Retweeted: " + str(self.retweet_count) + \
               ",  Retweeted Author: @" + str(self.retweeted_author) + "</p>"

    def get_info_table(self):
        return "<table style='border-collapse: collapse'>" + \
               "<thead>" + self.get_header_row() + "</thead>" + \
               self.get_normal_row(self.get_text_html()) + \
               self.get_normal_row(self.get_other_info()) + "</table>"

    def jsonify(self):
        return {
            "coordinate":{"latitude": self.latitude,
                           "longitude": self.longitude},
            "id": str(self.id),
            "htmlLabel":self.get_html()
        }

