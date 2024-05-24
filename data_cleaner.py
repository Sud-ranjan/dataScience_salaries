import pandas as pd
import matplotlib as plt
import numpy as np

df = pd.read_csv("./data_scraped.csv")

# salary parsing
df['hourly'] = df['Salary Estimate'].apply(lambda x: True if 'per hour' in x.lower() else False)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: True if 'employer provided salary:' in x.lower() else False)


df = df[df['Salary Estimate'] != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
removed_kd = salary.apply(lambda x: x.replace('K','').replace('$',''))
removed_hr = removed_kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary'] = removed_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = removed_hr.apply(lambda x: int(x.split('-')[1]))

df['avg_salary'] = (df.min_salary + df.max_salary)/2



# comp name text only
df['company_text'] = df.apply(lambda x: x['Company Name'] if x['Rating']=='-1' else x['Company Name'][:-3], axis = 1)

# state & city field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
df['job_city'] = df['Location'].apply(lambda x: x.split(',')[0])

# job is at headquarters

df['same_state_as_hq'] =  df.apply(lambda x: True if x.Location == x.Headquarters else False, axis = 1)


# company age
from datetime import datetime
current_year = datetime.now().year
df['company_age'] = df.Founded.apply(lambda x: x if x<1 else current_year-x)

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

# print(df.api_dev_yn.value_counts())

df_out = df.drop(['Unnamed: 0'],axis = 1)

df_out.to_csv('glassdoor_datascience_salaries_cleaned.csv')