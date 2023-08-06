class Metric:
    def __init__(self, user_info):
        self.user_info = user_info

    def process(self, data):
        return data

    def process_event_data(self, data):
        return data

    def generate_detail_list_sql(self, click_args):
        sql = f"select * from work_workorder where <filters> and template_id={click_args['item_data']['id']} and create_time between <start_time> and <end_time>"
        return sql

    def process_detail_list_data(self, data):
        return data