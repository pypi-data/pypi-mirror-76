import pytest
from .instance import Instance

def _validate_dict(spec, res):
    for k,v in spec.items():
        assert res[k] == v, "{}: {} != {}".format(k, res[k], v)


def create_valids(component, validate_result=_validate_dict, **kwargs):
    valids = component.valids(**{
        "endpoint": component.endpoints.create,
        **kwargs
    })
    for spec in valids:
        data = component.endpoints.create.call(spec)
        assert data
        print("test valid:", data)
        validate_result(spec, data)
    return valids


def create_invalids(component, **kwargs):
    invalids = component.invalids(**{
        "endpoint": component.endpoints.create,
        **kwargs
    })
    for invalid in invalids:
        with pytest.raises(Exception):
            component.endpoints.create.call(invalid)
    return invalids


def read_valids(component, validate_result=_validate_dict, **kwargs):
    valids = component.valids(**{
        "endpoint": component.endpoints.create,
        **kwargs
    })
    for spec in valids:
        data = component.endpoints.create.call(spec)
        res = component.endpoints.read.call(data)
        assert res, "result of read endpoint None for {}".format(data)
        validate_result(data, res)
    return valids


def read_invalids(component, invalids, **kwargs):
    for invalid in invalids:
        with pytest.raises(Exception) as e:
            component.endpoints.read.call(invalid)
        print(e)
    return invalids


def update_valids(component, validate_result=_validate_dict, **kwargs):
    update_valids = component.valids(**{
        "endpoint": component.endpoints.update,
        **kwargs
    })
    create_valids = component.valids(**{
        "endpoint": component.endpoints.create,
        "count": len(update_valids)
    })
    for create_spec,update_spec in zip(create_valids,update_valids):
        data = component.endpoints.create.call(create_spec)
        data_updated = component.endpoints.update.call(data, update_spec)
        assert data_updated, "result of update endpoint None for {} / {}".format(data, update_spec)
        validate_result(update_spec, data_updated)
        data_read = component.endpoints.read.call(data)
        validate_result(update_spec, data_read)
    return update_valids


def update_invalids(component, **kwargs):
    update_specs = component.invalids(**{
        "endpoint": component.endpoints.update,
        **kwargs
    })
    create_specs = component.valids(**{
        "endpoint": component.endpoints.create,
        "count": len(update_specs)
    })
    for create_spec,update_spec in zip(create_specs,update_specs):
        data = component.endpoints.create.call(create_spec)
        print(update_spec)
        with pytest.raises(Exception):
            component.endpoints.update.call(data, update_spec)
    return update_specs


def list_total(component, total_from_res=None, instance_count=10):
    if total_from_res is None:
        total_from_res = lambda res: len(res)
    current_count = total_from_res(component.endpoints.list.call({}))
    instances = []
    for i in range(instance_count):
        instances.append(Instance(component).__enter__())
        current_count_ = total_from_res(component.endpoints.list.call({}))
        assert current_count_ == current_count + 1, (current_count_, current_count)
        current_count = current_count_
    for instance in instances:
        instance.__exit__(None, None, None)
        current_count_ = total_from_res(component.endpoints.list.call({}))
        assert current_count_ == current_count - 1, (current_count_, current_count)
        current_count = current_count_


def list_valids(component, total_from_res=None, instance_count=10, **kwargs):
    specs = component.valids(**{
        "endpoint": component.endpoints.list,
        **kwargs
    })
    instances = []
    for i in range(instance_count):
        instances.append(Instance(component).__enter__())
    for spec in specs:
        component.endpoints.list.call(spec)
    for instance in instances:
        instance.__exit__(None, None, None)
    return specs


def list_invalids(component, total_from_res=None, instance_count=10, **kwargs):
    specs = component.invalids(**{
        "endpoint": component.endpoints.list,
        **kwargs
    })
    instances = []
    for i in range(instance_count):
        instances.append(Instance(component).__enter__())
    for spec in specs:
        with pytest.raises(Exception):
            component.endpoints.list.call(spec)
    for instance in instances:
        instance.__exit__(None, None, None)
    return specs