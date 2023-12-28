# Measurement_for_SPF_and_DMARC_2023

## Introduction
This work is part of our paper **"Both Sides Needed: A Two-Dimensional Measurement Study of Email Security Based on SPF and DMARC"**. This paper has been accepted by **the  19th International Conference on Mobility, Sensing and Networking (MSN)**. We implement assessments in the scope of the Alexa Top Million ranked domains in September 2021, March 2022 and April 2023. First, we extract and de-duplicate the root domains in the list, leaving only 224,789 individual domains as the dataset for our measurement study. The domain list is in ./top-1m-no.csv. Results of 2022 is in ./measurement_result_2022.zip. 

Most recent results of 2023 is in ./measurement_result_2023/. Under this directory, dig_crawl.py is used for original MX, SPF, and DMARC record extraction; valid_check.py is used to check whether the SPF and DMARC records are valid or not;  mail.py is used for sending test emails to domains that have MX record to validate whether the domain server has SPF and DMARC verification funciton.

log1-5.zip are the original log text from the receiving server.
