import vaex

class DataProcessor:
    def __init__(self, request):
        self.request = request

    def run(self):
        if not self.request.data_processing_requested():
            return
        data_df = vaex.from_csv("data.csv", copy_index=False)
        xyz_df = vaex.from_csv("xyz.csv", copy_index=False)
        out_df = data_df.join(xyz_df, left_on='xyz_id', right_on='id', lsuffix='d', rsuffix='x')
        out_df.export_csv('out.csv')
