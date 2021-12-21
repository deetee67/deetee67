#!/usr/bin/env python
# coding: utf-8

# In[175]:


#1. Set up libraries
#Import libraries
import pandas as pd
import re
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('classic')
get_ipython().run_line_magic('matplotlib', 'inline')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', -1)


# Research question - Compare the the activity and performance of younger students in a stem related subject (Earth Science) across the 5 Boroughs.  I decided to look at the younger students of the dataset to get some insights as to whether or not Stem related subjects are being instroduced early in the academic life of a student, hoping that the dataset will reveal how ambitious this initaitive is by determining how young students are entered for some subjects and how many students in any given year or Borough.

# In[176]:


#2. Upload
#Read csv file
#Viewing the data - 212,331 rows, 15 columns
df=pd.read_csv("https://raw.githubusercontent.com/CunyLaguardiaDataAnalytics/datasets/master/2014-15_To_2016-17_School-_Level_NYC_Regents_Report_For_All_Variables.csv")


# In[177]:


#3. Exploring original dataset
df.shape


# In[178]:


df.head(3)


# In[179]:


df.tail(2)


# In[180]:


#Explore random sample of 5 of original dataset
df.sample(2)


# In[181]:


#Explore column information
df.columns


# In[182]:


#Explore list of subjects/ Regents exam
df[['Regents Exam']].value_counts()


# In[183]:


#Explore List/Count of all school levels in dataset
df["School Level"].value_counts()


# In[184]:


df["School Name"].nunique()


# In[185]:


df.info()


# In[186]:


#4. Cleaning of DATA
#Remove all record/ row of data that has mean score of 's'
df = df.loc[df["Mean Score"]!='s']


# In[187]:


#shows that 75,000 rows of data removed (additional col - Borough)
df.shape


# In[188]:


#5. Transformation - datatype conversion and string formatting, subsetting of dataset
# Converting columns Mean Score and Number Scoring 80 or Above to numeric data type 
df[["Mean Score", "Number Scoring 80 or Above"]]=df[["Mean Score","Number Scoring 80 or Above"]].apply(pd.to_numeric)


# In[189]:


#Show that col=Mean score and col=Number scoring above 80 datatype now converted to numeric
df.dtypes


# In[190]:


#copy School DBN column creating new column for Boroughs
#Remove the numbers before and after the Borough Letter - K,M,Q,R,X
df["Boroughs"]=df["School DBN"]
df["Boroughs"] = df.Boroughs.str.replace('\d+', '',regex=True )


# In[191]:


#Create subset of dataset of relevant columns
SchoolCol = df[["School DBN","Boroughs","School Name", "School Level","Regents Exam", "Year", "Total Tested", "Mean Score", "Number Scoring 80 or Above"]]
SchoolCol.sample(2)


# In[192]:


#Create subset of dataset of relevant columns
Final_df = df[["School DBN","Boroughs", "School Level","Regents Exam", "Year", "Total Tested", "Number Scoring 80 or Above"]]
Final_df.sample(2)


# In[193]:


#Check new shape (rows/columns) of adjusted dataset
Final_df.shape


# In[194]:


#Sample Selection - selecting only Physical Settings/Earth Science and K8 school level
ExamEarthSci = Final_df[(Final_df["Regents Exam"]=="Physical Settings/Earth Science") & (SchoolCol["School Level"]=="K-8")]
ExamEarthSci.groupby(['Boroughs', 'Year']).sum()


# In[195]:


#6. Data Visualization
#HISTOGRAM - showing Total Tested - Earth Science, School Level-K8 
ExamEarthSci.hist(column='Total Tested', bins=5, color='#478800')
plt.xlabel('All Boroughs 2015-2017 Regents Exam - Physical Settings/Earth Science-K8')
plt.ylabel('Frequency')


# In[196]:


#HISTOGRAM - showing count of K8 students scoring 80 and above on Earth Science
ExamEarthSci.hist(column='Number Scoring 80 or Above', bins=5, color='#110055')
plt.xlabel('All Boroughs 2015-2017 Regents Exam - Physical Settings/Earth Science-K8')
plt.ylabel('Frequency')


# In[197]:


ExamEarthSci_plot2 = ExamEarthSci[["Total Tested", "Number Scoring 80 or Above"]]
ExamEarthSci_plot2.hist(bins=5)


# In[198]:


ExamEarthSci.groupby(['Boroughs', 'Year']).max()


# In[199]:


#ExamEarthSci.plot()
ExamEarthSci.groupby('Boroughs').max()


# In[200]:


#ExamEarthSci.plot()
ExamEarthSci.groupby('Boroughs').min()


# In[201]:


#ExamEarthSci.plot()
ExamEarthSci.groupby('Boroughs').mean()


# In[202]:


#ExamEarthSci.plot()
ExamEarthSci.groupby('Boroughs').sum()


# In[203]:


#ExamEarthSci.plot()
ExamEarthSci.groupby('Year').sum()


# In[204]:


#Show descriptive stats/mean, max, min/ of cols Total_Tested/ Score above 80 - K8 students in Earth Science
ExamEarthSci_plot2.describe()


# In[205]:


ExamEarthSci_plot2.plot.hist(stacked=True, bins=8,alpha=.6)


# In[206]:


ExamEarthSci.groupby(['Boroughs']).sum()


# In[207]:


#ExamEarthSci_plot = df[["Boroughs","Total Tested","Number Scoring 80 or Above"]]
sns.pairplot(ExamEarthSci_plot2)


# In[208]:


#ExamEarthSci = sns.load_dataset("ExamEarthSci")
#ExamEarthSci.head()
sns.displot(x ='Total Tested',kde=True,bins = 4 ,
hue = df['Year'] , palette = 'vlag', data=ExamEarthSci)


# In[209]:


sns.scatterplot(x='Total Tested', y ='Number Scoring 80 or Above' ,
data = ExamEarthSci , hue = 'Boroughs')


# In[210]:


sns.jointplot(x = 'Total Tested', y = 'Number Scoring 80 or Above',
data = ExamEarthSci,hue = 'Boroughs')


# In[211]:


sns.scatterplot(x='Total Tested', y ='Number Scoring 80 or Above' ,
data = ExamEarthSci , hue = 'Year')


# In[212]:


sns.jointplot(x = 'Total Tested', y = 'Number Scoring 80 or Above',
data = ExamEarthSci,hue = 'Year')


# In[213]:


#Showing schools/ occurrences of 10 and under total students tested 2015-2017
ExamEarthSci_Borough = ExamEarthSci[(ExamEarthSci["Total Tested"]<=10)]
ExamEarthSci_Borough.groupby('Year').sum().plot(kind='bar')


# In[214]:


#Showing schools/ occurrences of 100+ total students tested 2015 to 2017
ExamEarthSci_Borough = ExamEarthSci[(ExamEarthSci["Total Tested"]>=100)]
ExamEarthSci_Borough.groupby('Year').sum().plot(kind='bar')


# In[215]:


#Showing a positive correlation between Total Tested and score above 80
sns.scatterplot(data = ExamEarthSci_plot3, x = "Total Tested", y = "Number Scoring 80 or Above")
plt.show()


# In[216]:


#Showing (mean) comparison of total tested/ Numbers scoring above 80 ACROSS the Boroughs
ExamEarthSci_plot3 = ExamEarthSci[["Boroughs","Total Tested", "Number Scoring 80 or Above"]]
ExamEarthSci_plot3.groupby('Boroughs').mean().plot(kind='barh', title="Mean comparison across Boroughs")


# In[217]:


ExamEarthSci_plot3.groupby('Boroughs').sum().plot(kind='barh')


# In[218]:


ExamEarthSci_plot3.groupby('Boroughs').max().plot(kind='barh', title='Chart showing MAX across Boroughs')
plt.xlabel("Max")


# In[219]:


Queens_Borough = ExamEarthSci[(ExamEarthSci["Boroughs"]=="Q")]
Queens_Borough.groupby('Year').sum().plot(kind='bar',title='Queens Borough(Sum) 2015-2017')
plt.ylabel("Sum")


# In[220]:


Brooklyn_Borough = ExamEarthSci[(ExamEarthSci["Boroughs"]=="K")]
Brooklyn_Borough.groupby('Year').sum().plot(kind='bar', title='Brooklyn Borough (Sum) 2015-2017')
plt.ylabel("Sum")

