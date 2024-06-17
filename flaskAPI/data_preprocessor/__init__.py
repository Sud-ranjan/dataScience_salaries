import pandas as pd
import matplotlib as plt
import numpy as np

def job_title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    elif 'Gen AI' in title.lower():
        return 'AI engineer'
    else:
        return 'na'
    

def seniority (title):
    if 'sr' in title.lower() or 'sr.' in title.lower() or 'senior' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
        return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower() or 'junior' in title.lower():
        return 'junior'
    else:
        return 'na'

def rename_cols(df):
    df.rename(columns={
            'city':'job_city', 
            'company-size':'Size', 
            'companyName':'company_text', 
            'competitors':'Competitors', 
            'founded':'Founded',
            'industry':'Industry', 
            'jobDescription': 'Job Description', 
            'jobTitle': 'Job Title',
            'ownership':'Type of ownership', 
            'rating':'Rating', 
            'revenue':'Revenue', 
            'sector':'Sector', 
            'state': 'job_state'
        }, inplace=True)

def parse_input(df):
    # salary parsing
    # comp name text only
    # df['company_text'] = df.apply(lambda x: x['Company Name'] if x['Rating']=='-1' else x['Company Name'][:-3], axis = 1)
    # state & city field

    rename_cols(df)

    print(df.columns)
    # job is at headquarters
    # print(df.head())
    df['same_state_as_hq'] =  df.apply(lambda x: True if x.job_state == x.hqState and x.job_city == x.hqCity else False, axis = 1)
    # company age
    from datetime import datetime
    current_year = datetime.now().year
    df['company_age'] = df.Founded.apply(lambda x: x if int(x)<1 else current_year-int(x))

    # parsing of job desc for skills eg python/R etc
    # python
    # spark
    # cloud
    # BigData
    # Kubernetes/docker
    # tableau/powerbi

    df['python_yn'] = df['Job Description'].apply(lambda x: True if 'python' in x.lower() else False)
    df['spark_yn'] = df['Job Description'].apply(lambda x: True if 'spark' in x.lower() else False)
    df['cloud_yn'] = df['Job Description'].apply(lambda x: True if 'azure' in x.lower() or 'gcp' in x.lower() or 'aws' in x.lower() else False)
    df['deployments_yn'] = df['Job Description'].apply(lambda x: True if 'kubernetes' in x.lower() or 'docker' in x.lower() else False)
    df['viz_tools_yn'] = df['Job Description'].apply(lambda x: True if 'tableau' in x.lower() or 'powerbi' in x.lower() or 'looker' in x.lower() else False)
    df['api_dev_yn'] = df['Job Description'].apply(lambda x: True if 'javascript' in x.lower() or 'react' in x.lower() or 'flask' in x.lower() else False)

    # adding job title simplified
    df['job_title_simplified'] = df['Job Title'].apply(job_title_simplifier)

    # adding seniority
    df['seniority'] = df['Job Title'].apply(seniority)

    # Job Description Length
    df['jd_length'] = df['Job Description'].apply(lambda x: len(x))

    # Competitors Count
    df['num_comp'] = df['Competitors'].apply(lambda x: len(x.split(',')) if x != '-1' else 0)
    
    req_features = ['Rating','Size','Type of ownership','Industry', 'Sector', 'Revenue','num_comp','job_state','same_state_as_hq','company_text',
            'company_age','python_yn', 'spark_yn', 'cloud_yn','deployments_yn','viz_tools_yn', 'api_dev_yn','job_title_simplified', 'seniority','jd_length']

    return df[req_features]

    
