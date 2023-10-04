from accounts.models import Staff
import django_filters

class StaffFilter(django_filters.FilterSet):
    class Meta:
        model = Staff
        fields = ['Account_id__first_name', 'Account_id__last_name', 'Address','Account_id__date_joined', ]


def filter_staff(address,first_name):
    print('entering filter function')
    print(address)
    print(first_name)
    result = {}
    if (not address) and (not first_name):
        print('No Filter')
        result['bool'] = False
        

    elif address and (not first_name):
        print('Address Filter')
        result['bool'] = True
        result['staff'] = Staff.objects.filter(Address = address)
        

    elif (not address) and first_name:
        result['bool'] = True
        result['staff'] = Staff.objects.filter(Account_id__first_name = first_name)
        
    
    elif address and first_name:
        result['bool'] = True
        result['staff'] = Staff.objects.filter(Account_id__first_name = first_name , Address = address)

    return result
        

