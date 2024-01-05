from datetime import datetime, date

from django.apps import apps
from django.core.paginator import Paginator
from django.db.models import Q, Model

from altar.utils.training import TrainingAttributes

# Create Here
class OrdersData:
    _response: dict = {}
    _data_list: list = []
    _instance: Model = None
    _request: None
    _app_name: str = ''
    _model_name: str = ''
    _query = Q(pk__isnull=False)
    _data_type = ''
    _selected_related = []
    _annotations = None
    _paginate: bool = True
    _jsonify: bool = True
    _distinct: bool = True
    """
        Returns a dictionary of the serialized data
    """
    @property
    def response(self) -> dict:
        return self._response
    

class GetSerializedData(OrdersData):
    """"
        Generates Json Data from the specified model
    Args:
        request (Request): Django request object
        app_name (str): App name containing the model
        model_name (str): Model name data to be extracted
        query (Q): Any filtration created using Q object
        data_type (str): Schema name to extract data from
        select_related (list): List of select related fields
        annotate (None): Any annotations that require addition
        (default is False)

    Returns:
        None
    """
    def __init__(self,
                 request,
                 app_name: str,
                 model_name: str,
                 query: Q,
                 data_type: str,
                 select_related: list,
                 annotate: None = None,
                 paginated: bool = True,
                 jsonify: bool = False,
                 distinct: bool = False
                 ) -> None:
        super().__init__()
        self._request = request
        self._app_name = app_name
        self._model_name = model_name
        self._query = query
        self._data_type = data_type
        self._select_related = select_related
        self._annotations = annotate
        self._paginate = paginated
        self._jsonify = jsonify
        self._data_list = []
        self._distinct = distinct
        self._instance = self.get_model()
        self.get_data()

    def get_model(self) -> Model:
        model = apps.get_model(app_label=self._app_name, model_name=self._model_name)
        if isinstance(self._annotations, dict):
            return model.objects.filter(self._query).annotate(
                **self._annotations
            ).select_related(*self._select_related).order_by("-pk").distinct() if self._distinct else model.objects.filter(self._query).annotate(
                **self._annotations
            ).select_related(*self._select_related).order_by("-pk").distinct()

        return model.objects.filter(self._query).select_related(*self._select_related).order_by("-pk").distinct() if self._distinct else model.objects.filter(self._query).select_related(*self._select_related).order_by("-pk")

    def check_related_field(self, key, value: str, data, d_dict):
        new_data = data
        v_split = value.split('.')
        for sp in v_split:
            if hasattr(new_data, sp):
                new_data = getattr(new_data, sp)

        d_dict[key] = new_data

    def get_data(self):
        return self.pagination()

    def pagination(self) -> None:
        rows = self._request.GET.get('rows') or 25
        page = self._request.GET.get('page') or 1
        instance = self._instance
        attrs = DataFactory(self._data_type).factory()

        if not self._paginate:
            d_list = []

            for data in instance:
                d_dict = {}
                for attr in attrs.items():
                    key = attr[0]
                    value = attr[1]
                    if hasattr(data, value):
                        new_value = getattr(data, value)
                        if self._jsonify:
                            if isinstance(new_value, datetime):
                                new_value = datetime.strftime(new_value, '%Y-%m-%d')
                            if isinstance(new_value, date):
                                new_value = datetime.strftime(new_value, '%Y-%m-%d')
                        d_dict[key] = new_value
                    else:
                        self.check_related_field(key, value, data, d_dict)
                d_list.append(d_dict)
            self._response[self._data_type] = d_list
            return

        if rows == '0':
            rows = instance.count()

        paginator = Paginator(instance, rows)
        self._data_list = paginator.page(int(page))

        try:
            next_page = self._data_list.next_page_number()
        except:
            next_page = None

        try:
            previous_page = self._data_list.previous_page_number()
        except:
            previous_page = None

        d_list = []

        for data in self._data_list.object_list:
            d_dict = {}
            for attr in attrs.items():
                key = attr[0]
                value = attr[1]
                if hasattr(data, value):
                    new_value = getattr(data, value)
                    if self._jsonify:
                        if isinstance(new_value, datetime):
                            new_value = datetime.strftime(new_value, '%Y-%m-%d')
                        if isinstance(new_value, date):
                            new_value = datetime.strftime(new_value, '%Y-%m-%d')
                    d_dict[key] = new_value
                else:
                    self.check_related_field(key, value, data, d_dict)
            d_list.append(d_dict)
        self._response[self._data_type] = d_list

        self._response['pagination'] = {
            'has_next': self._data_list.has_next(),
            'has_previous': self._data_list.has_previous(),
            'next_page': next_page,
            'previous_page': previous_page,
            'page': self._data_list.number,
            'total_pages': self._data_list.paginator.num_pages,
            'count': self._data_list.paginator.count
        }


class DataFactory(object):
    def __init__(self, data_type: str) -> None:
        self.data_type = data_type
        self.attrs = {}

    def factory(self) -> dict:
        if self.data_type == "trainings":
            self.attrs = TrainingAttributes().attrs

            
        return self.attrs