
CREATE OR REPLACE FUNCTION func_dsp_dsml_generate_record_id(
    p_inn IN VARCHAR2,
    p_shift in number default 0
) RETURN VARCHAR2 IS
    -- Configuration Constants
    v_base_date DATE := TO_DATE('1940-01-01', 'YYYY-MM-DD');
    v_sex_capacity NUMBER := 100000;
    v_daily_capacity NUMBER := 200000;

    -- Variables
    v_sex_digit NUMBER;
    v_dob_str VARCHAR2(8);
    v_suffix NUMBER;

    v_current_date DATE;
    v_days_offset NUMBER;
    v_sex_index NUMBER;
    v_record_id NUMBER;
    v_ag_shift NUMBER := 1265;
BEGIN
    -- 1. Parse Input
    -- Note: SUBSTR in Oracle is 1-indexed. SUBSTR(string, start_position, length)
    v_sex_digit := TO_NUMBER(SUBSTR(p_inn, 1, 1));
    v_dob_str   := SUBSTR(p_inn, 2, 8);
    v_suffix    := TO_NUMBER(SUBSTR(p_inn, 10));

    -- 2. Extract Date Components
    -- TO_DATE parses the 8-character string directly into a date object
    v_current_date := TO_DATE(v_dob_str, 'DDMMYYYY');

    -- 3. Calculate "Days Since Base"
    -- Subtracting dates in Oracle yields the difference in days
    v_days_offset := TRUNC(v_current_date) - TRUNC(v_base_date);

    IF v_days_offset < 0 THEN
        RETURN NULL; -- Mirrors Python returning None on ValueError
    END IF;

    -- 4. Normalize Sex (1=Female->0, 2=Male->1)
    IF v_sex_digit NOT IN (1, 2) THEN
        RETURN NULL;
    END IF;

    v_sex_index := 2 - v_sex_digit;

    -- 5. Compute Final ID
    v_record_id := (v_days_offset * v_daily_capacity) +
                   (v_sex_index * v_sex_capacity) +
                   v_suffix + v_ag_shift + p_shift;

    RETURN TO_CHAR(v_record_id);

EXCEPTION
    -- Catches any parsing errors (e.g., bad date, non-numeric characters)
    -- and returns NULL, mirroring your Python try/except block.
    WHEN OTHERS THEN
        RETURN NULL;
END func_dsp_dsml_generate_record_id;


----------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION func_dsml_dsp_sha_algorithm(p_data                      IN VARCHAR2,
                                                    p_salt                      IN VARCHAR2 DEFAULT '',
                                                    p_algorithm                 IN VARCHAR2 DEFAULT 'SHA512'
                                                    )
  RETURN VARCHAR2 IS
  v_result   VARCHAR2(4000);
  v_initials VARCHAR2(100) := '';
BEGIN
  -- Return NULL if the input data is NULL
  IF p_data IS NULL THEN
    RETURN NULL;
  END IF;

  -- Route STANDARD_HASH through the SQL engine
  SELECT LOWER(RAWTOHEX(STANDARD_HASH(UTL_I18N.STRING_TO_RAW( p_salt || p_data ,
                                                             'AL32UTF8'),
                                      UPPER(p_algorithm))))
    INTO v_result
    FROM dual;



    RETURN v_result;

END func_dsml_dsp_sha_algorithm;



-----------------------TESTING-----------------------
begin
  -- Call the function
  :REC_ID := func_dsp_dsml_generate_record_id(p_inn => '22110199500001'
                                              );
  :HASHED_REC_ID := func_dsml_dsp_sha_algorithm(p_data      => :REC_ID,
                                                p_salt      => ''
                                                );
end;

