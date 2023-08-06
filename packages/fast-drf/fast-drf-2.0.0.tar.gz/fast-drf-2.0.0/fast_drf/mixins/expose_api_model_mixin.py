class ExposeApiModelMixin(object):
    """
    ==== MODEL MIXIN ====

    This Mixin(Class) will help to generate automatic api from models with few configs
    """

    @classmethod
    def exposed_api(cls, *args, **kwargs):
        """
        This method holds a bunch of API configs and return like following...
        {
            "api_url": "",  # (REQUIRED)

            # You must use from HTTPVerbsEnum. Like HTTPVerbsEnum.GET.value, HTTPVerbsEnum.POST.value
            "allowed_methods": ['get', 'post', 'put', 'patch', 'delete'], # (NOT REQUIRED)

            # slug_field is application 'put', 'patch', 'delete' these methods
            "slug_field": "pk", # (NOT REQUIRED) DEFAULT [PK] (Must be model field, unique or primary key)

            "queryset": "",  # (NOT REQUIRED) default all
            "viewset_class": "",  # (NOT REQUIRED) BaseViewset class
            "serializer_class": "",  # (NOT REQUIRED) default BaseEntitySerializer
            "permission_classes": "",  # (NOT REQUIRED) default set from settings
        }
        :param args:
        :param kwargs:
        :return: An empty Dictionary/False OR Full config dictionary.
        """
        api_configs = {}
        return api_configs

    @classmethod
    def api_version_fields(cls, **kwargs):
        """
        *** DEFAULT VERSION `v1` ***

        This method will return a dictionary object with version number and fields name. Fields are similar like
        serializer fields. Or you can say exactly as same as serializer fields.
        :param kwargs: Currently nothing to receive on kwargs
        :return: a dictionary object with version number
        """
        versions = {}
        return versions
