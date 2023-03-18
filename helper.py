phone_regex = r"^(?:\+20|0)?1[0-2]\d{8}$"

def is_egyptian_national_id(national_id):
    # check if national_id is a string of 14 digits
    if not isinstance(national_id, str) or not re.match(r'^\d{14}$', national_id):
        return False
    
    # check if the first digit is either 2, 3, 4, or 9
    if national_id[0] not in ['2', '3', '4', '9']:
        return False

    return True