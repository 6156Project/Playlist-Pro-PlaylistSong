from resources.base_resource import BaseResource


class PlaylistResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)
        self.data_service = None

    def get_full_collection_name(self):
        return self.config.collection_name

    def get_data_service(self):
        if self.data_service is None:
            self.data_service = self.config.data_service
        return self.data_service

    def get_resource_by_id(self, id):
        pass

    def get_by_template(self,
                        relative_path=None,
                        path_parameters=None,
                        template=None,
                        field_list=None,
                        limit=None,
                        offset=None,
                        order_by=None):
        
        return super().get_by_template(relative_path, path_parameters, template, field_list,
                                         limit, offset, order_by)

    def create_resource(self, resource_data):
        return super().create_resource(resource_data)

    def delete_resource(self, resource_data):
        template = {'id': resource_data}
        return super().delete_resource(template)

    def update_resource(self, id, resource_data):
        template = {'id': id}
        return super().update_resource(resource_data, template)