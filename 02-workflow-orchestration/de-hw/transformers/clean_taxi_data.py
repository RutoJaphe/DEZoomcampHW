if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform_taxi_data(data, *args, **kwargs):

    passenger_count_fixed = data[data['passenger_count']>0]
    trip_distance_fixed = passenger_count_fixed[passenger_count_fixed['trip_distance']>0]
    data = trip_distance_fixed

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data = data.rename(columns={'VendorID':'vendor_id'})
    data.columns = (data.columns.str.replace(' ','_')
                                .str.lower()
                                )
    

    return data



@test 
def test_output(output, *args) -> None:
    assert output is not None, 'The output is Undefined'

@test
def vendor_id_col_test(output, *args) -> None:
    assert 'vendor_id' in output.columns, 'Column not found'

@test
def passenger_count_test(output, *args) -> None:
   
    assert (output['passenger_count']==0).sum()==0, 'There are trips with 0 passengers'

@test
def trip_distance_test(output, *args) -> None:

    assert (output['trip_distance']==0).sum()==0, 'There are trips with 0 miles'
