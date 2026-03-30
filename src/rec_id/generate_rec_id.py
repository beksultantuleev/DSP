from datetime import date, timedelta
import hashlib
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


SALT = os.getenv("SALT", "")

def func_generate_record_id(inn: str, shift: int = 0, verbose=False) -> Optional[str]:
    # Configuration
    BASE_DATE = date(1940, 1, 1)
    SEX_CAPACITY = 100000
    DAILY_CAPACITY = 2 * SEX_CAPACITY  # (2 sexes * 100,000 codes)
    AG_shift = 1265

    try:
        # 1. Parse Input
        sex_digit = int(inn[0])
        dob_str = inn[1:9]      # Extracts the 8 date digits (DDMMYYYY)
        suffix = int(inn[9:]) + AG_shift + shift

        # 2. Extract Date Components
        day = int(dob_str[0:2])
        month = int(dob_str[2:4])
        year = int(dob_str[4:8])

        current_date = date(year, month, day)

        # 3. Calculate "Days Since Base"
        delta = current_date - BASE_DATE
        days_offset = delta.days

        if days_offset < 0:
            raise ValueError(
                f"Date {current_date} is before base date {BASE_DATE}")

        # 4. Normalize Sex (1=Female->0, 2=Male->1)
        if sex_digit not in (1, 2):
            raise ValueError("Sex digit must be 1 (Female) or 2 (Male)")

        sex_index = 2 - sex_digit

        # 5. Compute Final ID
        record_id = (days_offset * DAILY_CAPACITY) + \
            (sex_index * SEX_CAPACITY) + suffix
        return str(record_id)

    except (ValueError, IndexError) as e:
        # We log the error internally, but return None to signal failure
        if verbose:
            print(f"Logic Error: {e}")
        return None

def func_generate_sha(input_data: str,  bit_length: int = 512, salt: str = "") -> str:
    if input_data is None:
        return None
    # 1. Encode string to bytes
    encoded_data = input_data.encode('utf-8')
    encoded_salt = salt.encode('utf-8')

    # Note: Concatenating here as requested
    combined_data = encoded_salt + encoded_data

    # 2. Select the correct hash object
    if bit_length == 512:
        hash_obj = hashlib.sha512()
    elif bit_length == 256:
        hash_obj = hashlib.sha256()
    elif bit_length == 384:
        hash_obj = hashlib.sha384()
    else:
        raise ValueError("Invalid bit_length. Supported values: 256, 384, 512")

    # 3. Update and return
    hash_obj.update(combined_data)
    return hash_obj.hexdigest()

if __name__ == "__main__":
    inn = 22110199500001
    expected_record_id = "4076401266"
    record_id = func_generate_record_id(str(inn), verbose=True)
    print(f"Generated Record ID: {record_id}")
    
    assert record_id == expected_record_id, f"Expected {expected_record_id}, got {record_id}"

    hashed_rec_id = func_generate_sha(expected_record_id, salt=SALT)
    assert hashed_rec_id == "fc82bcf49c1630209a816c668240b4b363ace3bcc1f1f7675bcbe39ef07d1d87e6faf789c5155b424455863d1be9877c867db2a25465dadba3688420e7ab6bd3", f"Expected fc82bcf49c1630209a816c668240b4b363ace3bcc1f1f7675bcbe39ef07d1d87e6faf789c5155b424455863d1be9877c867db2a25465dadba3688420e7ab6bd3, got {hashed_rec_id}"
    print(f"SHA-512 Hash: {hashed_rec_id}")
