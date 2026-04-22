from generate_rec_id import *


inn = 22110199500001
# expected_record_id = "4076401266"
record_id = func_generate_record_id(str(inn), verbose=True)
print(f"Generated Record ID: {record_id}")

# assert record_id == expected_record_id, f"Expected {expected_record_id}, got {record_id}"

hashed_rec_id = func_generate_sha(record_id, salt=SALT)
# assert hashed_rec_id == "fc82bcf49c1630209a816c668240b4b363ace3bcc1f1f7675bcbe39ef07d1d87e6faf789c5155b424455863d1be9877c867db2a25465dadba3688420e7ab6bd3", f"Expected fc82bcf49c1630209a816c668240b4b363ace3bcc1f1f7675bcbe39ef07d1d87e6faf789c5155b424455863d1be9877c867db2a25465dadba3688420e7ab6bd3, got {hashed_rec_id}"
print(f"SHA-512 Hash: {hashed_rec_id}")
